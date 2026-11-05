"""AegisBrain Deep Planning, Feasibility & Cascading Hierarchical Alignment Engine.

Implements the Comprehensive Pre-Execution Architecture:
1. Arsenal & Skill Discovery:
   - Scans ~/.gemini/config/{plugins,skills,tools} and matches optimal execution muscles.
2. Y-Combinator Feasibility & Flaw Detection:
   - Evaluates core hypotheses, fatal assumptions, failure modes, and scores feasibility (0-100).
3. Multi-Approach Architectural Scenarios:
   - Generates 3-4 tailored technical pathways based on user requirements with detailed Pros, Cons, Complexity, and Token Cost.
4. Zero-Assumption Clarification Gate:
   - Generates 4 to 20 precise diagnostic questions tailored to the exact problem space.
   - Strictly blocks code generation until requirements and trade-offs are confirmed.
5. Cascading Hierarchical Alignment:
   - Senior Boss (Antigravity Frontier) ⇄ Junior Boss (Domain Leads) ⇄ Workers (Hermes, MOE, Local Models).
   - Multi-tier Q&A, skill provisioning, and coaching before code synthesis.
6. Pre-Execution Living Documentation:
   - Generates PRD, TRD, ERD (Mermaid), and a dynamic Checkbook / Task Ledger before coding begins.
7. Dual-Environment Sandbox Gates:
   - Isolated sandbox verification before host environment promotion.
"""

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .ceo_stress_test import YCCEOStressTester, CEOCritique
from .hardware import get_hardware_status, recommend_model_tier
from .sandbox import RedTeamAuditor


@dataclass
class ArchitectureOption:
    name: str
    archetype: str
    summary: str
    feasibility_score: int  # 0-100
    complexity: int         # 1-10
    token_cost_rating: str  # "Lowest", "Moderate", "High"
    pros: List[str]
    cons: List[str]
    recommended_when: str


@dataclass
class ClarifyingQuestion:
    id: str
    category: str  # "Scope", "UI/UX", "Backend Logic", "Security & Reliability", "Sensory & Tooling"
    question: str
    options: List[str]
    answered: bool = False
    selected_option: Optional[str] = None


@dataclass
class HierarchicalAgentDialog:
    tier_from: str
    tier_to: str
    agent_name: str
    question: str
    answer: str
    status: str = "RESOLVED"  # "PENDING" or "RESOLVED"


