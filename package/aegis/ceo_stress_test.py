"""AegisBrain Y-Combinator CEO Ideation & Stress-Testing Module.

Critically analyzes product ideas, technical proposals, and startup concepts using
the battle-tested Y-Combinator / Founder diagnostic framework:
1. Hair-on-Fire Problem Identification (urgent daily pain vs vitamin)
2. 10x Unfair Advantage & Secret Insight
3. "Why Now?" Inflection Point
4. Distribution Velocity & Zero-Friction Onboarding
5. Top 3 Fatal Failure Modes & Kill-Criteria
6. 24-Hour Minimal Verifiable MVP
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class CEOCritique:
    idea_summary: str
    feasibility_score: int  # 1-10
    risk_level: str         # "Low", "Medium", "High", "Critical"
    urgent_pain_assessment: str
    why_now_inflection: str
    unfair_advantage: str
    fatal_failure_modes: List[str]
    smallest_verifiable_mvp: str
    strategic_verdict: str
    actionable_next_steps: List[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        failures_md = "\n".join(f"- ⚠️ **Risk {i+1}**: {f}" for i, f in enumerate(self.fatal_failure_modes))
        steps_md = "\n".join(f"{i+1}. {step}" for i, step in enumerate(self.actionable_next_steps))

        return f"""
# 🏢 YC CEO Ideation & Stress-Test Report

**Concept Analyzed**: `{self.idea_summary}`
**Feasibility Score**: `{self.feasibility_score}/10` &bull; **Risk Rating**: `{self.risk_level}`

---

### 1. Hair-on-Fire Problem Assessment
{self.urgent_pain_assessment}

### 2. "Why Now?" Inflection Point
{self.why_now_inflection}

### 3. Unfair Advantage & Competitive Moat
{self.unfair_advantage}

### 4. Fatal Failure Modes (Why This Could Die)
{failures_md}

### 5. 24-Hour Smallest Verifiable MVP
🎯 **Core Milestone**: {self.smallest_verifiable_mvp}

### 6. Strategic Executive Verdict
💡 **{self.strategic_verdict}**

