"""Async cross-chain event relayer with integrity, replay, and finality guards.

The relayer accepts signed events from an allowlisted source chain and delivers
them to an allowlisted destination chain through an injected async transport.
It is intentionally dependency-free so it can run inside the Aegis sandbox.

Security properties enforced before an event may be queued:
- Allowlisted source and destination chain identifiers.
- Canonical JSON serialization with HMAC-SHA256 signatures.
- Constant-time signature comparison.
- Strict freshness window plus bounded future clock skew.
- Monotonic nonce and event-id replay protection per source chain.
- Minimum finality confirmations.
- Bounded payload size and bounded in-memory queue.
"""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import math
import time
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass
from typing import Any

MAX_PAYLOAD_BYTES = 65_536
SIGNATURE_HEX_LENGTH = 64
MAX_EVENT_ID_LENGTH = 128
MAX_NONCE = (1 << 64) - 1

_HEX_DIGITS = frozenset("0123456789abcdef")


class RelayerError(Exception):
    """Base class for relayer failures."""


class EventValidationError(RelayerError, ValueError):
    """Raised when an event fails structural or policy validation."""


class SignatureVerificationError(EventValidationError):
    """Raised when an event signature does not match its canonical body."""


class ReplayDetectedError(EventValidationError):
    """Raised when an event id or nonce was already consumed."""


class FinalityError(EventValidationError):
    """Raised when an event has fewer confirmations than policy requires."""


class DeliveryExhaustedError(RelayerError):
    """Raised when every delivery attempt for an event failed."""


def _is_plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_finite_number(value: Any) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return math.isfinite(float(value))


@dataclass(frozen=True)
class CrossChainEvent:
    """Immutable event envelope exchanged between two chains."""

    event_id: str
    source_chain: str
    destination_chain: str
    nonce: int
    payload: Mapping[str, Any]
    signature: str
    timestamp: float
    confirmations: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.payload, Mapping):
            raise EventValidationError("event payload must be a mapping")
        object.__setattr__(self, "payload", dict(self.payload))

    def canonical_body(self) -> dict[str, Any]:
        """Return the exact body covered by the event signature."""
        return {
            "destination_chain": self.destination_chain,
            "event_id": self.event_id,
            "nonce": self.nonce,
            "payload": self.payload,
            "source_chain": self.source_chain,
            "timestamp": self.timestamp,
        }

    def signing_bytes(self) -> bytes:
        """Return canonical bytes for signature creation and verification."""
        try:
            encoded = json.dumps(
                self.canonical_body(),
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=True,
                allow_nan=False,
            )
        except (TypeError, ValueError) as exc:
            raise EventValidationError("event body is not canonical JSON") from exc
        return encoded.encode("utf-8")


def compute_signature(secret: bytes | str, signing_bytes: bytes) -> str:
    """Compute a hex HMAC-SHA256 signature over canonical event bytes."""
    if isinstance(secret, str):
        key = secret.encode("utf-8")
    elif isinstance(secret, (bytes, bytearray)):
        key = bytes(secret)
    else:
        raise TypeError("relayer secret must be bytes or text")
    if not key:
        raise EventValidationError("relayer secret must not be empty")
    if not isinstance(signing_bytes, (bytes, bytearray)):
        raise TypeError("signing input must be bytes")
    return hmac.new(key, bytes(signing_bytes), hashlib.sha256).hexdigest()


def build_event(
    secret: bytes | str,
    *,
    event_id: str,
    source_chain: str,
    destination_chain: str,
    nonce: int,
    payload: Mapping[str, Any],
    timestamp: float | None = None,
    confirmations: int = 0,
) -> CrossChainEvent:
    """Construct a correctly signed event for a configured source chain."""
    event = CrossChainEvent(
        event_id=event_id,
        source_chain=source_chain,
        destination_chain=destination_chain,
        nonce=nonce,
        payload=payload,
        signature="",
        timestamp=time.time() if timestamp is None else timestamp,
        confirmations=confirmations,
    )
    signature = compute_signature(secret, event.signing_bytes())
    return CrossChainEvent(
        event_id=event.event_id,
        source_chain=event.source_chain,
        destination_chain=event.destination_chain,
        nonce=event.nonce,
        payload=event.payload,
        signature=signature,
        timestamp=event.timestamp,
        confirmations=event.confirmations,
    )


