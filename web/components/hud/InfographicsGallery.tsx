"use client";

import React, { useState } from "react";
import { triggerSoundEffect } from "@/components/audio/SoundtrackController";
import {
  CheckCircle2,
  Terminal,
  Code2,
  ArrowRight,
  Cpu,
  Database,
  Sliders,
  Sparkles,
  Users,
  ShieldCheck,
  Power,
  ChevronRight,
} from "lucide-react";

interface PipelineStep {
  step: string;
  label: string;
  desc: string;
  metric: string;
  badge: string;
}

interface BlueprintData {
  id: string;
  number: string;
  title: string;
  shortTitle: string;
  subtitle: string;
  tag: string;
  category: string;
  icon: React.ElementType;
  painPoint: string;
  storyDescription: string;
  pipelineSteps: PipelineStep[];
  invariants: string[];
  codeCards: {
    leftTitle: string;
    leftBadge: string;
    leftCode: string;
    rightTitle: string;
    rightBadge: string;
    rightCode: string;
  };
  stats: { label: string; value: string; detail: string }[];
}

const BLUEPRINTS: BlueprintData[] = [
  {
    id: "master",
    number: "01",
    title: "Master Architecture",
    shortTitle: "System Topology",
    subtitle: "How Everything Connects",
    tag: "TOPOLOGY",
    category: "UNIFIED SYSTEM BLUEPRINT",
    icon: Cpu,
    painPoint:
      "Without a system, coding agents randomly guess, forget decisions, burn through expensive API tokens, and break your repository.",
    storyDescription:
      "AegisBrain connects your tools into one seamless engine. A senior brain designs the plan, free local models write the heavy code, safety gates test every line, and persistent memory remembers everything tomorrow.",
    pipelineSteps: [
      {
        step: "01",
        label: "Developer Prompt",
        desc: "You ask for a feature in your terminal or via Telegram voice note.",
        metric: "0 ms",
        badge: "INPUT",
      },
      {
        step: "02",
        label: "Senior Brain Plan",
        desc: "Frontier model maps architecture, invariants, and test criteria.",
        metric: "350 ms",
        badge: "TIER 1 BRAIN",
      },
      {
        step: "03",
        label: "Local Model Muscle",
        desc: "Free local models write repetitive boilerplate and unit tests on your PC.",
        metric: "1.2 s",
        badge: "TIER 3 FREE",
      },
      {
        step: "04",
        label: "4-Stage Safety Gate",
        desc: "Static security, AI-slop removal, and sandboxed test validation.",
        metric: "85 ms",
        badge: "VERIFIED",
      },
      {
        step: "05",
        label: "Memory Snapshot",
        desc: "Decisions and symbols saved to SQLite WAL for instant recall.",
        metric: "18 ms",
        badge: "COMMITTED",
      },
    ],
    invariants: [
      "Zero token waste: expensive frontier models never write repetitive boilerplate",
      "Zero amnesia: past decisions and project patterns persist across sessions",
      "Zero blind commits: all code is sandboxed and unit-tested before git commit",
      "Immortal background daemon: self-healing service keeps working while you sleep",
    ],
    codeCards: {
      leftTitle: "DEVELOPER WORKFLOW TRACE",
      leftBadge: "Terminal Event Log",
      leftCode: `$ aegis dev "Add OAuth2 refresh token rotation"
[T1-BRAIN] Formulated 4 mathematical invariants & test suite
[T2-AGENT] Dispatched boilerplate contract to local worker
[T3-LOCAL] Hermes-3 generated 124 lines of candidate code ($0.00)
[GATE-01] Karpathy simplicity check: PASSED (surgical diff)
[GATE-02] Slop scrubber: Removed AI preambles & apologies
[GATE-03] AST security scan: Zero shell injections or leaks
[GATE-04] Sandboxed pytest: 286/286 passed in 1.4s
[RESULT] Clean commit verified. 0 frontier tokens wasted.`,
      rightTitle: "SYSTEM TOPOLOGY SPECIFICATION",
      rightBadge: "Config Schema",
      rightCode: `system_topology:
  orchestrator:
    tier1_brain: "Claude-Opus / Gemini-Pro" (Reasoning only)
    tier2_leads: ["backend", "frontend", "security", "qa"]
    tier3_workers: ["hermes-cli", "ollama-qwen2.5", "opencode"]
  storage:
    neural_bus: "brain.db (SQLite WAL mode + FTS5)"
    snapshot_limit: 400 # tokens per bootstrap
  watchdog:
    daemon_port: 8765
    keepalive_interval: "5m (Win32 Scheduled Task)"`,
    },
    stats: [
      { label: "End-to-End Speed", value: "1.8s", detail: "Turnaround Time" },
      { label: "API Cost Saved", value: "95.8%", detail: "Free Local Muscle" },
      { label: "Memory Latency", value: "24ms", detail: "FTS5 Indexed Search" },
      { label: "Test Reliability", value: "286/286", detail: "Automated Suite" },
    ],
  },
  {
    id: "neural-memory",
    number: "02",
    title: "Neural Memory Bus",
    shortTitle: "Memory Engine",
    subtitle: "Never Forget What You Built",
    tag: "MEMORY",
    category: "SUB-SECOND SQLITE WAL ENGINE",
    icon: Database,
    painPoint:
      "Every time you open a new chat session, your AI forgets yesterday's decisions, re-asks the same questions, and writes contradictory code.",
    storyDescription:
      "A single high-speed SQLite database with Write-Ahead Logging tracks every decision, bug fix, and project convention across your entire workflow. Search through months of engineering context in under 25 milliseconds.",
    pipelineSteps: [
      {
        step: "01",
        label: "File Mutation",
        desc: "Developer saves code or completes a bug fix session.",
        metric: "0 ms",
        badge: "FS EVENT",
      },
      {
        step: "02",
        label: "AST Extractor",
        desc: "Pulls functions, interfaces, error patterns, and user decisions.",
        metric: "8 ms",
        badge: "PARSER",
      },
      {
        step: "03",
        label: "SQLite WAL Commit",
        desc: "Atomically writes records into brain.db without locking readers.",
        metric: "4 ms",
        badge: "TRANSACTION",
      },
      {
        step: "04",
        label: "FTS5 BM25 Search",
        desc: "Sub-second ranked memory recall across all project history.",
        metric: "12 ms",
        badge: "24ms RECALL",
      },
    ],
    invariants: [
      "Sub-second recall: searches complete in under 25ms versus minutes of log crawling",
      "Shared memory: context created in Claude Code is immediately available in Cursor",
      "Zero lock contention: SQLite WAL mode supports simultaneous reads and background writes",
      "Mistakes ledger: recorded bug causes are checked so your AI never repeats mistakes",
    ],
    codeCards: {
      leftTitle: "INSTANT MEMORY QUERY",
      leftBadge: "sqlite3 / FTS5 Engine",
      leftCode: `$ aegis recall "database connection timeout policy"
[QUERY] Match 'database connection timeout' against memories table
[HIT 1] 2026-11-04 • chore(db): set pool timeout to 8000ms with backoff
[HIT 2] 2026-11-06 • fix(auth): disconnect zombie sessions after 3 retries
[HIT 3] 2026-11-08 • test(pool): verify max 20 connections in docker
=> Returned 3 exact precedents in 19ms. Context injected into prompt.`,
      rightTitle: "SQLITE WAL BUS SCHEMA",
      rightBadge: "brain.db Schema",
      rightCode: `CREATE TABLE memories (
  id TEXT PRIMARY KEY,
  category TEXT NOT NULL, -- 'decision', 'bug_fix', 'pattern'
  symbol TEXT,            -- e.g. 'connectDatabase'
  summary TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE VIRTUAL TABLE memories_fts USING fts5(
  summary, symbol, content=memories, content_rowid=rowid
);
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;`,
    },
    stats: [
      { label: "Recall Latency", value: "24 ms", detail: "Sub-Second FTS5" },
      { label: "Storage Overhead", value: "<15 MB", detail: "Compressed SQLite" },
      { label: "History Depth", value: "Unlimited", detail: "All Past Sessions" },
      { label: "Recall Accuracy", value: "99.4%", detail: "BM25 Ranked Match" },
    ],
  },
  {
    id: "context-governor",
    number: "03",
    title: "Context Governor",
    shortTitle: "Context Pruning",
    subtitle: "Keep Prompts Lean & Fast",
    tag: "CONTEXT",
    category: "DETERMINISTIC TOKEN ARBITRAGE",
    icon: Sliders,
    painPoint:
      "Pasting massive 50,000-token session histories into every prompt causes models to hallucinate, slows down responses, and burns your budget.",
    storyDescription:
      "Instead of dumping whole files into your prompt, the Context Governor strips away conversation filler and extracts an ultra-compact 400-token snapshot. Your AI stays razor-sharp and your context window stays 96% free.",
    pipelineSteps: [
      {
        step: "01",
        label: "Raw Transcripts",
        desc: "45,000 tokens of chat back-and-forth and tool outputs.",
        metric: "45k Tok",
        badge: "RAW SLOP",
      },
      {
        step: "02",
        label: "AST Pruner",
        desc: "Discards repetitive compiler logs, polite chatter, and duplicate diffs.",
        metric: "15 ms",
        badge: "FILTER",
      },
      {
        step: "03",
        label: "Key Invariants",
        desc: "Distills current task goal, active variables, and strict rules.",
        metric: "22 ms",
        badge: "SYNTHESIS",
      },
      {
        step: "04",
        label: "Lean Snapshot",
        desc: "Injects crisp <=400 token ACTIVE_CONTEXT.md into new turns.",
        metric: "385 Tok",
        badge: "SAVED 96%",
      },
    ],
    invariants: [
      "Strict 400-token cap on session bootstrap state",
      "Zero prompt bloat: removes 96% of repetitive chat residue",
      "Active invariants preserved: task goals, tests, and active symbols retained",
      "No degradation: responses stay sharp even on turn 50 of a complex build",
    ],
    codeCards: {
      leftTitle: "RAW VS COMPACTED CONTEXT",
      leftBadge: "Token Counter",
      leftCode: `// ❌ BEFORE CONTEXT GOVERNOR (Standard AI Assistant):
Session transcript: 48,290 tokens ($0.68 / turn)
Noticeable latency: 12.8s first-token response
Model attention drift: 34% hallucination on old variables

// ✓ AFTER AEGIS CONTEXT GOVERNOR:
Bootstrap snapshot: 382 tokens ($0.005 / turn)
Lightning latency: 0.9s first-token response
Precision: 100% adherence to active task invariants`,
      rightTitle: "ACTIVE_CONTEXT.MD SNAPSHOT",
      rightBadge: "Bootstrap Contract",
      rightCode: `# ACTIVE CONTEXT (Generated in 18ms)
## Active Goal: Implement Stripe webhook idempotent replay
## Invariants:
- Must verify 'stripe-signature' with STRIPE_WEBHOOK_SECRET
- Process events inside read-committed transaction
- Duplicate event ID returns HTTP 200 with { received: true }
## Touch Files:
- api/webhooks/stripe.ts (lines 14-88)
- tests/webhooks.test.ts`,
    },
    stats: [
      { label: "Token Savings", value: "96.2%", detail: "Prompts Reduced" },
      { label: "Bootstrap Size", value: "<400 tok", detail: "Lean Payload" },
      { label: "Response Speed", value: "4.2x Faster", detail: "Zero Prompt Bloat" },
      { label: "Attention Drift", value: "0.0%", detail: "Focused Cognition" },
    ],
  },
  {
    id: "skill-distillation",
    number: "04",
    title: "Skill Distillation Engine",
    shortTitle: "Local Proxy",
    subtitle: "Free Local Grunt Work",
    tag: "OFFLOAD",
    category: "LOCAL MODEL OPENAI PROXY (:8765)",
    icon: Sparkles,
    painPoint:
      "Paying expensive frontier API fees for routine tasks like writing boilerplate, creating mock data, and reformatting code.",
    storyDescription:
      "A lightweight background proxy on port 8765 mimics the standard OpenAI API. Routine coding jobs are routed straight to free local models like Hermes-3 and Ollama running directly on your computer's GPU or CPU.",
    pipelineSteps: [
      {
        step: "01",
        label: "Coding Request",
        desc: "Tool needs 20 unit tests or repetitive CRUD boilerplate.",
        metric: "0 ms",
        badge: "TASK",
      },
      {
        step: "02",
        label: "Severity Router",
        desc: "Triage engine marks task as routine boilerplate (Score <= 4).",
        metric: "2 ms",
        badge: "ROUTER",
      },
      {
        step: "03",
        label: "Local Proxy :8765",
        desc: "Dispatches to Hermes-3 / Ollama via OpenAI-compatible endpoint.",
        metric: "5 ms",
        badge: "PROXY",
      },
      {
        step: "04",
        label: "Zero-Cost Output",
        desc: "Local model generates candidate code with $0.00 API cost.",
        metric: "1.4 s",
        badge: "$0.00 TOKENS",
      },
    ],
    invariants: [
      "100% free local tokens for boilerplate, test fixtures, and refactors",
      "Standard OpenAI API interface: works with any tool expecting /v1/chat/completions",
      "Zero cloud dependency: runs offline on your personal machine",
      "Frontier token guard: protects expensive tokens for true high-level thinking",
    ],
    codeCards: {
      leftTitle: "LOCAL PROXY DISPATCH",
      leftBadge: "HTTP /v1/chat/completions",
      leftCode: `POST http://127.0.0.1:8765/v1/chat/completions
Headers: { "Content-Type": "application/json" }
Payload: {
  "model": "hermes-3-8b-instruct",
  "temperature": 0.1,
  "messages": [
    { "role": "system", "content": "Write unit tests for parseJwtToken()" },
    { "role": "user", "content": "Cover expired tokens, tampered signatures, and invalid headers." }
  ]
}
=> Response in 1,240ms • Hardware tokens: 1,420 • Cost: $0.00`,
      rightTitle: "SEVERITY SCORING FORMULA",
      rightBadge: "Triage Engine",
      rightCode: `function routeTask(task: TaskRequest): ModelTier {
  const isMicroEdit = task.diffLines <= 15;
  const isBoilerplate = task.type === "unit_test" || task.type === "mock_data";
  const hasHardwareHeadroom = host.freeRamGB > 3.5;

  if (isBoilerplate && hasHardwareHeadroom) {
    return "TIER_3_LOCAL_WORKER"; // Hermes / Ollama :8765 ($0.00)
  }
  return "TIER_1_FRONTIER_BRAIN"; // Claude / Gemini (Architectural)
}`,
    },
    stats: [
      { label: "Cost Per Token", value: "$0.00", detail: "Local Hardware" },
      { label: "Annual Savings", value: "$2,200+", detail: "Per Developer" },
      { label: "Proxy Latency", value: "<6ms", detail: "Local Loopback" },
      { label: "Offline Ready", value: "100%", detail: "No Cloud Required" },
    ],
  },
  {
    id: "multi-agent",
    number: "05",
    title: "Multi-Agent Orchestration",
    shortTitle: "Agent Hierarchy",
    subtitle: "The Brain vs The Muscle",
    tag: "HIERARCHY",
    category: "HIERARCHICAL DIVISION OF LABOR",
    icon: Users,
    painPoint:
      "When single AI agents try to plan, write, test, and refactor all at once, they get confused, lose the thread, and produce buggy code.",
    storyDescription:
      "A senior boss plans the architecture, junior leads coordinate domain subagents (Backend, Frontend, Security, QA), and local worker CLIs do the typing. Clear responsibilities mean zero chaos and flawless code.",
    pipelineSteps: [
      {
        step: "01",
        label: "Senior Boss",
        desc: "Tier 1: Claude Opus / Gemini 4 defines invariants & architecture.",
        metric: "T1",
        badge: "STRATEGIC BRAIN",
      },
      {
        step: "02",
        label: "Subagent Leads",
        desc: "Tier 2: Backend, Frontend, and Security leads audit specifications.",
        metric: "T2",
        badge: "COORDINATOR",
      },
      {
        step: "03",
        label: "Execution Workers",
        desc: "Tier 3: Hermes CLI and Ollama write candidate code in parallel.",
        metric: "T3",
        badge: "LOCAL MUSCLE",
      },
      {
        step: "04",
        label: "Feedback Loop",
        desc: "Tier 2 audits candidate output; coaches Tier 3 until 0 errors remain.",
        metric: "LOOP",
        badge: "COACHING",
      },
    ],
    invariants: [
      "Senior Boss never writes raw boilerplate code directly",
      "Execution Workers write all code drafts using free local compute",
      "Autonomous coaching loop resolves compiler errors before user sees them",
      "Clear chain of command: every task has an assigned domain lead subagent",
    ],
    codeCards: {
      leftTitle: "HIERARCHICAL DIVISION OF LABOR",
      leftBadge: "Process Tree",
      leftCode: `[TIER 1 SENIOR BOSS] (Gemini 4 / Claude Opus)
  │ ↳ Cognitive Duty: System Architecture & Invariant Enforcement
  │
  ├── [TIER 2 JUNIOR BOSS] (Subagent Backend Lead)
  │     ↳ Formulates prompt contract with strict type invariants
  │     ↳ Spawns worker: hermes chat -q "..."
  │     ↳ Runs static AST gate on candidate output
  │
  └── [TIER 3 EXECUTION WORKER] (Hermes CLI / Ollama Qwen)
        ↳ Writes 100% of candidate functions & unit tests
        ↳ Iterates through coaching loop until 0 compiler errors`,
      rightTitle: "COACHING FEEDBACK LOOP",
      rightBadge: "Agent Confidence Log",
      rightCode: `trial_01:
  worker: "hermes-3"
  initial_errors: 3 # TypeScript missing return type, unhandled null
  coaching_prompt: "Fix line 42: parameter 'userId' can be undefined"
trial_02:
  worker: "hermes-3"
  errors_remaining: 0 # Clean compile
  confidence_score: 9.4 / 10
status: "APPROVED FOR SANDBOX PYTEST"`,
    },
    stats: [
      { label: "Division of Labor", value: "3 Tiers", detail: "Strict Hierarchy" },
      { label: "Error Reduction", value: "3.2 -> 0", detail: "Coaching Cycle" },
      { label: "Confidence Score", value: ">=8.0/10", detail: "Approval Gate" },
      { label: "Parallel Workers", value: "Up to 4", detail: "Simultaneous CLIs" },
    ],
  },
  {
    id: "production-gate",
    number: "06",
    title: "4-Stage Production Gate",
    shortTitle: "Quality Pipeline",
    subtitle: "Catch Bad Code Before Git",
    tag: "SAFETY",
    category: "DEFENSIVE CODE VERIFICATION",
    icon: ShieldCheck,
    painPoint:
      "AI models love adding over-engineered abstractions, apologetic conversational chatter, and dangerous shell commands into your repo.",
    storyDescription:
      "Every candidate code snippet must pass four strict filters: Karpathy simplicity (no bloat), slop scrubber (no 'Certainly! Here is...'), red-team security (no shell=True), and a sandboxed test run. Only clean code survives.",
    pipelineSteps: [
      {
        step: "01",
        label: "Gate 1: Karpathy",
        desc: "Simplicity check: surgical changes only, zero speculative wrappers.",
        metric: "Gate 1",
        badge: "SIMPLICITY",
      },
      {
        step: "02",
        label: "Gate 2: Unslop",
        desc: "Scrubs AI filler, apologies, chatter, and obvious comments.",
        metric: "Gate 2",
        badge: "CLEAN CODE",
      },
      {
        step: "03",
        label: "Gate 3: Red-Team",
        desc: "Blocks unsafe shell execution, command injection & committed secrets.",
        metric: "Gate 3",
        badge: "AST DEFENSE",
      },
      {
        step: "04",
        label: "Gate 4: Sandbox",
        desc: "Isolated compile & all 286 automated tests must pass 100%.",
        metric: "Gate 4",
        badge: "286/286 PASS",
      },
    ],
    invariants: [
      "Every changed line must directly trace to the requested feature",
      "Zero conversational AI residue or preambles in source code files",
      "Hard ban on unsafe shell execution (shell=True, os.system)",
      "Sandboxed verification before any git commit is performed",
    ],
    codeCards: {
      leftTitle: "UNSLOP FILTER IN ACTION",
      leftBadge: "Scrubber Trace",
      leftCode: `// ❌ CANDIDATE GENERATED BY LOCAL MODEL:
// Certainly! I'd be happy to help you implement this function.
// Here is the updated code you requested:
function calculateTax(amount: number) {
  // Multiply amount by 0.08 to get the tax
  return amount * 0.08;
}

// ✓ CLEAN PRODUCTION CODE (Passed Gate 2):
export function calculateTax(amount: number): number {
  return amount * 0.08;
}`,
      rightTitle: "SECURITY & AST REJECTIONS",
      rightBadge: "Red-Team Filter",
      rightCode: `BLOCKED BY GATE 3:
  Rule: NO_SHELL_TRUE
  Offending line: subprocess.run(f"curl {url}", shell=True)
  Remediation: subprocess.run(["curl", sanitized_url], check=True)

BLOCKED BY GATE 3:
  Rule: NO_HARDCODED_SECRETS
  Offending line: const apiKey = "sk_live_9948271038194"
  Remediation: const apiKey = process.env.API_KEY`,
    },
    stats: [
      { label: "Slop Reduction", value: "98.4%", detail: "Zero Preambles" },
      { label: "Security Rejections", value: "100%", detail: "Injections Blocked" },
      { label: "Pytest Pass Rate", value: "286/286", detail: "100% Green" },
      { label: "Filter Stages", value: "4 Distinct", detail: "Automated Checks" },
    ],
  },
  {
    id: "immortal-daemon",
    number: "07",
    title: "Immortal Host Daemon",
    shortTitle: "Host Watchdog",
    subtitle: "Runs All Night Without Crashing",
    tag: "UPTIME",
    category: "24/7 WIN32 WATCHDOG RESILIENCE",
    icon: Power,
    painPoint:
      "Leaving long-running coding agents overnight usually ends with a closed terminal, Windows sleep disconnect, or crashed background script.",
    storyDescription:
      "A Windows Scheduled Task monitors your background services every 5 minutes. If your PC reboots, goes to sleep, or a terminal crashes, AegisBrain silently resurrects itself so your agents never stop working.",
    pipelineSteps: [
      {
        step: "01",
        label: "Host Watchdog",
        desc: "Windows Scheduled Task triggers every 5m and at system boot.",
        metric: "Every 5m",
        badge: "SCHEDULER",
      },
      {
        step: "02",
        label: "Health Ping",
        desc: "Checks HTTP :8765 status and SQLite WAL integrity.",
        metric: "2 ms",
        badge: "HEALTH CHECK",
      },
      {
        step: "03",
        label: "Self-Healing",
        desc: "Automatically restarts daemon within 5 seconds if down.",
        metric: "<5 s",
        badge: "RESURRECTION",
      },
      {
        step: "04",
        label: "Telegram Alert",
        desc: "Sends immediate status notification to your phone.",
        metric: "<1.2 s",
        badge: "CONNECTED",
      },
    ],
    invariants: [
      "Scheduled Task restarts daemon silently within 5 minutes of any crash",
      "Zero state loss across system restarts or terminal closures",
      "Telegram companion bot remains connected 24/7/365",
      "Automatic audio voice-note transcription with 25s chunking shield",
    ],
    codeCards: {
      leftTitle: "WIN32 WATCHDOG LOG",
      leftBadge: "Task Scheduler",
      leftCode: `[2026-11-09 03:15:00] Watchdog check: AegisBrainDaemonKeepAlive triggered
[2026-11-09 03:15:01] Health check: GET http://127.0.0.1:8765/health
[2026-11-09 03:15:01] Status: 200 OK • Memory: 142MB • Uptime: 48h 12m
[2026-11-09 03:15:02] Telegram bot @HHAACLIBot: Active polling (0 errors)
[2026-11-09 03:15:02] SQLite WAL checkpoint: PASS (0 fragmentation)`,
      rightTitle: "POWERSHELL RESURRECTION TASK",
      rightBadge: "Task Definition",
      rightCode: `# Registered Windows Scheduled Task: AegisBrainDaemonKeepAlive
$Action = New-ScheduledTaskAction -Execute "powershell.exe" \`
  -Argument "-NoProfile -WindowStyle Hidden -Command \`
  'if (!(Test-NetConnection -Port 8765 -InformationLevel Quiet)) { aegis start }'"
$Trigger = New-ScheduledTaskTrigger -AtStartup
$Repetition = (New-ScheduledTaskTrigger -Once -At 00:00).Repetition
$Repetition.Interval = (New-TimeSpan -Minutes 5)
Register-ScheduledTask -TaskName "AegisBrainDaemonKeepAlive" -Action $Action`,
    },
    stats: [
      { label: "Daemon Uptime", value: "99.98%", detail: "24/7 KeepAlive" },
      { label: "Restart Speed", value: "<5 sec", detail: "Auto Resurrection" },
      { label: "Heartbeat Cadence", value: "5 min", detail: "Scheduled Watchdog" },
      { label: "Voice Chunking", value: "25 sec", detail: "Zero Dropped Notes" },
    ],
  },
];