#### Immediate Action Items
{steps_md}
""".strip()


class YCCEOStressTester:
    """Stress-tests software concepts and architectures against YC founder heuristics."""

    @classmethod
    def evaluate(cls, idea: str, context: Optional[str] = None) -> CEOCritique:
        idea_lower = idea.lower()

        # Heuristic detection for common domains
        is_extension = any(k in idea_lower for k in ["extension", "plugin", "browser", "chrome", "brave"])
        is_leetcode = any(k in idea_lower for k in ["leetcode", "dsa", "coding interview", "solutions"])
        is_agent = any(k in idea_lower for k in ["agent", "cli", "ai assistant", "aegis", "bot"])
        is_database = any(k in idea_lower for k in ["database", "postgres", "sql", "sync", "storage"])

        # Determine scores and targeted critiques
        if is_leetcode and is_extension:
            return CEOCritique(
                idea_summary=idea,
                feasibility_score=9,
                risk_level="Low",
                urgent_pain_assessment=(
                    "High frequency, acute pain point. Serious software engineers solve 3-5 LeetCode problems "
                    "daily during interview prep. Existing marketplace extensions are either abandoned, broken by "
                    "LeetCode DOM changes, or demand recurring subscriptions for basic GitHub sync. Direct client-side "
                    "sync into date-versioned problem packages completely eliminates manual copy-paste friction."
                ),
                why_now_inflection=(
                    "Modern browsers enforce Manifest V3 service workers, breaking old declarative webRequest extensions. "
                    "An interception model hooking fetch/XHR in the MAIN world reliably parses GraphQL submission "
                    "payloads regardless of visual DOM obfuscation."
                ),
                unfair_advantage=(
                    "Zero external infrastructure costs (100% direct GitHub REST API), transparent client-side code, "
                    "and multi-solution date preservation (preventing overwrites when optimizing 5% beats to 95% beats)."
                ),
                fatal_failure_modes=[
                    "LeetCode GraphQL schema or submission endpoint migration breaks payload extraction.",
                    "GitHub API rate limits on Personal Access Tokens if batch syncing excessive files.",
                    "Windows NTFS path sanitization failures on filenames containing colons or illegal chars."
                ],
                smallest_verifiable_mvp=(
                    "A Manifest V3 extension with in-page fetch interception that automatically commits a solved problem "
                    "into `problems/<0000-slug>/Solution_<date>.java` on `leetcode.com` submit click."
                ),
                strategic_verdict=(
                    "GREENLIGHT. Clear utility, zero cloud cost, immediate portfolio utility, and high viral shareability "
                    "among collegiate and competitive programming communities."
                ),
                actionable_next_steps=[
                    "Test unpacked in Brave/Chrome on 3 distinct difficulty problems.",
                    "Verify file naming prevents collisions when multiple submissions occur on the same day.",
                    "Ensure GitHub PAT setup guide in README has zero friction."
                ]
            )

        if is_agent:
            return CEOCritique(
                idea_summary=idea,
                feasibility_score=8,
                risk_level="Medium",
                urgent_pain_assessment=(
                    "AI coding agents often hallucinate passes, agree sycophantically with flawed prompts, "
                    "and lack historical memory across restarts. A local agent that learns from past errors "
                    "and enforces objective verification solves real engineering fatigue."
                ),
                why_now_inflection=(
                    "Local reasoning models and function-calling APIs allow sub-second, zero-cost verification loops "
                    "running entirely on user workstations (e.g. drive P:\\)."
                ),
                unfair_advantage=(
                    "Coupling sub-second SQLite FTS5 memory + AST graph indexing + anti-sycophancy verification guards "
                    "yields 90% fewer tokens consumed than traditional web search and file dumping."
                ),
                fatal_failure_modes=[
                    "Agent context window bloat if session transcripts are loaded unpruned.",
                    "Over-engineering: building too many layers before simple CLI commands work reliably.",
                    "Platform lock-in: failing to support Windows PowerShell and Linux paths interchangeably."
                ],
                smallest_verifiable_mvp=(
                    "A standalone CLI tool (`aegis`) that executes pre-flight checks, creates instant config snapshots, "
                    "and records mistakes in a local SQLite ledger."
                ),
                strategic_verdict=(
                    "PROCEED WITH DISCIPLINE. Keep worker modules decoupled and avoid premature distributed orchestration."
                ),
                actionable_next_steps=[
                    "Enforce strict 400-token active bootstrap limit.",
                    "Implement the Anti-Sycophancy Verification Protocol to challenge flawed code before running.",
                    "Add automated snapshot recovery reflex before modifying host configs."
                ]
            )

        # General Software / Tech Idea Stress-Test
        return CEOCritique(
            idea_summary=idea,
            feasibility_score=7,
            risk_level="Medium",
            urgent_pain_assessment=(
                "Evaluate whether target users are actively seeking a workaround today. If users are not currently "
                "losing time or money dealing with this friction manually, the product risks being a 'nice-to-have'."
            ),
            why_now_inflection=(
                "Identify the exact technical or regulatory shift that occurred in the last 12-24 months enabling this solution."
            ),
            unfair_advantage=(
                "Must possess proprietary data, superior speed/cost economics, or distribution advantage to survive clones."
            ),
            fatal_failure_modes=[
                "User churn due to high setup friction or required credential configurations.",
                "High ongoing operating costs outpacing perceived value.",
                "Lack of verifiable feedback loops to prove objective correctness."
            ],
            smallest_verifiable_mvp=(
                "Build the thinnest end-to-end slice that solves the core loop for 1 user in < 5 minutes."
            ),
            strategic_verdict="PROCEED TO TECHNICAL VALIDATION WITH SPECIFIED MILESTONES.",
            actionable_next_steps=[
                "Define 3 non-negotiable success criteria prior to implementation.",
                "Confirm local dependencies and avoid heavy third-party SaaS integrations.",
                "Build automated integration tests covering the critical happy path and top 2 failure edges."
            ]
        )
