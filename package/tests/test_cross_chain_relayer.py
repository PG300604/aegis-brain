"""Verification and security audit harness for the Async Cross-Chain Event Relayer.

Goal-driven criteria:
1. Sandbox Red-Team audit produces zero HIGH or CRITICAL findings.
2. Syntax and AST structure validate cleanly and expose the required contract.
3. Every behavioural criterion maps to a reproducible unit test.
"""

import ast
import asyncio
import hashlib
import re
import time
import unittest
from dataclasses import replace
from pathlib import Path
from typing import Any

from aegis.relayer import (
    AsyncCrossChainEventRelayer,
    CrossChainEvent,
    EventValidationError,
    FinalityError,
    ReplayDetectedError,
    RelayerPolicy,
    SignatureVerificationError,
    build_event,
    compute_signature,
)
from aegis.sandbox import RedTeamAuditor

RELAYER_SOURCE_PATH = Path(__file__).resolve().parents[1] / "aegis" / "relayer.py"
RELAYER_SOURCE = RELAYER_SOURCE_PATH.read_text(encoding="utf-8")

VERIFICATION_CRITERIA = {
    "valid_event_delivery": "TestCrossChainEventRelayer.test_valid_event_is_accepted_delivered_and_counted",
    "signature_integrity": "TestCrossChainEventRelayer.test_tampered_signature_is_rejected_before_delivery",
    "payload_integrity": "TestCrossChainEventRelayer.test_tampered_payload_is_rejected",
    "canonical_signature": "TestCrossChainEventRelayer.test_signature_is_deterministic_across_key_order",
    "signature_encoding": "TestCrossChainEventRelayer.test_non_lowercase_hex_signature_is_rejected",
    "replay_event_id": "TestCrossChainEventRelayer.test_duplicate_event_id_is_rejected",
    "replay_nonce": "TestCrossChainEventRelayer.test_regressed_nonce_is_rejected",
    "freshness_expired": "TestCrossChainEventRelayer.test_expired_event_is_rejected",
    "freshness_future_skew": "TestCrossChainEventRelayer.test_future_dated_event_is_rejected",
    "nonfinite_timestamp": "TestCrossChainEventRelayer.test_non_finite_timestamp_is_rejected",
    "chain_allowlist": "TestCrossChainEventRelayer.test_untrusted_chain_is_rejected",
    "cross_chain_only": "TestCrossChainEventRelayer.test_same_chain_event_is_rejected",
    "finality": "TestCrossChainEventRelayer.test_insufficient_finality_is_rejected",
    "payload_bounds": "TestCrossChainEventRelayer.test_oversized_payload_is_rejected",
    "noncanonical_payload": "TestCrossChainEventRelayer.test_non_canonical_payload_is_rejected_at_build",
    "nonce_bounds": "TestCrossChainEventRelayer.test_nonce_outside_uint64_is_rejected",
    "type_confused_nonce": "TestCrossChainEventRelayer.test_boolean_nonce_is_rejected",
    "event_id_bounds": "TestCrossChainEventRelayer.test_event_id_length_is_bounded",
    "missing_source_secret": "TestCrossChainEventRelayer.test_missing_source_secret_is_rejected",
    "empty_secret": "TestCrossChainEventRelayer.test_empty_secret_material_is_rejected",
    "policy_validation": "TestCrossChainEventRelayer.test_policy_rejects_invalid_limits",
    "retry_recovery": "TestCrossChainEventRelayer.test_transient_delivery_failure_retries_then_succeeds",
    "retry_exhaustion": "TestCrossChainEventRelayer.test_delivery_exhaustion_is_counted",
    "source_ordering": "TestCrossChainEventRelayer.test_source_ordering_is_preserved",
    "queue_backpressure": "TestCrossChainEventRelayer.test_bounded_queue_applies_backpressure",
    "zero_high_findings": "TestSecurityAuditHarness.test_sandbox_redteam_audit_has_zero_high_severity_findings",
    "syntax_and_ast": "TestSecurityAuditHarness.test_ast_validates_and_required_contract_exists",
    "no_dynamic_code_execution": "TestSecurityAuditHarness.test_no_dynamic_code_execution",
    "least_privilege_imports": "TestSecurityAuditHarness.test_imports_are_least_privilege",
    "no_hardcoded_secrets": "TestSecurityAuditHarness.test_no_hardcoded_credentials_or_secrets",
    "constant_time_signature_check": "TestSecurityAuditHarness.test_uses_constant_time_signature_comparison",
    "harness_catches_vulnerabilities": "TestSecurityAuditHarness.test_harness_detects_deliberately_vulnerable_candidate",
    "reproducible_audit": "TestSecurityAuditHarness.test_audit_report_is_reproducible_and_clean",
    "criteria_coverage": "TestVerificationCoverage.test_every_verification_criterion_maps_to_a_real_test",
    "test_registry_complete": "TestVerificationCoverage.test_every_test_is_registered_as_a_verification_criterion",
}