@dataclass(frozen=True)
class RelayerPolicy:
    """Fail-closed policy applied to every inbound event."""

    allowed_chains: frozenset[str]
    min_confirmations: int = 1
    max_event_age_seconds: float = 300.0
    max_future_skew_seconds: float = 30.0
    max_payload_bytes: int = MAX_PAYLOAD_BYTES
    max_delivery_attempts: int = 3
    retry_base_delay_seconds: float = 0.05
    max_queue_size: int = 128

    def __post_init__(self) -> None:
        chains = frozenset(self.allowed_chains)
        if not chains or any(not isinstance(c, str) or not c for c in chains):
            raise EventValidationError("allowed_chains must contain non-empty chain ids")
        object.__setattr__(self, "allowed_chains", chains)
        if not _is_plain_int(self.min_confirmations) or self.min_confirmations < 0:
            raise EventValidationError("min_confirmations must be a non-negative integer")
        if not _is_plain_int(self.max_delivery_attempts) or self.max_delivery_attempts < 1:
            raise EventValidationError("max_delivery_attempts must be at least one")
        if not _is_plain_int(self.max_queue_size) or self.max_queue_size < 1:
            raise EventValidationError("max_queue_size must be at least one")
        if not _is_plain_int(self.max_payload_bytes) or self.max_payload_bytes < 1:
            raise EventValidationError("max_payload_bytes must be at least one")
        if not _is_finite_number(self.max_event_age_seconds) or self.max_event_age_seconds <= 0:
            raise EventValidationError("max_event_age_seconds must be positive")
        if not _is_finite_number(self.max_future_skew_seconds) or self.max_future_skew_seconds < 0:
            raise EventValidationError("max_future_skew_seconds must be non-negative")
        if not _is_finite_number(self.retry_base_delay_seconds) or self.retry_base_delay_seconds < 0:
            raise EventValidationError("retry_base_delay_seconds must be non-negative")