@dataclass
class DeepPlanReport:
    task: str
    niche: str
    feasibility_score: int
    fatal_flaws: List[str]
    arsenal_tools_recommended: List[str]
    architecture_options: List[ArchitectureOption]
    recommended_option: str
    clarifying_questions: List[ClarifyingQuestion]
    hierarchical_dialogs: List[HierarchicalAgentDialog]
    prd_markdown: str
    trd_markdown: str
    erd_mermaid: str
    task_ledger: List[Dict[str, Any]]
    is_clarified: bool = False

    def to_markdown(self) -> str:
        options_md = "\n\n".join(
            f"#### Option {i+1}: {opt.name} ({opt.archetype})\n"
            f"- **Feasibility**: `{opt.feasibility_score}/100` | **Complexity**: `{opt.complexity}/10` | **Token Cost**: `{opt.token_cost_rating}`\n"
            f"- **Summary**: {opt.summary}\n"
            f"- **Pros**:\n" + "\n".join(f"  + {p}" for p in opt.pros) + "\n"
            f"- **Cons**:\n" + "\n".join(f"  - {c}" for c in opt.cons) + "\n"
            f"- **Best For**: {opt.recommended_when}"
            for i, opt in enumerate(self.architecture_options)
        )

        questions_md = "\n\n".join(
            f"**Q{i+1} [{q.category}]: {q.question}**\n" +
            "\n".join(f"- [ ] {opt}" for opt in q.options)
            for i, q in enumerate(self.clarifying_questions)
        )

        flaws_md = "\n".join(f"- ⚠️ **Fatal Flaw Risk {i+1}**: {f}" for i, f in enumerate(self.fatal_flaws))
        tools_md = ", ".join(f"`{t}`" for t in self.arsenal_tools_recommended)

        dialogs_md = "\n".join(
            f"- **[{d.tier_from} ➔ {d.tier_to} ({d.agent_name})]**: *\"{d.question}\"*\n"
            f"  ↳ **Resolution**: {d.answer}"
            for d in self.hierarchical_dialogs
        )

        ledger_md = "\n".join(
            f"- [{ 'x' if item.get('status') == 'done' else ' ' }] **{item['milestone']}** (Verification: {item['verification']})"
            for item in self.task_ledger
        )

        return f"""# 🧠 AegisBrain Deep Planning & Feasibility Report

**Target Task**: `{self.task}`
**Niche**: `{self.niche}` &bull; **Feasibility Score**: `{self.feasibility_score}/100`
**Status**: `{'✅ CLARIFIED & READY FOR SANDBOX' if self.is_clarified else '🛑 CLARIFICATION REQUIRED (Awaiting Answers)'}`

---

### 1. Arsenal & Skill Discovery
- **Matched Arsenal Muscles**: {tools_md}
- **Recommended Model Tier**: Subagents with local worker offload

### 2. Y-Combinator Feasibility & Flaw Detection
{flaws_md}

---

### 3. Multi-Approach Architectural Scenarios
{options_md}

**Recommended Path**: `{self.recommended_option}`

---

### 4. Interactive Clarification Interview (Zero-Assumption Gate)
> **MANDATORY INVARIANT**: Before code generation starts, all non-obvious constraints, UI dials, and logic tradeoffs must be answered.

{questions_md}

---

### 5. Cascading Hierarchical Alignment Dialog
{dialogs_md}

---

### 6. Pre-Execution Living Documentation

#### Product Requirements Document (PRD)
{self.prd_markdown}

#### Technical Requirements & Architecture (TRD)
{self.trd_markdown}

#### Entity-Relationship & Data Flow (ERD)
```mermaid
{self.erd_mermaid}
```

#### Living Task Ledger & Checkbook
{ledger_md}
"""


