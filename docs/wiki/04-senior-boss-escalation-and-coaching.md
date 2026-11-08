# Chapter 04: Senior Boss Escalation & Coaching

This chapter specifies the supervisory feedback loop between Tier 2 Junior Bosses and Tier 3 Execution Workers, the structure of the Escalation Dossier, and the conditions under which Tier 1 Senior Boss executes an authoritative takeover.

---

## 1. Why Lower Models Require Supervision

Smaller cloud models (e.g., DeepSeek V4.1 Flash Free, Nemotron 3.5 Bolt) and local models (Qwen2.5-Coder 7B) offer rapid generation at zero token cost. However, empirical testing across hundreds of agent trajectories reveals four recurring failure modes:

1. **Algorithmic Inversion & Off-By-One Logic**: Inverting boolean conditionals, failing to handle edge cases (empty lists, null pointers, race conditions), or omitting cleanup blocks.
2. **Hallucinated Signatures & APIs**: Invoking non-existent methods or mixing syntax across different library versions.
3. **Conversational AI Slop**: Inserting pleasantries ("Sure, here is your code:", "Certainly!") or enclosing code in conversational markdown explanations where raw files were requested.
4. **Security Vulnerabilities**: Introducing dangerous patterns like `shell=True`, `os.system()`, or concatenating unvalidated inputs into SQL statements.

To harness free tokens without sacrificing engineering quality, **Tier 2 Junior Bosses act as rigorous code reviewers and coaches** before any output is accepted.

---

## 2. The Subagent Coaching Loop

When a Tier 3 Worker generates a raw candidate draft, the Tier 2 Subagent executes a structured review cycle:

```
                  ┌────────────────────────────────────────┐
                  │ Tier 3 Worker Generates Raw Code Draft │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │ Tier 2 Junior Boss Audits Draft:       │
                  │ - AST Syntax & Logic Verification      │
                  │ - 4-Gate Quality Architecture Check    │
                  └───────────────────┬────────────────────┘
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
                  [ 0 Errors Found ]       [ Flaws Detected ]
                         │                         │
                         ▼                         ▼
                 Accept Deliverable        Formulate Targeted Coaching Prompt:
                 (Proceed to Tests)        - Pinpoint line numbers & exact flaws
                                           - Re-specify strict invariants
                                                   │
                                                   ▼
                                           Re-invoke Worker CLI:
                                           `hermes chat -q "<coaching_prompt>"`
                                                   │
                                                   ▼
                                           Record error delta in brain.db
                                           (Repeat loop up to max_retries)
```

### 2.1 The Coaching Prompt Structure
A coaching prompt is strictly technical, containing zero polite filler:
```
[COACHING DIRECTIVE]
Your previous implementation of `SessionDispatcher` failed quality verification.
Identified Flaws:
1. Line 42: Used `os.system(cmd)` which violates the Red-Team Security Gate. Replace with `subprocess.run(cmd, shell=False, check=True)`.
2. Line 88: Unhandled `KeyError` when payload missing 'session_id'. Implement defensive dictionary lookup `.get('session_id')`.
3. Output contains conversational markdown preamble. Output RAW code only.

Re-implement now conforming strictly to these invariants.
```

### 2.2 Confidence & Learning Ledger (`brain.db`)
Every coaching loop records metrics into the `agent_confidence` table in `brain.db`:
- `worker_type` (e.g. `hermes`, `opencode`)
- `initial_errors` vs `final_errors`
- `retry_count`
- `score` (0.0 to 10.0 scale)

Over time, AegisBrain dynamically avoids assigning complex subtasks to workers with historical confidence scores $< 8.0$.

---

## 3. Escalation Triggers

A Subagent aborts the coaching loop and triggers an immediate escalation to Tier 1 under two strict conditions:

1. **Coaching Retries Expired (`retry_count >= max_retries`)**:
   The worker has failed to resolve architectural or logical flaws after repeated coaching attempts, indicating a fundamental cognitive reasoning barrier.
2. **Mission-Critical Task Severity (`severity == CRITICAL`)**:
   The incoming task touches cryptographic primitives, root authentication, database schema drops, or core security perimeters where any lower-model hallucination introduces unacceptable organizational risk.

---

## 4. The Escalation Dossier

Upon triggering escalation, the Tier 2 Subagent constructs an **Escalation Dossier** serialized as JSON:

```json
{
  "subagent_id": "backend-lead-01",
  "domain": "authentication_service",
  "worker_type": "hermes",
  "task_spec": "Implement PBKDF2 password hashing and constant-time token comparison",
  "escalation_reason": "Worker failed security audit after 3 coaching retries.",
  "reasoning_critique": "Worker persistently used naive string equality (==) for secret tokens instead of hmac.compare_digest, creating timing attack vectors.",
  "initial_errors": 4,
  "final_errors": 1,
  "flaws": [
    "Timing attack vulnerability on token verification",
    "Missing salt generation routine"
  ],
  "candidate_draft_path": "/tmp/aegis-brain/candidate_draft_auth.py",
  "timestamp": "2026-11-08T13:30:00Z"
}
```

The Subagent marks its internal state as `status="escalated_to_senior_boss"` and emits a high-priority message to Tier 1.

---

## 5. Senior Boss Takeover Protocol

When Tier 1 Senior Boss receives the Escalation Dossier:

1. **Strategic Assessment**: The Senior Boss ingests the worker's candidate draft and the Subagent's critique.
2. **Direct Authoring Override**: The Senior Boss bypasses lower workers and directly authors the production-grade implementation, applying high-cognition reasoning to resolve the subtle edge cases.
3. **Dual Verification**: The Senior Boss validates the code against the 4-Decision Quality Architecture Gate.
4. **Knowledge Seeding**: The root cause and correct implementation pattern are persisted into `brain.db` via `aegis remember` so future sessions recall the architectural invariant.
5. **Signed Executive Sign-Off**: The final deliverable is delivered to the user with a notation of the escalation event.
