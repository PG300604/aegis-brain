"use client";

import React, { useState } from "react";
import {
  Layers,
  Cpu,
  Database,
  ShieldAlert,
  Terminal,
  Activity,
  CheckCircle2,
  Copy,
  Check,
  ChevronRight,
  Flame,
  ArrowRight,
  Sparkles,
} from "lucide-react";

export interface Feature06BlueprintCardsProps {
  className?: string;
  initialBlueprintIndex?: number;
}

interface BlueprintData {
  id: string;
  code: string;
  title: string;
  subtitle: string;
  category: string;
  icon: React.ComponentType<{ className?: string }>;
  description: string;
  hierarchy: {
    tier1: string;
    tier2: string;
    tier3: string;
  };
  metrics: { label: string; value: string; delta: string }[];
  invariants: string[];
  codeSnippet: string;
  cliCommand: string;
}

const BLUEPRINTS: BlueprintData[] = [
  {
    id: "BP-01",
    code: "ARCH_3TIER_GOVERNOR",
    title: "3-Tier Hierarchical Governor",
    subtitle: "Senior Brain → Domain Lead → Free Local Execution Nodes",
    category: "ORCHESTRATION",
    icon: Layers,
    description:
      "Eliminates frontier token burn by strictly segregating strategic reasoning from boilerplate writing. The Senior Brain plans invariants; local workers write raw code.",
    hierarchy: {
      tier1: "Tier 1: Senior Brain (Frontier Model - High Cognition & AST Gates)",
      tier2: "Tier 2: Sub-Agent Leads (Domain Verification & Coaching Loops)",
      tier3: "Tier 3: Worker CLI (Hermes / Ollama / Local Nodes - 0 Frontier Tokens)",
    },
    metrics: [
      { label: "Token Arbitrage", value: "95.8%", delta: "-$142/mo" },
      { label: "AST Gate Latency", value: "1.8ms", delta: "Sub-frame" },
      { label: "Coaching Loops", value: "1.2 avg", delta: "Converged" },
      { label: "Zero-Leak Rate", value: "100%", delta: "Air-gapped" },
    ],
    invariants: [
      "∀ C ∈ Changeset : DiffLines(C) ≤ 15 ∨ WorkerDelegated(C) = TRUE",
      "Cost(Frontier) → min s.t. QualityGate(Draft) = 1.000",
      "SeniorBrain.WritesRawCode = FALSE (Zero-Direct-Code Invariant)",
      "Worker.LoopLimit ≤ 5 ∧ ErrorRate → 0.000",
    ],
    codeSnippet: `// Aegis Orchestrator Triage
export async function triageTask(task: TaskSpec): Promise<ExecutionPlan> {
  const complexity = evaluateComplexity(task);
  if (complexity <= 15) {
    return { route: "DIRECT_SURGICAL", model: "TIER2_SUBAGENT" };
  }
  return {
    route: "LOCAL_WORKER_ARBITRAGE",
    worker: "hermes",
    auditor: "TIER1_BRAIN",
    gate: "KARPATHY_SIMPLICITY",
  };
}`,
    cliCommand: "aegis triage --task 'synthesize telemetry bus' --arbitrage",
  },
  {
    id: "BP-02",
    code: "FTS5_NEURAL_MEMORY",
    title: "SQLite FTS5 Neural Memory Core",
    subtitle: "Permanent Sub-Second Photographic Context Persistence",
    category: "PERSISTENCE",
    icon: Database,
    description:
      "Replaces multi-megabyte raw log crawls with zero-latency SQLite BM25 full-text indexing. Agents recall rules, past fixes, and design decisions in 21ms.",
    hierarchy: {
      tier1: "Schema: SQLite FTS5 Virtual Table (brain.db)",
      tier2: "Index: Trigram BM25 + Recency Ranking Decay",
      tier3: "Access: Zero-Copy CLI Shims (aegis recall / bootstrap)",
    },
    metrics: [
      { label: "Recall Latency", value: "21.4ms", delta: "Instant" },
      { label: "Context Window", value: "380 TK", delta: "-88% bloat" },
      { label: "Indexed Decisions", value: "4,820", delta: "Permanent" },
      { label: "Corrupted Nodes", value: "0", delta: "ACID Safe" },
    ],
    invariants: [
      "∀ q ∈ Query : Latency(FTS5(q)) < 50ms",
      "Tokens(BootstrapContext) ≤ 400 TK (Hard Upper Bound)",
      "MemoryLossOnReboot = 0% (ACID Persistent)",
      "RecallPrecision @ Rank1 ≥ 0.942",
    ],
    codeSnippet: `-- SQLite FTS5 Photographic Retrieval
SELECT content, score, timestamp 
FROM neural_memories_fts 
WHERE neural_memories_fts MATCH ? 
ORDER BY rank, timestamp DESC 
LIMIT 5;`,
    cliCommand: "aegis recall 'architectural invariants' --limit 3",
  },
  {
    id: "BP-03",
    code: "TOKEN_ARBITRAGE_ENGINE",
    title: "Deterministic Cost Pruner",
    subtitle: "Adaptive Complexity Scorer & Local Model Offloading",
    category: "FINOPS",
    icon: Flame,
    description:
      "Surgically detects task size. Micro-tasks (<15 lines) run instantly; macro tasks trigger local workers, routing 95.8% of generated lines through zero-cost tokens.",
    hierarchy: {
      tier1: "Complexity Heuristic: AST Diff Estimation & Line Threshold",
      tier2: "Routing Engine: Hermes CLI / Ollama Qwen2.5-Coder / OpenCode",
      tier3: "Quality Verifier: Automated Static Syntax & Type Checks",
    },
    metrics: [
      { label: "Monthly Saved", value: "$420.00", delta: "+92% ROI" },
      { label: "Local Tokens", value: "1.42M", delta: "Free local" },
      { label: "Frontier Tokens", value: "62K", delta: "Strategic only" },
      { label: "Execution Speed", value: "1.8s", delta: "Parallel" },
    ],
    invariants: [
      "MacroTask.TokenCost = $0.00 (Local Worker Generated)",
      "CoachingAttempts ≤ 3 ∨ EscalateToSenior(Task)",
      "AST.ValidationPasses = TRUE Before File Write",
      "Hardware Headroom: RAM > 3.5GB ∧ CPU < 85%",
    ],
    codeSnippet: `# Token Arbitrage Pipeline
if task.lines > 15:
    candidate = run_worker_cli("hermes", task.prompt)
    verified = run_quality_gates(candidate)
    commit_changes(verified)
else:
    surgical_edit(task)`,
    cliCommand: "aegis run --task 'generate auth boilerplate' --local-tokens",
  },
  {
    id: "BP-04",
    code: "WIN32_KEEPALIVE_DAEMON",
    title: "24/7 Background Supervisor",
    subtitle: "Self-Healing Win32 Task Scheduler & Health Sentinel",
    category: "RELIABILITY",
    icon: Cpu,
    description:
      "Backed by Windows Scheduled Task 'AegisBrainDaemonKeepAlive'. Runs persistently across reboots, account switches, and terminal closures with sub-second resurrection.",
    hierarchy: {
      tier1: "Supervisor: aegis.server HTTP Daemon (127.0.0.1:8765)",
      tier2: "Watchdog: Win32 Scheduled Task (5-min heartbeat trigger)",
      tier3: "Telegram Listener: Real-Time Event & Alert Dispatcher",
    },
    metrics: [
      { label: "Daemon Uptime", value: "99.98%", delta: "24/7 Live" },
      { label: "Heartbeat Period", value: "300s", delta: "Deterministic" },
      { label: "Resurrection Time", value: "<850ms", delta: "Instant" },
      { label: "Memory Overhead", value: "28.4MB", delta: "Ultra-lean" },
    ],
    invariants: [
      "DaemonStatus(HTTP_8765) = ALIVE ∨ SelfResurrect()",
      "TerminalCloseEvents.InterruptDaemon = FALSE",
      "NetworkFailure.ReconnectBackoff = Exponential(1.5, 30s)",
      "StateCheckpoints.Interval = 60s (Auto-Sync)",
    ],
    codeSnippet: `// Win32 KeepAlive Check
const res = await fetch("http://127.0.0.1:8765/health");
if (!res.ok) {
  await spawnDetachedProcess("aegis", ["start"]);
  console.log("Daemon resurrected in 820ms");
}`,
    cliCommand: "aegis status --daemon-verbose",
  },
  {
    id: "BP-05",
    code: "TELEGRAM_REMOTE_BRIDGE",
    title: "24/7 Mobile Telemetry Stream",
    subtitle: "In-Flight Keystroke Interrupt & Voice Note Transcoder",
    category: "REMOTE OPS",
    icon: Terminal,
    description:
      "Control your workstation from anywhere via Telegram (@HHAACLIBot). Send /type commands to steer in-flight coding sessions, stream live metrics, and ingest media.",
    hierarchy: {
      tier1: "Gateway: Telegram Long-Polling Listener",
      tier2: "Input Injector: Win32 Virtual Keycode Simulator",
      tier3: "Media Transcoder: Local Whisper Speech-to-Text & FFmpeg",
    },
    metrics: [
      { label: "Command Latency", value: "240ms", delta: "Real-time" },
      { label: "Voice STT Speed", value: "1.1s", delta: "Local Whisper" },
      { label: "In-Flight Interrupt", value: "Supported", delta: "/type /alt+m" },
      { label: "Offline Queue", value: "Zero Loss", delta: "Persistent" },
    ],
    invariants: [
      "∀ msg ∈ Telegram : AuthorizedChatID(msg) = TRUE",
      "VoiceNote → Transcribe(LocalWhisper) → DirectAction",
      "InFlightInterrupt.Latency < 500ms",
      "CompletionBanner.Emitted = TRUE on Task Finish",
    ],
    codeSnippet: `# In-flight typing injection via Win32
if text.endswith("/alt+m"):
    clean_text = text[:-6].strip()
    type_to_desktop(clean_text)
    simulate_alt_m()
    notify_telegram("Command injected successfully")`,
    cliCommand: "aegis remote --send 'status report'",
  },
  {
    id: "BP-06",
    code: "FORMAL_QUALITY_GATES",
    title: "4-Stage Formal Gate Pipeline",
    subtitle: "Karpathy Simplicity + Security Audit + Secret Scan + Dual-Env",
    category: "VERIFICATION",
    icon: ShieldAlert,
    description:
      "No candidate code reaches production without passing all four architectural gates: anti-slop cleaning, vulnerability checks, credential scanning, and dual-env testing.",
    hierarchy: {
      tier1: "Gate 1: Karpathy Simplicity (Surgical diff, zero speculative code)",
      tier2: "Gate 2: Anti-Slop (TurnItOut & Ponytail conversational purges)",
      tier3: "Gate 3 & 4: Red-Team Security Audit & Dual-Environment Tests",
    },
    metrics: [
      { label: "Pass Rate", value: "100%", delta: "Enforced" },
      { label: "Vulnerabilities", value: "0 Detected", delta: "Clean" },
      { label: "Leaked Secrets", value: "0", delta: "GitGuardian verified" },
      { label: "Dual-Env Verification", value: "Passed", delta: "Sandbox + Host" },
    ],
    invariants: [
      "∀ PR : HasPassingUnitTests(PR) ∧ SecretScan(PR) = CLEAN",
      "ShellExec.DangerousFlags = 0 (shell=True strictly blocked)",
      "UnusedImportsOrWrappers(File) = 0",
      "BuildExitCode = 0 (Next.js Turbopack production pass)",
    ],
    codeSnippet: `// 4-Stage Formal Gate Pipeline
export async function executeQualityGates(code: string): Promise<GateResult> {
  const g1 = verifyKarpathySimplicity(code);
  const g2 = purgeConversationalSlop(code);
  const g3 = scanVulnerabilitiesAndSecrets(code);
  const g4 = await runDualEnvironmentTests(code);
  return g1 && g2 && g3 && g4 ? { status: "PASS" } : { status: "REJECT" };
}`,
    cliCommand: "aegis challenge --target ./web --all-gates",
  },
  {
    id: "BP-07",
    code: "QUICKSTART_ENVIRONMENT_BOOT",
    title: "One-Click Sovereign Setup",
    subtitle: "Automated Tooling Shims & Self-Updating Arsenal",
    category: "BOOTSTRAP",
    icon: CheckCircle2,
    description:
      "One command configures global CLI shims, Win32 scheduled tasks, SQLite database schemas, and tool registries. Updates monthly via AST deep merge.",
    hierarchy: {
      tier1: "Installer: agy-skill-builder / aegis bootstrap",
      tier2: "Path Shims: ~/.local/bin registered in system PATH",
      tier3: "Auto-Update: AntigravityMonthlyUpdate (1st of month 02:00 AM)",
    },
    metrics: [
      { label: "Setup Time", value: "<15s", delta: "Turnkey" },
      { label: "Tracked Skills", value: "148", delta: "Self-updating" },
      { label: "External Deps", value: "0", delta: "Python stdlib" },
      { label: "Merge Conflicts", value: "0", delta: "AST Deep Merge" },
    ],
    invariants: [
      "BootstrapTime < 30s on Clean Windows Host",
      "DependencyCount = 0 (Zero npm/pip external requirements)",
      "MonthlyCron.Active = TRUE (Auto-Update Enabled)",
      "RestorePointCreated = TRUE Prior to Any Mutation",
    ],
    codeSnippet: `# Quickstart setup command
python package/aegis/bootstrap.py --install-all
aegis snapshot create --reason "initial-boot"
aegis status`,
    cliCommand: "aegis bootstrap --verify",
  },
];