class AsyncCrossChainEventRelayer:
    """Validate, queue, and deliver signed cross-chain events in FIFO order."""

    def __init__(
        self,
        policy: RelayerPolicy,
        secrets: Mapping[str, bytes | str],
        deliver: Callable[[CrossChainEvent], Awaitable[None]],
        *,
        wall_clock: Callable[[], float] = time.time,
    ) -> None:
        if not isinstance(policy, RelayerPolicy):
            raise TypeError("policy must be a RelayerPolicy")
        if not callable(deliver):
            raise TypeError("deliver must be an async callable")
        if not callable(wall_clock):
            raise TypeError("wall_clock must be callable")

        material: dict[str, bytes] = {}
        for chain, secret in secrets.items():
            if not isinstance(chain, str) or not chain:
                raise EventValidationError("secret chain ids must be non-empty strings")
            if isinstance(secret, str):
                key = secret.encode("utf-8")
            elif isinstance(secret, (bytes, bytearray)):
                key = bytes(secret)
            else:
                raise TypeError("relayer secrets must be bytes or text")
            if not key:
                raise EventValidationError("relayer secrets must not be empty")
            material[chain] = key

        self._policy = policy
        self._secrets = material
        self._deliver = deliver
        self._wall_clock = wall_clock
        self._queue: asyncio.Queue[CrossChainEvent] = asyncio.Queue(maxsize=policy.max_queue_size)
        self._seen: set[tuple[str, str]] = set()
        self._last_nonce: dict[str, int] = {}
        self._stats: dict[str, int] = {
            "accepted": 0,
            "rejected": 0,
            "delivered": 0,
            "failed": 0,
            "delivery_attempts": 0,
            "retry_attempts": 0,
        }

    @property
    def policy(self) -> RelayerPolicy:
        return self._policy

    @property
    def pending(self) -> int:
        return self._queue.qsize()

    @property
    def stats(self) -> dict[str, int]:
        return dict(self._stats)

    async def submit(self, event: CrossChainEvent) -> bool:
        """Validate and enqueue one event. Raises on any failed guard."""
        if not isinstance(event, CrossChainEvent):
            raise EventValidationError("submit expects a CrossChainEvent")

        try:
            self._validate_policy(event)
            self._verify_signature(event)
            previous_nonce = self._reserve(event)
        except RelayerError:
            self._stats["rejected"] += 1
            raise

        try:
            await self._queue.put(event)
        except BaseException:
            self._seen.discard((event.source_chain, event.event_id))
            if previous_nonce is None:
                self._last_nonce.pop(event.source_chain, None)
            else:
                self._last_nonce[event.source_chain] = previous_nonce
            raise

        self._stats["accepted"] += 1
        return True

    async def process_once(self) -> CrossChainEvent | None:
        """Process a single queued event, returning it when one was handled."""
        if self._queue.empty():
            return None
        event = await self._queue.get()
        try:
            await self._handle(event)
            return event
        finally:
            self._queue.task_done()

    async def run_until_idle(self) -> int:
        """Drain the queue and return the number of processed events."""
        processed = 0
        while not self._queue.empty():
            event = await self.process_once()
            if event is not None:
                processed += 1
        return processed

    async def run(self, stop_event: asyncio.Event) -> None:
        """Consume events until the supplied stop event is set."""
        while not stop_event.is_set():
            try:
                event = await asyncio.wait_for(self._queue.get(), timeout=0.05)
            except asyncio.TimeoutError:
                continue
            try:
                await self._handle(event)
            finally:
                self._queue.task_done()

    async def _handle(self, event: CrossChainEvent) -> None:
        try:
            await self._deliver_with_retry(event)
            self._stats["delivered"] += 1
        except DeliveryExhaustedError:
            self._stats["failed"] += 1

    async def _deliver_with_retry(self, event: CrossChainEvent) -> None:
        attempts = 0
        while attempts < self._policy.max_delivery_attempts:
            attempts += 1
            self._stats["delivery_attempts"] += 1
            try:
                await self._deliver(event)
                return
            except asyncio.CancelledError:
                raise
            except Exception:
                if attempts >= self._policy.max_delivery_attempts:
                    raise DeliveryExhaustedError(
                        f"delivery exhausted for event {event.event_id} after {attempts} attempts"
                    ) from None
                self._stats["retry_attempts"] += 1
                delay = self._policy.retry_base_delay_seconds * (2 ** (attempts - 1))
                if delay > 0:
                    await asyncio.sleep(delay)

    def _validate_policy(self, event: CrossChainEvent) -> None:
        if not isinstance(event.event_id, str) or not event.event_id:
            raise EventValidationError("event_id must be a non-empty string")
        if len(event.event_id) > MAX_EVENT_ID_LENGTH:
            raise EventValidationError("event_id exceeds the maximum length")

        for label, value in (
            ("source_chain", event.source_chain),
            ("destination_chain", event.destination_chain),
        ):
            if not isinstance(value, str) or not value:
                raise EventValidationError(f"{label} must be a non-empty string")
        if event.source_chain == event.destination_chain:
            raise EventValidationError("source and destination chains must differ")
        for chain in (event.source_chain, event.destination_chain):
            if chain not in self._policy.allowed_chains:
                raise EventValidationError(f"chain is not allowlisted: {chain}")

        if not _is_plain_int(event.nonce) or event.nonce < 0 or event.nonce > MAX_NONCE:
            raise EventValidationError("nonce must be an unsigned 64-bit integer")
        if not _is_plain_int(event.confirmations) or event.confirmations < 0:
            raise EventValidationError("confirmations must be a non-negative integer")
        if event.confirmations < self._policy.min_confirmations:
            raise FinalityError(
                f"event has {event.confirmations} confirmations, policy requires "
                f"{self._policy.min_confirmations}"
            )

        if not _is_finite_number(event.timestamp):
            raise EventValidationError("timestamp must be a finite number")
        now = self._wall_clock()
        if event.timestamp - now > self._policy.max_future_skew_seconds:
            raise EventValidationError("event timestamp is beyond the allowed clock skew")
        if now - event.timestamp > self._policy.max_event_age_seconds:
            raise EventValidationError("event timestamp is outside the freshness window")

        if (
            not isinstance(event.signature, str)
            or len(event.signature) != SIGNATURE_HEX_LENGTH
            or any(char not in _HEX_DIGITS for char in event.signature)
        ):
            raise EventValidationError("signature must be lowercase hex SHA-256")

        try:
            payload_size = len(
                json.dumps(
                    event.payload,
                    sort_keys=True,
                    separators=(",", ":"),
                    ensure_ascii=True,
                    allow_nan=False,
                ).encode("utf-8")
            )
        except (TypeError, ValueError) as exc:
            raise EventValidationError("event payload is not canonical JSON") from exc
        if payload_size > self._policy.max_payload_bytes:
            raise EventValidationError("event payload exceeds the maximum size")

    def _verify_signature(self, event: CrossChainEvent) -> None:
        secret = self._secrets.get(event.source_chain)
        if secret is None:
            raise SignatureVerificationError(
                f"no shared secret configured for source chain: {event.source_chain}"
            )
        expected = compute_signature(secret, event.signing_bytes())
        if not hmac.compare_digest(expected, event.signature):
            raise SignatureVerificationError("event signature verification failed")

    def _reserve(self, event: CrossChainEvent) -> int | None:
        key = (event.source_chain, event.event_id)
        if key in self._seen:
            raise ReplayDetectedError("duplicate event id for source chain")
        previous_nonce = self._last_nonce.get(event.source_chain)
        if previous_nonce is not None and event.nonce <= previous_nonce:
            raise ReplayDetectedError("nonce was already consumed for source chain")
        self._seen.add(key)
        self._last_nonce[event.source_chain] = event.nonce
        return previous_nonce


# Aliases for test compatibility
AsyncEventRelayer = AsyncCrossChainEventRelayer
ChainEvent = CrossChainEvent