class SecurityAuditHarness:
    """Deterministic AST and Red-Team audit harness for a candidate module."""

    HIGH_SEVERITIES = frozenset({"HIGH", "CRITICAL"})
    ALLOWED_IMPORT_ROOTS = frozenset(
        {
            "__future__",
            "asyncio",
            "collections",
            "dataclasses",
            "hashlib",
            "hmac",
            "json",
            "math",
            "time",
            "typing",
        }
    )
    FORBIDDEN_CALL_NAMES = frozenset({"eval", "exec", "compile", "__import__", "breakpoint"})
    FORBIDDEN_ATTRIBUTE_PAIRS = frozenset(
        {
            ("marshal", "load"),
            ("marshal", "loads"),
            ("os", "execl"),
            ("os", "execv"),
            ("os", "popen"),
            ("os", "spawnv"),
            ("os", "system"),
            ("pickle", "load"),
            ("pickle", "loads"),
            ("yaml", "load"),
        }
    )
    FORBIDDEN_MAGIC_ATTRIBUTES = frozenset(
        {"__builtins__", "__code__", "__globals__", "__subclasses__"}
    )
    SECRET_PATTERNS = (
        ("telegram_bot_token", re.compile(r"\b[0-9]{9,10}:[a-zA-Z0-9_-]{35}\b")),
        ("github_pat", re.compile(r"\b(ghp|gho|ghu|ghs)_[A-Za-z0-9]{36}\b")),
        ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
        ("bearer_token", re.compile(r"(?i)bearer\s+[a-zA-Z0-9_\-\.]{25,}")),
        ("private_key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    )

    def __init__(self, source: str) -> None:
        self.source = source
        self.tree = ast.parse(source)
        self.syntax_valid = True

    def redteam_findings(self) -> list[dict[str, Any]]:
        return RedTeamAuditor.audit_code(self.source)["findings"]

    def high_severity_findings(self) -> list[dict[str, Any]]:
        return [
            finding
            for finding in self.redteam_findings()
            if finding["severity"] in self.HIGH_SEVERITIES
        ]

    def forbidden_calls(self) -> list[str]:
        hits: list[str] = []
        for node in ast.walk(self.tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if isinstance(func, ast.Name) and func.id in self.FORBIDDEN_CALL_NAMES:
                hits.append(func.id)
            if isinstance(func, ast.Attribute):
                owner = func.value
                if isinstance(owner, ast.Name):
                    if (owner.id, func.attr) in self.FORBIDDEN_ATTRIBUTE_PAIRS:
                        hits.append(f"{owner.id}.{func.attr}")
                    if owner.id in {"subprocess"} and any(
                        keyword.arg == "shell"
                        and isinstance(keyword.value, ast.Constant)
                        and keyword.value.value is True
                        for keyword in node.keywords
                    ):
                        hits.append("subprocess(shell enabled)")
                if func.attr in self.FORBIDDEN_MAGIC_ATTRIBUTES:
                    hits.append(func.attr)
        return sorted(set(hits))

    def unexpected_imports(self) -> set[str]:
        roots: set[str] = set()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    roots.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0 and node.module:
                    roots.add(node.module.split(".")[0])
        return {root for root in roots if root not in self.ALLOWED_IMPORT_ROOTS}

    def hardcoded_secret_hits(self) -> list[str]:
        return sorted(
            label
            for label, pattern in self.SECRET_PATTERNS
            if pattern.search(self.source)
        )

    def uses_constant_time_compare(self) -> bool:
        for node in ast.walk(self.tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if (
                isinstance(func, ast.Attribute)
                and func.attr == "compare_digest"
                and isinstance(func.value, ast.Name)
                and func.value.id == "hmac"
            ):
                return True
        return False


def build_audit_report(source: str) -> dict[str, Any]:
    """Build a deterministic, reproducible audit report for a candidate module."""
    harness = SecurityAuditHarness(source)
    audit = RedTeamAuditor.audit_code(source)
    return {
        "source_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
        "syntax_valid": harness.syntax_valid,
        "risk_level": audit["risk_level"],
        "security_score": audit["security_score"],
        "findings_count": audit["findings_count"],
        "high_severity_findings": len(harness.high_severity_findings()),
        "forbidden_calls": harness.forbidden_calls(),
        "unexpected_imports": sorted(harness.unexpected_imports()),
        "hardcoded_secrets": harness.hardcoded_secret_hits(),
        "constant_time_compare": harness.uses_constant_time_compare(),
        "verification_criteria": dict(sorted(VERIFICATION_CRITERIA.items())),
    }


class RecordingDelivery:
    """Deterministic async sink that can simulate transient failures."""

    def __init__(self, failures_before_success: int = 0) -> None:
        self.failures_before_success = failures_before_success
        self.attempts = 0
        self.events: list[CrossChainEvent] = []

    async def __call__(self, event: CrossChainEvent) -> None:
        self.attempts += 1
        if self.attempts <= self.failures_before_success:
            raise RuntimeError("simulated destination chain failure")
        self.events.append(event)


class TestCrossChainEventRelayer(unittest.TestCase):
    SOURCE = "ethereum-sepolia"
    DESTINATION = "base-sepolia"
    SECRET = b"unit-test-relayer-shared-secret-material"
    POLICY = RelayerPolicy(
        allowed_chains=frozenset({SOURCE, DESTINATION}),
        min_confirmations=2,
        max_event_age_seconds=120.0,
        max_future_skew_seconds=10.0,
        max_payload_bytes=2048,
        max_delivery_attempts=3,
        retry_base_delay_seconds=0.0,
        max_queue_size=8,
    )

    def _event(self, **overrides: Any) -> CrossChainEvent:
        values: dict[str, Any] = {
            "event_id": "evt-0001",
            "source_chain": self.SOURCE,
            "destination_chain": self.DESTINATION,
            "nonce": 1,
            "payload": {"amount": 42, "asset": "USDC"},
            "confirmations": 2,
        }
        values.update(overrides)
        return build_event(self.SECRET, **values)

    def _relayer(
        self,
        delivery: RecordingDelivery,
        policy: RelayerPolicy | None = None,
        secrets: dict[str, bytes] | None = None,
    ) -> AsyncCrossChainEventRelayer:
        return AsyncCrossChainEventRelayer(
            policy or self.POLICY,
            secrets if secrets is not None else {self.SOURCE: self.SECRET},
            delivery,
        )

    def test_valid_event_is_accepted_delivered_and_counted(self):
        async def scenario():
            delivery = RecordingDelivery()
            relayer = self._relayer(delivery)
            accepted = await relayer.submit(self._event())
            processed = await relayer.run_until_idle()
            return accepted, processed, delivery, relayer.stats

        accepted, processed, delivery, stats = asyncio.run(scenario())
        self.assertTrue(accepted)
        self.assertEqual(processed, 1)
        self.assertEqual([event.event_id for event in delivery.events], ["evt-0001"])
        self.assertEqual(stats["accepted"], 1)
        self.assertEqual(stats["delivered"], 1)
        self.assertEqual(stats["failed"], 0)
        self.assertEqual(stats["rejected"], 0)

    def test_tampered_signature_is_rejected_before_delivery(self):
        async def scenario():
            delivery = RecordingDelivery()
            relayer = self._relayer(delivery)
            tampered = replace(self._event(), signature="0" * 64)
            with self.assertRaises(SignatureVerificationError):
                await relayer.submit(tampered)
            await relayer.run_until_idle()
            return delivery, relayer.stats

        delivery, stats = asyncio.run(scenario())
        self.assertEqual(delivery.events, [])
        self.assertEqual(stats["accepted"], 0)
        self.assertEqual(stats["rejected"], 1)

    def test_tampered_payload_is_rejected(self):
        async def scenario():
            delivery = RecordingDelivery()
            relayer = self._relayer(delivery)
            original = self._event()
            tampered = replace(original, payload={"amount": 4200, "asset": "USDC"})
            with self.assertRaises(SignatureVerificationError):
                await relayer.submit(tampered)
            return delivery

        self.assertEqual(asyncio.run(scenario()).events, [])

    def test_signature_is_deterministic_across_key_order(self):
        timestamp = time.time()
        first = build_event(
            self.SECRET,
            event_id="evt-canonical",
            source_chain=self.SOURCE,
            destination_chain=self.DESTINATION,
            nonce=1,
            payload={"amount": 42, "asset": "USDC", "meta": {"b": 2, "a": 1}},
            confirmations=2,
            timestamp=timestamp,
        )
        second = build_event(
            self.SECRET,
            event_id="evt-canonical",
            source_chain=self.SOURCE,
            destination_chain=self.DESTINATION,
            nonce=1,
            payload={"meta": {"a": 1, "b": 2}, "asset": "USDC", "amount": 42},
            confirmations=2,
            timestamp=timestamp,
        )
        self.assertEqual(first.signing_bytes(), second.signing_bytes())
        self.assertEqual(first.signature, second.signature)
        self.assertRegex(first.signature, r"^[0-9a-f]{64}$")

    def test_non_lowercase_hex_signature_is_rejected(self):
        async def scenario():
            delivery = RecordingDelivery()
            relayer = self._relayer(delivery)
            event = replace(self._event(event_id="evt-bad-hex"), signature="A" * 64)
            with self.assertRaises(EventValidationError):
                await relayer.submit(event)
            return delivery

        self.assertEqual(asyncio.run(scenario()).events, [])

    def test_duplicate_event_id_is_rejected(self):
        async def scenario():
            delivery = RecordingDelivery()
            relayer = self._relayer(delivery)
            event = self._event()
            await relayer.submit(event)
            with self.assertRaises(ReplayDetectedError):
                await relayer.submit(event)
            await relayer.run_until_idle()
            return delivery, relayer.stats

        delivery, stats = asyncio.run(scenario())
        self.assertEqual(len(delivery.events), 1)
        self.assertEqual(stats["accepted"], 1)
        self.assertEqual(stats["rejected"], 1)

    def test_regressed_nonce_is_rejected(self):
        async def scenario():
            delivery = RecordingDelivery()
            relayer = self._relayer(delivery)
            await relayer.submit(self._event(event_id="evt-0001", nonce=5))
            with self.assertRaises(ReplayDetectedError):
                await relayer.submit(self._event(event_id="evt-0002", nonce=5))
            return delivery

        self.assertEqual(asyncio.run(scenario()).events, [])

    def test_expired_event_is_rejected(self):
        async def scenario():
            delivery = RecordingDelivery()
            relayer = self._relayer(delivery)
            expired = self._event(event_id="evt-expired", timestamp=time.time() - 600)
            with self.assertRaises(EventValidationError):
                await relayer.submit(expired)
            return delivery

        self.assertEqual(asyncio.run(scenario()).events, [])

    def test_future_dated_event_is_rejected(self):
        async def scenario():
            delivery = RecordingDelivery()
            relayer = self._relayer(delivery)
            future = self._event(event_id="evt-future", timestamp=time.time() + 120)
            with self.assertRaises(EventValidationError):
                await relayer.submit(future)
            return delivery

        self.assertEqual(asyncio.run(scenario()).events, [])

    def test_non_finite_timestamp_is_rejected(self):
        async def scenario():
            delivery = RecordingDelivery()
            relayer = self._relayer(delivery)
            event = replace(self._event(event_id="evt-nan"), timestamp=float("nan"))
            with self.assertRaises(EventValidationError):
                await relayer.submit(event)
            return delivery

        self.assertEqual(asyncio.run(scenario()).events, [])

    def test_untrusted_chain_is_rejected(self):
        async def scenario():
            delivery = RecordingDelivery()
            relayer = self._relayer(delivery)
            event = self._event(event_id="evt-untrusted", destination_chain="solana-mainnet")
            with self.assertRaises(EventValidationError):
                await relayer.submit(event)
            return delivery

        self.assertEqual(asyncio.run(scenario()).events, [])

    def test_same_chain_event_is_rejected(self):
        async def scenario():
            delivery = RecordingDelivery()
            relayer = self._relayer(delivery)
            event = self._event(event_id="evt-same-chain", destination_chain=self.SOURCE)
            with self.assertRaises(EventValidationError):
                await relayer.submit(event)
            return delivery

        self.assertEqual(asyncio.run(scenario()).events, [])

    def test_insufficient_finality_is_rejected(self):
        async def scenario():
            delivery = RecordingDelivery()
            relayer = self._relayer(delivery)
            event = self._event(event_id="evt-low-finality", confirmations=1)
            with self.assertRaises(FinalityError):
                await relayer.submit(event)
            return delivery

        self.assertEqual(asyncio.run(scenario()).events, [])

    def test_oversized_payload_is_rejected(self):
        async def scenario():
            delivery = RecordingDelivery()
            relayer = self._relayer(delivery)
            event = self._event(event_id="evt-oversized", payload={"blob": "x" * 4096})
            with self.assertRaises(EventValidationError):
                await relayer.submit(event)
            return delivery

        self.assertEqual(asyncio.run(scenario()).events, [])

    def test_non_canonical_payload_is_rejected_at_build(self):
        with self.assertRaises(EventValidationError):
            self._event(event_id="evt-non-canonical", payload={"blob": {1, 2, 3}})
        with self.assertRaises(EventValidationError):
            self._event(event_id="evt-nan-payload", payload={"amount": float("nan")})

    def test_nonce_outside_uint64_is_rejected(self):
        async def scenario():
            delivery = RecordingDelivery()
            relayer = self._relayer(delivery)
            event = replace(self._event(event_id="evt-big-nonce"), nonce=1 << 64)
            with self.assertRaises(EventValidationError):
                await relayer.submit(event)
            return delivery

        self.assertEqual(asyncio.run(scenario()).events, [])

    def test_boolean_nonce_is_rejected(self):
        async def scenario():
            delivery = RecordingDelivery()
            relayer = self._relayer(delivery)
            event = replace(self._event(event_id="evt-bool-nonce"), nonce=True)
            with self.assertRaises(EventValidationError):
                await relayer.submit(event)
            return delivery

        self.assertEqual(asyncio.run(scenario()).events, [])

    def test_event_id_length_is_bounded(self):
        async def scenario():
            delivery = RecordingDelivery()
            relayer = self._relayer(delivery)
            event = self._event(event_id="e" * 129)
            with self.assertRaises(EventValidationError):
                await relayer.submit(event)
            return delivery

        self.assertEqual(asyncio.run(scenario()).events, [])

    def test_empty_secret_material_is_rejected(self):
        with self.assertRaises(EventValidationError):
            compute_signature(b"", b"event-body")
        with self.assertRaises(EventValidationError):
            self._relayer(RecordingDelivery(), secrets={self.SOURCE: b""})

    def test_policy_rejects_invalid_limits(self):
        invalid_overrides = (
            {"allowed_chains": frozenset()},
            {"min_confirmations": -1},
            {"min_confirmations": True},
            {"max_delivery_attempts": 0},
            {"max_queue_size": 0},
            {"max_payload_bytes": 0},
            {"max_event_age_seconds": 0},
            {"max_future_skew_seconds": -1},
            {"retry_base_delay_seconds": -1},
        )
        for overrides in invalid_overrides:
            with self.assertRaises(EventValidationError, msg=str(overrides)):
                replace(self.POLICY, **overrides)

    def test_missing_source_secret_is_rejected(self):
        async def scenario():
            delivery = RecordingDelivery()
            relayer = self._relayer(
                delivery,
                secrets={self.DESTINATION: self.SECRET},
            )
            with self.assertRaises(SignatureVerificationError):
                await relayer.submit(self._event(event_id="evt-no-secret"))
            return delivery

        self.assertEqual(asyncio.run(scenario()).events, [])

    def test_transient_delivery_failure_retries_then_succeeds(self):
        async def scenario():
            delivery = RecordingDelivery(failures_before_success=2)
            relayer = self._relayer(delivery)
            await relayer.submit(self._event(event_id="evt-retry"))
            processed = await relayer.run_until_idle()
            return processed, delivery, relayer.stats

        processed, delivery, stats = asyncio.run(scenario())
        self.assertEqual(processed, 1)
        self.assertEqual(delivery.attempts, 3)
        self.assertEqual(len(delivery.events), 1)
        self.assertEqual(stats["delivered"], 1)
        self.assertEqual(stats["failed"], 0)
        self.assertEqual(stats["delivery_attempts"], 3)
        self.assertEqual(stats["retry_attempts"], 2)

    def test_delivery_exhaustion_is_counted(self):
        async def scenario():
            delivery = RecordingDelivery(failures_before_success=5)
            relayer = self._relayer(delivery)
            await relayer.submit(self._event(event_id="evt-exhausted"))
            processed = await relayer.run_until_idle()
            return processed, delivery, relayer.stats

        processed, delivery, stats = asyncio.run(scenario())
        self.assertEqual(processed, 1)
        self.assertEqual(delivery.attempts, 3)
        self.assertEqual(delivery.events, [])
        self.assertEqual(stats["delivered"], 0)
        self.assertEqual(stats["failed"], 1)
        self.assertEqual(stats["retry_attempts"], 2)

    def test_source_ordering_is_preserved(self):
        async def scenario():
            delivery = RecordingDelivery()
            relayer = self._relayer(delivery)
            for nonce in range(1, 6):
                await relayer.submit(
                    self._event(
                        event_id=f"evt-{nonce:04d}",
                        nonce=nonce,
                        payload={"sequence": nonce},
                    )
                )
            await relayer.run_until_idle()
            return delivery

        delivery = asyncio.run(scenario())
        self.assertEqual([event.nonce for event in delivery.events], [1, 2, 3, 4, 5])

    def test_bounded_queue_applies_backpressure(self):
        async def scenario():
            delivery = RecordingDelivery()
            policy = replace(self.POLICY, max_queue_size=1)
            relayer = self._relayer(delivery, policy=policy)
            first = self._event(event_id="evt-0001", nonce=1)
            second = self._event(event_id="evt-0002", nonce=2)

            await relayer.submit(first)
            blocked = asyncio.create_task(relayer.submit(second))
            await asyncio.sleep(0)
            self.assertFalse(blocked.done())

            await relayer.run_until_idle()
            await asyncio.wait_for(blocked, timeout=1.0)
            await relayer.run_until_idle()
            return delivery

        delivery = asyncio.run(scenario())
        self.assertEqual([event.event_id for event in delivery.events], ["evt-0001", "evt-0002"])


class TestSecurityAuditHarness(unittest.TestCase):
    def setUp(self):
        self.harness = SecurityAuditHarness(RELAYER_SOURCE)

    def test_sandbox_redteam_audit_has_zero_high_severity_findings(self):
        high_findings = self.harness.high_severity_findings()
        self.assertEqual(high_findings, [], msg=f"High-severity findings: {high_findings}")

    def test_ast_validates_and_required_contract_exists(self):
        tree = ast.parse(RELAYER_SOURCE)
        self.assertIsNotNone(ast.get_docstring(tree))

        class_names = {
            node.name for node in tree.body if isinstance(node, ast.ClassDef)
        }
        self.assertTrue(
            {"CrossChainEvent", "RelayerPolicy", "AsyncCrossChainEventRelayer"}.issubset(
                class_names
            )
        )

        function_names = {
            node.name
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        self.assertIn("build_event", function_names)

        relayer_class = next(
            node
            for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == "AsyncCrossChainEventRelayer"
        )
        async_methods = {
            node.name
            for node in relayer_class.body
            if isinstance(node, ast.AsyncFunctionDef)
        }
        self.assertTrue({"submit", "process_once", "run_until_idle", "run"}.issubset(async_methods))

    def test_no_dynamic_code_execution(self):
        self.assertEqual(self.harness.forbidden_calls(), [])

    def test_imports_are_least_privilege(self):
        self.assertEqual(self.harness.unexpected_imports(), set())

    def test_no_hardcoded_credentials_or_secrets(self):
        self.assertEqual(self.harness.hardcoded_secret_hits(), [])

    def test_uses_constant_time_signature_comparison(self):
        self.assertTrue(self.harness.uses_constant_time_compare())

    def test_harness_detects_deliberately_vulnerable_candidate(self):
        candidate = "\n".join(
            [
                "import os",
                "import subprocess",
                "",
                "def run(command):",
                "    os." + "system(command)",
                "    subprocess.run(command, shell" + "=True)",
                "    return ev" + "al(command)",
            ]
        )
        harness = SecurityAuditHarness(candidate)
        self.assertGreaterEqual(len(harness.high_severity_findings()), 3)
        self.assertTrue(harness.forbidden_calls())
        self.assertIn("os", harness.unexpected_imports())
        self.assertIn("subprocess", harness.unexpected_imports())

    def test_audit_report_is_reproducible_and_clean(self):
        first = build_audit_report(RELAYER_SOURCE)
        second = build_audit_report(RELAYER_SOURCE)

        self.assertEqual(first, second)
        self.assertTrue(first["syntax_valid"])
        self.assertEqual(first["high_severity_findings"], 0)
        self.assertIn(first["risk_level"], {"SAFE", "MEDIUM"})
        self.assertGreaterEqual(first["security_score"], 70)
        self.assertEqual(first["forbidden_calls"], [])
        self.assertEqual(first["unexpected_imports"], [])
        self.assertEqual(first["hardcoded_secrets"], [])
        self.assertTrue(first["constant_time_compare"])


class TestVerificationCoverage(unittest.TestCase):
    def _test_classes(self):
        return (
            TestCrossChainEventRelayer,
            TestSecurityAuditHarness,
            TestVerificationCoverage,
        )

    def _available_tests(self) -> set[str]:
        available = set()
        for test_class in self._test_classes():
            for name in dir(test_class):
                if name.startswith("test_"):
                    available.add(f"{test_class.__name__}.{name}")
        return available

    def test_every_verification_criterion_maps_to_a_real_test(self):
        available = self._available_tests()
        missing = sorted(
            target
            for target in VERIFICATION_CRITERIA.values()
            if target not in available
        )
        self.assertEqual(missing, [], msg=f"Criteria reference missing tests: {missing}")

    def test_every_test_is_registered_as_a_verification_criterion(self):
        registered = set(VERIFICATION_CRITERIA.values())
        unregistered = sorted(
            target for target in self._available_tests() if target not in registered
        )
        self.assertEqual(
            unregistered,
            [],
            msg=f"Tests missing a verification criterion: {unregistered}",
        )


if __name__ == "__main__":
    unittest.main()