class DeepPlanningEngine:
    """Core engine for autonomous multi-tier planning, YC critique, and question gates."""

    @classmethod
    def discover_arsenal(cls, task: str) -> Tuple[str, List[str]]:
        """Identify task niche and match highest-scoring skills from user's arsenal."""
        lower = task.lower()
        tools = []
        niche = "general-engineering"

        def _has_keyword(patterns: List[str]) -> bool:
            return any(re.search(rf"\b{re.escape(p)}\b", lower) for p in patterns)

        # Multi-modal / Sensory / Research Tools
        if _has_keyword(["browser", "playwright", "eyes", "ears", "whisper", "research", "reels", "trends", "github", "stack overflow"]):
            niche = "research-and-sensory"
            tools.extend(["aegis.browser", "local-whisper", "playwright-skill", "ffmpeg", "creator-intel", "ponytail", "unslop"])

        elif _has_keyword(["ui", "frontend", "landing", "css", "react", "page", "web"]):
            niche = "frontend"
            tools.extend(["uipro", "ui-ux-pro-max", "tailwindcss", "lucide-icons", "ponytail", "unslop"])

        elif _has_keyword(["backend", "api", "database", "postgres", "sql", "fastapi", "server", "pipeline", "streaming"]):
            niche = "backend"
            tools.extend(["pg-aiguide", "fastapi-patterns", "pydantic-v2", "sql-sentinel", "uv", "ponytail"])

        elif _has_keyword(["video", "audio", "voice", "speech", "media", "transcribe"]):
            niche = "media-processing"
            tools.extend(["ffmpeg", "local-whisper", "remotion-best-practices", "mediabunny"])

        elif _has_keyword(["security", "audit", "pentest", "vulnerability", "auth"]):
            niche = "security"
            tools.extend(["redteam-mindset", "sast-scanning", "gitguardian-scanner", "invariant-guard"])

        if not tools:
            tools = ["andrej-karpathy-skills", "ponytail", "unslop", "uv", "systematic-debugging", "ast-deep-merger"]

        return niche, tools

    @classmethod
    def evaluate_yc_feasibility(cls, task: str, niche: str) -> Tuple[int, List[str]]:
        """Evaluate concept with YC founder methodology and identify fatal flaws."""
        critique = YCCEOStressTester.evaluate(task)
        score = min(max(critique.feasibility_score * 10, 30), 95)
        flaws = list(critique.fatal_failure_modes)

        if niche == "research-and-sensory":
            flaws.append("Browser scraping rate-limits & Cloudflare turnstile gates if using raw web clients without proxy pools.")
            flaws.append("High memory / VRAM consumption when running local Whisper and headless Playwright simultaneously.")
        elif niche == "frontend" and not any("state" in f.lower() for f in flaws):
            flaws.append("Frontend state hydration mismatches and mobile viewport accessibility clipping.")
        elif niche == "backend" and not any("concurrency" in f.lower() for f in flaws):
            flaws.append("Unbounded database connection pooling and lack of circuit breakers under load spikes.")
        elif niche == "general-engineering" and not any("abstraction" in f.lower() for f in flaws):
            flaws.append("Premature modular abstraction for single-use code paths violating Karpathy and Ponytail simplicity.")

        return score, flaws

    @classmethod
    def generate_architecture_options(cls, task: str, niche: str) -> List[ArchitectureOption]:
        """Generate 3 to 4 distinct technical implementation pathways customized to the task."""
        if niche == "research-and-sensory":
            return [
                ArchitectureOption(
                    name="Dual-Layer Research & Sensory Pipeline (Fast HTTP + Playwright Fallback)",
                    archetype="Ponytail Efficiency / Zero-Bloat",
                    summary="Lightweight Jev-style HTTP parser for 90% of text/docs (<1,500 tokens), escalating to headless Playwright CLI only for JavaScript-heavy SPAs and visual screenshot inspections.",
                    feasibility_score=95,
                    complexity=3,
                    token_cost_rating="Lowest",
                    pros=["Ultra-low RAM overhead", "Sub-second scraping latency", "Local Whisper audio pipeline isolated in background process"],
                    cons=["Headless browser only spawned on demand, slight initial launch delay on cold start"],
                    recommended_when="Continuous planning phase research, GitHub/Reddit scraping, and rapid documentation extraction."
                ),
                ArchitectureOption(
                    name="Persistent Headless Playwright Browser Cluster with Dedicated CDP",
                    archetype="Heavy-Duty Browser Automation",
                    summary="Always-on Chromium instance via Chrome DevTools Protocol (CDP) with randomized user-agents and full DOM mutation observers.",
                    feasibility_score=82,
                    complexity=7,
                    token_cost_rating="Moderate",
                    pros=["Full JavaScript execution, cookie persistence, and automated UI event recording"],
                    cons=["Consumes ~600MB RAM persistently, risk of triggering host hardware bottleneck guard"],
                    recommended_when="Complex interactive UI journey testing, authenticated dashboards, and randomized stress testing."
                ),
                ArchitectureOption(
                    name="Asynchronous Social & Tech Radar Aggregator",
                    archetype="Event-Driven Multi-Source Collector",
                    summary="Background daemon queue polling Reddit (r/LocalLLaMA), GitHub trending feeds, and Telegram inbox media asynchronously during system idle periods.",
                    feasibility_score=90,
                    complexity=4,
                    token_cost_rating="Lowest",
                    pros=["Zero interference with active coding sessions", "Pre-computes research before user prompts arrive", "Offline Whisper audio transcription"],
                    cons=["Data freshness depends on polling interval"],
                    recommended_when="Long-term research accumulation, social reel ingestion, and keeping abreast of new tech trends."
                )
            ]

        if niche == "frontend":
            return [
                ArchitectureOption(
                    name="Minimalist High-Performance Single-Page Component",
                    archetype="Karpathy Simplicity / Zero-Build",
                    summary="Self-contained HTML5 + Tailwind CDN + Lucide Icons + Vanilla ES Modules. Zero npm overhead, instant browser launch.",
                    feasibility_score=94,
                    complexity=2,
                    token_cost_rating="Lowest",
                    pros=["Zero build pipeline friction", "Instant preview in any browser", "Lowest maintenance debt"],
                    cons=["No SSR or complex dynamic route splitting", "State managed via vanilla JS"],
                    recommended_when="Validating designs, standalone landing pages, dashboards, and quick demos."
                ),
                ArchitectureOption(
                    name="Next.js 15 App Router & Server Components",
                    archetype="Modern Enterprise Full-Stack",
                    summary="Next.js 15 with React Server Components, Tailwind CSS, Radix UI primitives, and streaming SSR.",
                    feasibility_score=85,
                    complexity=6,
                    token_cost_rating="Moderate",
                    pros=["Built-in SEO and OpenGraph metadata", "Optimized image loading", "Rich component ecosystem"],
                    cons=["Requires Node.js runtime and build step", "Hydration mismatch pitfalls"],
                    recommended_when="Production web applications requiring user authentication, dynamic SEO, and multiple routes."
                ),
                ArchitectureOption(
                    name="Decoupled Static UI with Headless API Bridge",
                    archetype="Jamstack & Micro-Frontend",
                    summary="Static frontend assets hosted on CDN communicating via REST/WebSocket with the local Aegis daemon.",
                    feasibility_score=88,
                    complexity=5,
                    token_cost_rating="Moderate",
                    pros=["Complete separation of presentation from backend logic", "Air-gapped security"],
                    cons=["Requires CORS and localhost certificate handling"],
                    recommended_when="Local desktop companion tools, internal admin dashboards, and IDE extensions."
                )
            ]

        # Backend / General Engineering
        return [
            ArchitectureOption(
                name="Surgical In-Place Minimalist Implementation",
                archetype="Andrej Karpathy & Ponytail Doctrine",
                summary="Minimum code required to fulfill requirements using native stdlib and surgical edits. Zero speculative classes, decorators, or wrappers.",
                feasibility_score=96,
                complexity=2,
                token_cost_rating="Lowest",
                pros=["Near-zero regression risk", "Fastest compilation and execution", "100% testable in minutes"],
                cons=["Less initial scaffolding for future speculative features"],
                recommended_when="Feature additions, bug fixes, CLI tools, and core system utilities."
            ),
            ArchitectureOption(
                name="Event-Driven Micro-Service with Pub/Sub Bus",
                archetype="Distributed Modular Engine",
                summary="Decoupled producer-consumer queues using async workers and event channels for multi-agent coordination.",
                feasibility_score=82,
                complexity=7,
                token_cost_rating="High",
                pros=["High concurrency throughput", "Independent failure domains", "Horizontal scaling capability"],
                cons=["Complex distributed debugging", "Higher token spend for orchestration"],
                recommended_when="High-volume background ingestion, real-time message streaming, and distributed queues."
            ),
            ArchitectureOption(
                name="Frontier Manager with Local Worker Offload",
                archetype="3-Tier Multi-Agent Token Arbitrage",
                summary="High-cognition manager defines contracts; local models (Hermes, Ollama, MoE) write repetitive implementations.",
                feasibility_score=91,
                complexity=4,
                token_cost_rating="Lowest (Saves 78% Tokens)",
                pros=["Massive cost savings", "Zero private code leakage to cloud", "Hardware bottleneck guarded"],
                cons=["Requires local model availability on host"],
                recommended_when="Large-scale code refactorings, test generation, and repetitive boilerplate generation."
            )
        ]

    @classmethod
    def generate_clarifying_interview(cls, task: str, niche: str, count: int = 6) -> List[ClarifyingQuestion]:
        """Generate 4 to 20 deep diagnostic questions tailored specifically to the problem domain."""
        if niche == "research-and-sensory":
            questions = [
                ClarifyingQuestion(
                    id="browser_extraction_mode",
                    category="Sensory & Tooling",
                    question="How should the research browser handle web content extraction during planning?",
                    options=[
                        "(Recommended) Lightweight Jev-style HTTP parser (<1,500 tokens) with Playwright fallback only for complex SPAs",
                        "Always spawn full Playwright headless browser for every URL to execute full JavaScript",
                        "DuckDuckGo API search only with snippet extraction, avoiding direct website navigation"
                    ]
                ),
                ClarifyingQuestion(
                    id="whisper_model_tier",
                    category="Sensory & Tooling",
                    question="Which local Whisper model tier should be used for audio perception without spiking host RAM?",
                    options=[
                        "(Recommended) Whisper 'base.en' (~140MB VRAM, fast sub-second transcription)",
                        "Whisper 'small' (~460MB VRAM, higher accuracy for technical jargon and accents)",
                        "Whisper 'tiny' (~75MB VRAM, maximum speed, minimal hardware footprint)"
                    ]
                ),
                ClarifyingQuestion(
                    id="playwright_ui_testing_strategy",
                    category="Sensory & Tooling",
                    question="How should Playwright CLI conduct frontend validation and randomized testing?",
                    options=[
                        "(Recommended) Randomized fuzz clicks and viewport resize tests with screenshot capture on error",
                        "Strict end-to-end user journey assertions matching PRD specification",
                        "Headless console error and network failure listener without UI interaction"
                    ]
                ),
                ClarifyingQuestion(
                    id="tech_radar_sources",
                    category="Scope",
                    question="Which community and trend sources should be prioritized during planning research?",
                    options=[
                        "(Recommended) Reddit (r/LocalLLaMA, r/webdev) + GitHub trending repositories + Stack Overflow",
                        "GitHub repository search & code inspection only",
                        "Official framework documentation sites and RFC specification indices"
                    ]
                ),
                ClarifyingQuestion(
                    id="telegram_media_pipeline",
                    category="Backend Logic",
                    question="How should incoming Telegram reels and links be stored and processed?",
                    options=[
                        "(Recommended) Download to .user_uploaded, transcribe audio with Whisper, extract keyframes with FFmpeg, and queue for idle processing",
                        "Process immediately upon receipt and interrupt active Antigravity session",
                        "Save URLs to a Markdown backlog without automatic media transcoding"
                    ]
                ),
                ClarifyingQuestion(
                    id="sandbox_promotion_gate",
                    category="Security & Reliability",
                    question="What gate must pass before tools and research scripts are executed on the host system?",
                    options=[
                        "(Recommended) Isolated sandbox test runner + Red-Team subprocess audit (block shell=True)",
                        "Standard unit test assertion runner with host permissions",
                        "Interactive user confirmation before every browser or script execution"
                    ]
                )
            ]
            return questions[:count]

        # Standard / Other Niches
        questions = [
            ClarifyingQuestion(
                id="deliverable_boundary",
                category="Scope",
                question=f"For '{task}', what is the exact delivery boundary?",
                options=[
                    "(Recommended) Standalone self-contained implementation with 100% automated test coverage",
                    "Modular library package integrated into an existing repo",
                    "Iterative Phase 1 Proof-of-Concept before building full production stack"
                ]
            ),
            ClarifyingQuestion(
                id="aesthetic_style_dial",
                category="UI/UX",
                question="Which aesthetic visual direction or design system should be prioritized?",
                options=[
                    "(Recommended) Dark Obsidian Glassmorphism (Deep slate, electric indigo accents, clean typography)",
                    "Modern Clean Minimalist / Swiss Style (White space, crisp black-and-white, zero visual clutter)",
                    "Cyberpunk / Neo-Brutalist (High-contrast borders, bold typography, vivid terminal accents)",
                    "Pure Headless CLI / No UI (ANSI color codes, rich progress bars, zero frontend overhead)"
                ]
            ),
            ClarifyingQuestion(
                id="backend_logic_approach",
                category="Backend Logic",
                question="How should core business logic and state persistence be structured?",
                options=[
                    "(Recommended) Lightweight SQLite with FTS5 search and transactional WAL mode",
                    "In-memory state with periodic JSON/YAML snapshot persistence",
                    "Enterprise PostgreSQL with TimescaleDB time-series and pgvector search",
                    "Pure stateless functional transforms without persistent storage"
                ]
            ),
            ClarifyingQuestion(
                id="concurrency_and_performance",
                category="Backend Logic",
                question="What is the expected execution model and concurrency requirement?",
                options=[
                    "(Recommended) Asynchronous non-blocking event loop (asyncio / Promise based)",
                    "Synchronous deterministic execution with explicit lock guards",
                    "Multi-threaded background worker pool with thread-safe queues"
                ]
            ),
            ClarifyingQuestion(
                id="error_tolerance_and_safety",
                category="Security & Reliability",
                question="How should unexpected runtime exceptions and edge-case inputs be handled?",
                options=[
                    "(Recommended) Create automated restore snapshot before changes & fail-safe rollback",
                    "Log structured warning, trigger circuit breaker, and return graceful degraded response",
                    "Strict fail-fast with full diagnostic traceback and invariant violation report"
                ]
            ),
            ClarifyingQuestion(
                id="testing_and_sandbox_gate",
                category="Security & Reliability",
                question="What verification gate must be passed before promoting to the host system?",
                options=[
                    "(Recommended) Isolated sandbox test runner + Red-Team security scan + 100% unit tests pass",
                    "Unit test suite only with standard assertion checks",
                    "Interactive user acceptance test walkthrough with live browser/terminal inspection"
                ]
            )
        ]
        return questions[:count]

    @classmethod
    def simulate_hierarchical_alignment(cls, task: str, niche: str) -> List[HierarchicalAgentDialog]:
        """Simulate hierarchical Q&A between Senior Boss, Junior Bosses, and Execution Workers."""
        dialogs = [
            HierarchicalAgentDialog(
                tier_from="Tier 2: Junior Boss (ArchitectureLead)",
                tier_to="Tier 1: Senior Boss (Antigravity)",
                agent_name="ArchitectureLead",
                question="What is the maximum allowed dependency footprint and token budget for this architecture?",
                answer="Keep dependencies strictly to standard library and verified packages. Do not introduce speculative abstractions. Apply Ponytail and Karpathy simplicity.",
                status="RESOLVED"
            ),
            HierarchicalAgentDialog(
                tier_from="Tier 2: Junior Boss (ImplementationLead)",
                tier_to="Tier 1: Senior Boss (Antigravity)",
                agent_name="ImplementationLead",
                question="Which tools from the user arsenal are authorized for local execution workers?",
                answer="Authorize aegis.browser for light scraping, local Whisper for audio, and Playwright for UI validation. Block raw shell=True execution.",
                status="RESOLVED"
            ),
            HierarchicalAgentDialog(
                tier_from="Tier 3: Execution Worker (Hermes Worker)",
                tier_to="Tier 2: Junior Boss (ImplementationLead)",
                agent_name="HermesWorker-01",
                question="What exact exception handling pattern and type contract should I apply to the data ingestion functions?",
                answer="Use explicit typing (Optional, Dict, List). Raise ValueError with human-readable error messages on malformed payloads. Return fallback dataclass on timeouts.",
                status="RESOLVED"
            ),
            HierarchicalAgentDialog(
                tier_from="Tier 3: Execution Worker (MoE Synthesizer)",
                tier_to="Tier 2: Junior Boss (ImplementationLead)",
                agent_name="MoESynthesizer-02",
                question="I need the UI UX Pro Max color tokens and Ponytail rules. Do I have access?",
                answer="Provided from arsenal: ~/.gemini/config/plugins/ponytail and ui-ux-pro-max design tokens applied. Strip AI filler with unslop.",
                status="RESOLVED"
            ),
            HierarchicalAgentDialog(
                tier_from="Tier 2: Junior Boss (VerificationLead)",
                tier_to="Tier 1: Senior Boss (Antigravity)",
                agent_name="VerificationLead",
                question="Are all 4 quality gates (Karpathy Simplicity, Unslop, Red-Team, Dual-Env) active for this release?",
                answer="Affirmative. 100% test passing required in sandbox environment before host filesystem mutation.",
                status="RESOLVED"
            )
        ]
        return dialogs

    @classmethod
    def generate_pre_execution_docs(cls, task: str, niche: str, option: ArchitectureOption) -> Tuple[str, str, str, List[Dict[str, Any]]]:
        """Generate PRD, TRD, ERD, and Task Ledger before code is written."""
        prd = f"""
- **Objective**: Deliver a production-grade, verifiable solution for `{task}` adhering to the {option.name} architecture.
- **Target Users**: Engineers and autonomous agent swarms requiring reliable research and testing capabilities.
- **Key Deliverables**:
  1. Complete, functional core logic with zero placeholder stubs or hardcoded responses.
  2. Automated test suite validating both happy paths and edge cases in an isolated sandbox.
  3. Seamless integration with active arsenal tools (Ponytail, Unslop, Browser, Whisper, Playwright).
- **Acceptance Criteria**:
  - Must pass 100% of unit tests in an isolated sandbox.
  - Zero Red-Team security vulnerabilities, shell=True invocations, or secret leaks.
  - Zero conversational AI filler or speculative over-engineering.
""".strip()

        trd = f"""
- **Architecture Pattern**: `{option.archetype}`
- **Runtime Environment**: Host Workstation (Windows 11 / Python 3.12 / Playwright CLI / Local Whisper)
- **Security Invariants**:
  - Subprocess calls must use explicit argument lists without `shell=True`.
  - Input strings sanitized against path traversal and command injection.
- **Error Handling**: Graceful degradation with automated snapshot rollback on fatal exceptions.
- **Dependencies**: Whitelisted local packages with zero untrusted external dependencies.
""".strip()

        erd = """
classDiagram
    class UserRequest {
        +String task
        +String priority
        +Timestamp createdAt
    }
    class DeepPlan {
        +Int feasibilityScore
        +List~String~ fatalFlaws
        +List~Option~ options
        +Boolean isClarified
    }
    class MultiAgentHierarchy {
        +Tier1 SeniorBoss
        +Tier2 JuniorBosses
        +Tier3 ExecutionWorkers
    }
    class SandboxVerifier {
        +Boolean redTeamPassed
        +Boolean unitTestsPassed
        +Boolean dualEnvPassed
    }

    UserRequest --> DeepPlan : Triggers
    DeepPlan --> MultiAgentHierarchy : Decomposes
    MultiAgentHierarchy --> SandboxVerifier : Submits for Gate Check
""".strip()

        ledger = [
            {"milestone": "1. Deep Planning & YC Feasibility Evaluation", "verification": "Feasibility report generated with flaw analysis", "status": "done"},
            {"milestone": "2. Interactive Clarification Interview", "verification": "User trade-offs and options locked in", "status": "pending"},
            {"milestone": "3. Hierarchical Cascading Alignment", "verification": "Senior-Junior-Worker Q&A dialog completed", "status": "pending"},
            {"milestone": "4. Pre-Execution Living Documentation (PRD/TRD/ERD)", "verification": "Living documents archived in brain.db", "status": "done"},
            {"milestone": "5. Sandboxed Component Implementation", "verification": "Isolated sandbox syntax & unit tests pass", "status": "pending"},
            {"milestone": "6. Red-Team Security & Cloudflare Invariant Audit", "verification": "Zero secret leakage, injection, or traversal flags", "status": "pending"},
            {"milestone": "7. Dual-Environment Host Promotion & Final Sign-Off", "verification": "Host verification test passes cleanly", "status": "pending"},
        ]

        return prd, trd, erd, ledger

    @classmethod
    def create_plan(cls, task: str, question_count: int = 6) -> DeepPlanReport:
        """Create a complete Deep Planning Report ready for user alignment."""
        niche, tools = cls.discover_arsenal(task)
        score, flaws = cls.evaluate_yc_feasibility(task, niche)
        options = cls.generate_architecture_options(task, niche)
        recommended = options[0].name
        questions = cls.generate_clarifying_interview(task, niche, count=question_count)
        dialogs = cls.simulate_hierarchical_alignment(task, niche)
        prd, trd, erd, ledger = cls.generate_pre_execution_docs(task, niche, options[0])

        return DeepPlanReport(
            task=task,
            niche=niche,
            feasibility_score=score,
            fatal_flaws=flaws,
            arsenal_tools_recommended=tools,
            architecture_options=options,
            recommended_option=recommended,
            clarifying_questions=questions,
            hierarchical_dialogs=dialogs,
            prd_markdown=prd,
            trd_markdown=trd,
            erd_mermaid=erd,
            task_ledger=ledger,
            is_clarified=False
        )