export function Feature06BlueprintCards({
  className = "",
  initialBlueprintIndex = 0,
}: Feature06BlueprintCardsProps) {
  const [activeIdx, setActiveIdx] = useState<number>(
    Math.min(Math.max(initialBlueprintIndex, 0), BLUEPRINTS.length - 1)
  );
  const [copied, setCopied] = useState<boolean>(false);

  const bp = BLUEPRINTS[activeIdx];
  const IconComp = bp.icon;

  const handleCopy = (text: string) => {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <section
      className={`bg-[#070709] text-zinc-100 p-6 md:p-8 border-2 border-zinc-800 rounded-none font-sans selection:bg-[#B91C1C] selection:text-white ${className}`}
    >
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b-2 border-zinc-800 pb-5">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 bg-[#B91C1C] text-white px-2.5 py-1 border-2 border-black shadow-[3px_3px_0px_#000000]">
              <Layers className="w-3.5 h-3.5 stroke-[2.5]" />
              <span className="font-mono text-xs uppercase tracking-widest font-bold">
                SYSTEM BLUEPRINTS // LIVE ARCHITECTURAL PLATES
              </span>
            </div>
            <h2 className="text-2xl md:text-4xl font-black tracking-tight uppercase text-[#FAF8F5]">
              7 Interactive System Blueprints
            </h2>
          </div>

          <div className="flex items-center gap-2">
            <span className="font-mono text-xs text-zinc-400 uppercase tracking-widest">
              ACTIVE NODE:
            </span>
            <span className="font-mono text-xs text-[#FAF8F5] bg-[#101116] border-2 border-zinc-800 px-3 py-1 font-bold">
              {bp.code}
            </span>
          </div>
        </div>

        {/* 7-Tab Blueprint Selector */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2">
          {BLUEPRINTS.map((item, idx) => {
            const isSelected = idx === activeIdx;
            const ItemIcon = item.icon;
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => setActiveIdx(idx)}
                className={`text-left p-3 border-2 transition-all cursor-pointer ${
                  isSelected
                    ? "bg-[#FAF8F5] text-black border-black shadow-[3px_3px_0px_#B91C1C] -translate-y-0.5"
                    : "bg-[#101116] text-zinc-300 border-zinc-800 hover:border-zinc-700 hover:text-white"
                }`}
              >
                <div className="flex items-center justify-between mb-1.5">
                  <span className="font-mono text-[10px] uppercase tracking-widest opacity-75 font-bold">
                    {item.id}
                  </span>
                  <ItemIcon className="w-3.5 h-3.5" />
                </div>
                <div className="font-mono text-xs uppercase font-extrabold truncate">
                  {item.category}
                </div>
                <div className="text-[11px] font-medium truncate mt-0.5 opacity-85">
                  {item.title}
                </div>
              </button>
            );
          })}
        </div>

        {/* Active Blueprint Main Plate */}
        <div className="bg-[#FAF8F5] text-black border-2 border-black shadow-[6px_6px_0px_#000000] p-6 sm:p-8 space-y-6">
          {/* Plate Title Row */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b-2 border-black/15 pb-5">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-black text-[#FAF8F5] border-2 border-black shadow-[3px_3px_0px_#B91C1C] flex items-center justify-center shrink-0">
                <IconComp className="w-6 h-6 stroke-[2]" />
              </div>
              <div>
                <div className="inline-block bg-[#B91C1C] text-white font-mono text-[10px] uppercase font-bold px-2 py-0.5 mb-1">
                  {bp.id} • {bp.category}
                </div>
                <h3 className="font-charles-rosie text-2xl sm:text-3xl text-black uppercase tracking-tight">
                  {bp.title}
                </h3>
                <p className="font-gt-era text-sm text-black/75 font-medium mt-0.5">
                  {bp.subtitle}
                </p>
              </div>
            </div>

            <button
              type="button"
              onClick={() => handleCopy(bp.cliCommand)}
              className="inline-flex items-center gap-2 bg-black text-white hover:bg-neutral-800 font-mono text-xs px-3.5 py-2 border-2 border-black shadow-[2px_2px_0px_#B91C1C] cursor-pointer transition-colors shrink-0"
            >
              {copied ? (
                <>
                  <Check className="w-3.5 h-3.5 text-emerald-400" />
                  <span>COPIED COMMAND</span>
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5" />
                  <span>COPY CLI INVOKE</span>
                </>
              )}
            </button>
          </div>

          <p className="font-gt-era text-black/85 text-sm sm:text-base leading-relaxed">
            {bp.description}
          </p>

          {/* 3-Tier Hierarchy Flow */}
          <div className="bg-black text-[#FAF8F5] border-2 border-black p-4 space-y-2">
            <div className="font-mono text-[10px] uppercase tracking-widest text-zinc-400 font-bold mb-2 flex items-center gap-2">
              <Sparkles className="w-3.5 h-3.5 text-[#B91C1C]" />
              THREE-TIER EXECUTION HIERARCHY
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div className="bg-[#101116] border border-zinc-800 p-3">
                <div className="font-mono text-[10px] uppercase text-[#B91C1C] font-bold">
                  COGNITION LAYER
                </div>
                <div className="text-xs text-zinc-200 font-mono mt-1">
                  {bp.hierarchy.tier1}
                </div>
              </div>
              <div className="bg-[#101116] border border-zinc-800 p-3">
                <div className="font-mono text-[10px] uppercase text-zinc-400 font-bold">
                  VERIFICATION LEAD
                </div>
                <div className="text-xs text-zinc-200 font-mono mt-1">
                  {bp.hierarchy.tier2}
                </div>
              </div>
              <div className="bg-[#101116] border border-zinc-800 p-3">
                <div className="font-mono text-[10px] uppercase text-emerald-400 font-bold">
                  LOCAL EXECUTION
                </div>
                <div className="text-xs text-zinc-200 font-mono mt-1">
                  {bp.hierarchy.tier3}
                </div>
              </div>
            </div>
          </div>

          {/* Telemetry Metrics & Formal Invariants Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* 4 Telemetry Metrics */}
            <div className="space-y-2">
              <div className="font-mono text-xs uppercase tracking-widest font-extrabold text-black/75 flex items-center gap-2">
                <Activity className="w-4 h-4 text-[#B91C1C]" />
                TELEMETRY METRICS
              </div>
              <div className="grid grid-cols-2 gap-2.5">
                {bp.metrics.map((m, idx) => (
                  <div
                    key={idx}
                    className="bg-[#101116] text-[#FAF8F5] border-2 border-black p-3 shadow-[2px_2px_0px_#000000]"
                  >
                    <div className="font-mono text-[10px] uppercase tracking-wider text-zinc-400">
                      {m.label}
                    </div>
                    <div className="text-xl font-mono font-black text-white mt-1">
                      {m.value}
                    </div>
                    <div className="font-mono text-[10px] text-emerald-400 font-bold mt-0.5">
                      {m.delta}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* 4 Formal System Invariants */}
            <div className="space-y-2">
              <div className="font-mono text-xs uppercase tracking-widest font-extrabold text-black/75 flex items-center gap-2">
                <ShieldAlert className="w-4 h-4 text-[#B91C1C]" />
                VERIFIABLE MATHEMATICAL INVARIANTS
              </div>
              <div className="space-y-2">
                {bp.invariants.map((inv, idx) => (
                  <div
                    key={idx}
                    className="flex items-start gap-2.5 bg-white border-2 border-black p-2.5 shadow-[2px_2px_0px_#000000]"
                  >
                    <div className="font-mono text-[10px] font-bold bg-black text-[#FAF8F5] px-1.5 py-0.5 shrink-0">
                      INV-0{idx + 1}
                    </div>
                    <code className="font-mono text-xs text-black/90 font-semibold break-all leading-tight">
                      {inv}
                    </code>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Interactive Code Window */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <div className="font-mono text-xs uppercase tracking-widest font-extrabold text-black/75 flex items-center gap-2">
                <Terminal className="w-4 h-4 text-black" />
                DETERMINISTIC CODE INTERFACE
              </div>
              <code className="font-mono text-[11px] text-black/60 bg-black/5 px-2 py-0.5 border border-black/10">
                {bp.cliCommand}
              </code>
            </div>

            <div className="bg-[#070709] border-2 border-black p-4 overflow-x-auto shadow-[4px_4px_0px_#000000]">
              <pre className="font-mono text-xs text-emerald-400 leading-relaxed">
                <code>{bp.codeSnippet}</code>
              </pre>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