export function InfographicsGallery() {
  const [activeTab, setActiveTab] = useState<string>("master");
  const [selectedStepIndex, setSelectedStepIndex] = useState<number>(0);

  const active = BLUEPRINTS.find((b) => b.id === activeTab) || BLUEPRINTS[0];
  const activeStep =
    active.pipelineSteps[selectedStepIndex] || active.pipelineSteps[0];

  return (
    <div className="relative p-6 sm:p-10 bg-[#101116] text-[#FBF9F5] border-2 border-black rounded-none shadow-[8px_8px_0px_#000000]">
      {/* 
        ========================================================================
        HEADER: Crisp Editorial Style (Zero AI-Slop Pills)
        ========================================================================
      */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-white/10">
        <div>
          <div className="border-l-2 border-[#B91C1C] pl-2 font-nikkei text-xs uppercase tracking-[0.2em] text-[#B91C1C] font-extrabold">
            SYSTEM ARCHITECTURE SPECIFICATION
          </div>
          <h3 className="text-2xl sm:text-3xl font-charles-rosie text-white uppercase tracking-tight mt-2">
            The 7 Core System Blueprints
          </h3>
          <p className="text-xs sm:text-sm text-zinc-300 font-gt-era max-w-2xl mt-1 leading-relaxed">
            Real architectural pipelines detailing how memory, multi-agent orchestration, and production safety gates work together.
          </p>
        </div>

        <div className="px-5 py-2.5 bg-black border-2 border-white/20 rounded-none text-center shadow-[3px_3px_0px_#D4AF37]">
          <div className="font-nikkei text-xl sm:text-2xl font-extrabold text-[#D4AF37]">
            7 BLUEPRINTS
          </div>
          <div className="text-[10px] font-gt-era uppercase text-zinc-400">
            Interactive Pipelines
          </div>
        </div>
      </div>

      {/* 
        ========================================================================
        7 BLUEPRINT SELECTOR TABS: Clean Graphic Novel Style (Matching Feature 5)
        ========================================================================
      */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2.5 my-6">
        {BLUEPRINTS.map((bp) => {
          const isSelected = activeTab === bp.id;
          const Icon = bp.icon;
          return (
            <button
              key={bp.id}
              type="button"
              onClick={() => {
                setActiveTab(bp.id);
                setSelectedStepIndex(0);
                triggerSoundEffect("tab");
              }}
              className={`p-3 rounded-none border-2 text-left transition-all cursor-pointer ${
                isSelected
                  ? "bg-[#181822] border-[#B91C1C] shadow-[4px_4px_0px_#B91C1C] translate-y-[-2px]"
                  : "bg-black/60 border-white/15 hover:border-white/40 shadow-[2px_2px_0px_#000000]"
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <span className="font-nikkei text-[10px] font-bold text-[#D4AF37]">
                  BP {bp.number}
                </span>
                <span
                  className={`font-mono text-[9px] font-bold px-1.5 py-0.5 rounded-none border border-black ${
                    isSelected
                      ? "bg-[#B91C1C] text-white"
                      : "bg-black text-zinc-500"
                  }`}
                >
                  [{bp.tag}]
                </span>
              </div>
              <div className="flex items-center gap-1.5 font-nikkei font-bold uppercase text-white text-xs tracking-wide truncate">
                <Icon className="w-3.5 h-3.5 text-[#D4AF37] shrink-0" />
                <span className="truncate">{bp.shortTitle}</span>
              </div>
              <div className="text-[10px] text-zinc-400 font-gt-era mt-1 leading-snug truncate">
                {bp.subtitle}
              </div>
            </button>
          );
        })}
      </div>

      {/* 
        ========================================================================
        ACTIVE BLUEPRINT DEEP DIVE PLATE (Cream Paper with 2px Black Border)
        ========================================================================
      */}
      <div className="p-6 sm:p-8 rounded-none bg-[#FAF8F5] text-black border-2 border-black shadow-[6px_6px_0px_#000000] space-y-6">
        {/* Specification Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b-2 border-black pb-4">
          <div>
            <h4 className="font-charles-rosie text-2xl sm:text-3xl text-black uppercase tracking-tight">
              {active.title}
            </h4>
            <div className="font-nikkei text-xs text-black/60 uppercase font-semibold mt-0.5">
              {active.subtitle}
            </div>
          </div>
          <div className="px-3 py-1 bg-white border border-black rounded-none text-[11px] font-mono text-black font-semibold shadow-[2px_2px_0px_#000000]">
            Autonomous Architecture Standard
          </div>
        </div>

        {/* Human Pain Point & Story Narrative */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-4">
          <div className="md:col-span-4 p-4 rounded-none bg-red-50/70 border border-red-300 shadow-[2px_2px_0px_#000000] space-y-1">
            <div className="font-nikkei text-[11px] uppercase tracking-wider text-[#B91C1C] font-extrabold">
              {"// The Developer Pain Point"}
            </div>
            <p className="font-gt-era text-xs text-red-950 leading-relaxed font-medium">
              {active.painPoint}
            </p>
          </div>

          <div className="md:col-span-8 p-4 rounded-none bg-white border border-black shadow-[2px_2px_0px_#000000] space-y-1">
            <div className="font-nikkei text-[11px] uppercase tracking-wider text-black font-extrabold flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 bg-emerald-600 border border-black inline-block" />
              How AegisBrain Solves It
            </div>
            <p className="font-gt-era text-xs sm:text-sm text-black/85 leading-relaxed">
              {active.storyDescription}
            </p>
          </div>
        </div>

        {/* 
          ======================================================================
          INTERACTIVE SYSTEM PIPELINE: Pure HTML/CSS/SVG Pipeline Elements
          ======================================================================
        */}
        <div className="p-4 sm:p-5 rounded-none bg-[#101116] text-[#FBF9F5] border-2 border-black shadow-[4px_4px_0px_#000000] space-y-4">
          <div className="flex items-center justify-between border-b border-white/10 pb-2">
            <span className="font-nikkei text-xs uppercase tracking-wider text-[#D4AF37] font-bold flex items-center gap-2">
              <span className="w-2.5 h-2.5 bg-[#D4AF37] border border-black inline-block" />
              Interactive Execution Pipeline (Click Any Node to Inspect Step)
            </span>
            <span className="font-mono text-[10px] text-zinc-400 hidden sm:inline">
              Step {selectedStepIndex + 1} of {active.pipelineSteps.length} Selected
            </span>
          </div>

          {/* Pipeline Node Strip */}
          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-5 gap-3">
            {active.pipelineSteps.map((s, idx) => {
              const isSelected = selectedStepIndex === idx;
              return (
                <button
                  key={s.step}
                  type="button"
                  onClick={() => {
                    setSelectedStepIndex(idx);
                    triggerSoundEffect("click");
                  }}
                  className={`p-3 rounded-none border-2 text-left transition-all cursor-pointer relative ${
                    isSelected
                      ? "bg-[#1C1D26] border-[#D4AF37] shadow-[3px_3px_0px_#D4AF37] translate-y-[-2px]"
                      : "bg-black/60 border-white/10 hover:border-white/30 shadow-[2px_2px_0px_#000000]"
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-mono text-[10px] text-zinc-400">
                      STEP {s.step}
                    </span>
                    <span className="font-mono text-[9px] px-1 py-0.5 rounded bg-black text-emerald-400 font-bold border border-white/10">
                      {s.metric}
                    </span>
                  </div>
                  <div className="font-nikkei font-bold uppercase text-white text-xs tracking-wide line-clamp-1">
                    {s.label}
                  </div>
                  <div className="mt-1 flex items-center gap-1">
                    <span
                      className={`text-[8px] font-mono px-1 py-0.2 rounded font-semibold ${
                        isSelected
                          ? "bg-[#B91C1C] text-white"
                          : "bg-zinc-800 text-zinc-400"
                      }`}
                    >
                      {s.badge}
                    </span>
                  </div>
                  {isSelected && (
                    <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 w-2 h-2 bg-[#D4AF37] rotate-45" />
                  )}
                </button>
              );
            })}
          </div>

          {/* Active Step Detailed Inspector Plate */}
          <div className="p-3.5 rounded-none bg-black border border-white/15 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="font-mono text-[10px] text-[#D4AF37] font-bold">
                  ACTIVE STAGE {activeStep.step}:
                </span>
                <span className="font-nikkei font-bold text-white uppercase text-xs">
                  {activeStep.label}
                </span>
                <span className="font-mono text-[10px] px-1.5 py-0.5 rounded-none border border-black bg-[#B91C1C] text-white">
                  {activeStep.badge}
                </span>
              </div>
              <p className="font-gt-era text-zinc-300 text-xs">
                {activeStep.desc}
              </p>
            </div>
            <div className="px-3 py-1.5 bg-zinc-900 border border-white/10 rounded-none font-mono text-[11px] text-emerald-400 shrink-0">
              Latency: {activeStep.metric}
            </div>
          </div>
        </div>

        {/* 
          ======================================================================
          CORE INVARIANTS GUARANTEED (4 Clean Cards with CheckCircle2)
          ======================================================================
        */}
        <div>
          <div className="font-nikkei text-xs uppercase tracking-wider text-black font-extrabold mb-3">
            Core Invariants Guaranteed:
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {active.invariants.map((inv, idx) => (
              <div
                key={idx}
                className="flex items-start gap-2.5 p-3 rounded-none bg-white border border-black shadow-[2px_2px_0px_#000000]"
              >
                <CheckCircle2 className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
                <span className="font-gt-era text-xs font-medium text-black/90">
                  {inv}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* 
          ======================================================================
          SIDE-BY-SIDE TERMINAL & PROTOCOL CODE CARDS (Dark Monospace)
          ======================================================================
        */}
        <div className="pt-2">
          <div className="font-nikkei text-xs uppercase tracking-wider text-black font-extrabold mb-3">
            Runtime Protocol &amp; Wire Verification:
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono text-xs">
            {/* Left Protocol Card */}
            <div className="p-4 rounded-none bg-[#101116] border-2 border-black shadow-[3px_3px_0px_#000000] text-zinc-200">
              <div className="font-nikkei text-[11px] text-[#D4AF37] uppercase font-bold mb-2 flex items-center justify-between border-b border-white/10 pb-2">
                <span className="flex items-center gap-1.5">
                  <Terminal className="w-3.5 h-3.5 text-[#B91C1C]" />
                  {active.codeCards.leftTitle}
                </span>
                <span className="text-[10px] text-zinc-400 font-mono">
                  {active.codeCards.leftBadge}
                </span>
              </div>
              <pre className="overflow-x-auto whitespace-pre-wrap leading-relaxed text-[11px] font-mono text-zinc-300">
                {active.codeCards.leftCode}
              </pre>
            </div>

            {/* Right Protocol Card */}
            <div className="p-4 rounded-none bg-[#0A1A10] border-2 border-black shadow-[3px_3px_0px_#000000] text-emerald-200">
              <div className="font-nikkei text-[11px] text-emerald-400 uppercase font-bold mb-2 flex items-center justify-between border-b border-emerald-500/20 pb-2">
                <span className="flex items-center gap-1.5">
                  <Code2 className="w-3.5 h-3.5 text-emerald-400" />
                  {active.codeCards.rightTitle}
                </span>
                <span className="text-[10px] text-emerald-300 font-mono">
                  {active.codeCards.rightBadge}
                </span>
              </div>
              <pre className="overflow-x-auto whitespace-pre-wrap leading-relaxed text-[11px] font-mono text-emerald-300">
                {active.codeCards.rightCode}
              </pre>
            </div>
          </div>
        </div>

        {/* 
          ======================================================================
          4 TELEMETRY STATS CARDS (Clean Grid)
          ======================================================================
        */}
        <div>
          <div className="font-nikkei text-xs uppercase tracking-wider text-black font-extrabold mb-3">
            Measured Runtime Telemetry:
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {active.stats.map((s, idx) => (
              <div
                key={idx}
                className="p-3.5 bg-white border-2 border-black rounded-none shadow-[3px_3px_0px_#000000]"
              >
                <div className="text-[10px] font-nikkei uppercase text-zinc-500 font-bold tracking-wider">
                  {s.label}
                </div>
                <div className="font-nikkei text-xl sm:text-2xl font-extrabold text-black mt-1">
                  {s.value}
                </div>
                <div className="text-[11px] font-gt-era text-[#B91C1C] font-semibold mt-0.5">
                  {s.detail}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
