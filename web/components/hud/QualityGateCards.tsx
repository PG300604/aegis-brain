"use client";

import React, { useState } from "react";
import {
  ShieldAlert,
  Sparkles,
  Zap,
  CheckCircle2,
  Lock,
  Layers,
  ArrowRight,
  Code,
  FileCheck,
  Terminal,
  Cpu,
  ChevronDown,
  ChevronUp,
} from "lucide-react";

interface QualityGate {
  id: string;
  number: string;
  title: string;
  subtitle: string;
  badge: string;
  badgeColor: "cyan" | "emerald" | "amber" | "purple";
  icon: React.ElementType;
  description: string;
  invariants: string[];
  codeDiff: {
    rejected: string;
    approved: string;
  };
}

const GATES: QualityGate[] = [
  {
    id: "karpathy",
    number: "01",
    title: "Karpathy Simplicity Doctrine",
    subtitle: "Zero Speculative Abstraction",
    badge: "< 15 Lines Diff Fast-Path",
    badgeColor: "cyan",
    icon: Zap,
    description:
      "Every changed line must directly trace to the explicit requirement. For micro-tasks (≤15 lines), Tier 2 executes surgically with zero worker spawn overhead. Zero unnecessary wrappers or premature generalizations.",
    invariants: [
      "No abstractions for single-use functions",
      "No 'configurability' or speculative flexibility that wasn't requested",
      "Surgical edits: never refactor adjacent working code",
      "Fast-path ≤15 lines: bypass heavy CLI spawn latency",
    ],
    codeDiff: {
      rejected: `// ❌ Rejected (Over-engineered wrapper)\nclass AbstractConnectionPoolManagerFactorySingleton {\n  constructor(config: GenericProviderInterface) { ... }\n}`,
      approved: `// ✓ Approved (Karpathy Simplicity)\nexport function connectDb(url: string) {\n  return new Database(url);\n}`,
    },
  },
  {
    id: "unslop",
    number: "02",
    title: "Ponytail & TurnItOut Scrubber",
    subtitle: "Zero Conversational Residue",
    badge: "100% Watermark Free",
    badgeColor: "emerald",
    icon: Sparkles,
    description:
      "Automated sanitizer scrubbing all polite AI filler, sycophancy, 'Certainly!', 'I have updated...', and conversational watermarks from generated candidate files, leaving dense, production-grade source code.",
    invariants: [
      "100% removal of AI preambles and apologetic tone",
      "Zero repetitive explanatory comments explaining trivial syntax",
      "Dense, professional, human-equivalent engineering output",
      "Clean AST docstrings adhering strictly to PEP-257 / TSDoc",
    ],
    codeDiff: {
      rejected: `// ❌ Rejected (Conversational AI Slop)\n// Certainly! Here is the updated code that fulfills your request.\n// I made sure to add great comments for you:\nlet x = 1; // assigning 1 to x`,
      approved: `// ✓ Approved (Clean Production Code)\nconst retryAttempts = 3;\nawait executeWithRetry(fn, retryAttempts);`,
    },
  },
  {
    id: "security",
    number: "03",
    title: "Red-Team Security & Cloudflare Defense",
    subtitle: "AST Taint & Injection Firewall",
    badge: "0 Shell Injection Tolerance",
    badgeColor: "purple",
    icon: ShieldAlert,
    description:
      "Deep AST static analysis catches vulnerabilities before compilation. Zero tolerance for `shell=True`, unsanitized subprocesses, path traversals, and hardcoded secrets with GitGuardian entropy scanning.",
    invariants: [
      "Strict prohibition of `shell=True`, `os.system`, and eval()",
      "AST taint analysis on all subprocess inputs and external query params",
      "GitGuardian entropy scan blocking exposed API keys and JWTs",
      "Cloudflare Zero-Trust network boundary compliance",
    ],
    codeDiff: {
      rejected: `// ❌ Rejected (Severe Vulnerability)\nsubprocess.Popen(f"ping {user_ip}", shell=True)\napi_key = "sk_live_9948271038194"`,
      approved: `// ✓ Approved (Secure AST Parameterized)\nsubprocess.run(["ping", "-c", "1", sanitized_ip], check=True)\napi_key = os.environ["API_KEY"]`,
    },
  },
  {
    id: "verification",
    number: "04",
    title: "Dual-Environment Verification",
    subtitle: "Isolated Sandbox to Local Verification",
    badge: "100% Test Pass Gate",
    badgeColor: "amber",
    icon: FileCheck,
    description:
      "Every candidate draft is compiled and tested inside an isolated virtual sandbox first. Only when 100% of unit and integration tests pass is code merged into the local workspace and signed for deployment.",
    invariants: [
      "Isolated sandboxed virtual environment dry-run first",
      "Local host environment verification second",
      "Zero git commit or push until all static and unit gates pass",
      "Automated restore-point snapshot rollback on test regression",
    ],
    codeDiff: {
      rejected: `// ❌ Rejected (Unverified Blind Push)\ngit commit -m "update stuff" && git push origin main\n// Result: CI Pipeline Failed with 3 fatal errors`,
      approved: `// ✓ Approved (Dual-Environment Verified)\n1. Sandbox: npx tsc --noEmit [PASS]\n2. Local: pytest tests/ [100% PASS]\n3. Signed & pushed with verified snapshot #104`,
    },
  },
];

export function QualityGateCards() {
  const [selectedGate, setSelectedGate] = useState<string>("karpathy");
  const [expandedDiff, setExpandedDiff] = useState<string | null>("karpathy");

  const active = GATES.find((g) => g.id === selectedGate) || GATES[0];

  const getBadgeStyle = (color: string) => {
    switch (color) {
      case "cyan":
        return "bg-cyan-950/70 border-cyan-500/40 text-cyan-400";
      case "emerald":
        return "bg-emerald-950/70 border-emerald-500/40 text-emerald-400";
      case "purple":
        return "bg-purple-950/70 border-purple-500/40 text-purple-400";
      case "amber":
        return "bg-amber-950/70 border-amber-500/40 text-amber-400";
      default:
        return "bg-zinc-800 border-zinc-700 text-zinc-300";
    }
  };

  return (
    <section id="quality-gates" className="relative py-20 px-4 sm:px-6 max-w-6xl mx-auto">
      {/* Background radial glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[650px] h-[350px] bg-purple-500/10 blur-[140px] rounded-full pointer-events-none" />

      {/* Section Header */}
      <div className="text-center mb-12 space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-950/60 border border-purple-500/30 text-purple-400 font-mono text-xs">
          <ShieldAlert className="w-3.5 h-3.5" />
          <span>FOUR-TIER PRODUCTION SAFETY</span>
        </div>
        <h2 className="text-3xl sm:text-4xl font-bold tracking-tight text-white font-mono">
          The 4-Decision Quality Architecture Gate
        </h2>
        <p className="text-sm sm:text-base text-zinc-400 max-w-2xl mx-auto">
          Before any candidate code from local workers or subagents reaches production, it must pass all 4 rigorous
          architectural and security filters.
        </p>
      </div>

      {/* 4 Holographic Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {GATES.map((gate) => {
          const Icon = gate.icon;
          const isSelected = selectedGate === gate.id;

          return (
            <div
              key={gate.id}
              onClick={() => {
                setSelectedGate(gate.id);
                setExpandedDiff(expandedDiff === gate.id ? null : gate.id);
              }}
              className={`glass-panel p-5 rounded-2xl border cursor-pointer transition-all duration-300 relative overflow-hidden flex flex-col justify-between group ${
                isSelected
                  ? "border-cyan-400/80 shadow-[0_0_25px_rgba(0,240,255,0.2)] bg-[#0d101a]/90 scale-[1.02]"
                  : "border-white/10 hover:border-white/20 hover:bg-white/[0.03]"
              }`}
            >
              <div>
                {/* Top Number & Badge */}
                <div className="flex items-center justify-between mb-4">
                  <span className="font-mono text-2xl font-black text-zinc-600 group-hover:text-zinc-400 transition-colors">
                    {gate.number}
                  </span>
                  <span
                    className={`font-mono text-[10px] px-2 py-0.5 rounded-full border font-medium ${getBadgeStyle(
                      gate.badgeColor
                    )}`}
                  >
                    {gate.badge}
                  </span>
                </div>

                {/* Icon & Title */}
                <div className="flex items-center gap-2.5 mb-2">
                  <div
                    className={`p-2 rounded-lg bg-white/5 border border-white/10 ${
                      isSelected ? "border-cyan-400/40 text-cyan-400" : "text-zinc-400"
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                  </div>
                  <h3 className="font-bold text-sm text-white font-mono leading-snug">
                    {gate.title}
                  </h3>
                </div>

                <p className="text-[11px] text-zinc-400 font-mono mb-3">{gate.subtitle}</p>

                <p className="text-xs text-zinc-400 line-clamp-3 leading-relaxed">
                  {gate.description}
                </p>
              </div>

              {/* Card Footer */}
              <div className="mt-4 pt-3 border-t border-white/5 flex items-center justify-between text-[11px] font-mono text-cyan-400">
                <span>View Invariants</span>
                <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
              </div>
            </div>
          );
        })}
      </div>

      {/* Expanded Detail Panel for Selected Gate */}
      <div className="glass-panel-glow rounded-2xl p-6 sm:p-8 border border-cyan-500/30 shadow-2xl">
        <div className="flex flex-col lg:flex-row items-start justify-between gap-6 pb-6 border-b border-white/10">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="font-mono text-xs px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-500/30">
                GATE #{active.number} DEEP DIVE
              </span>
              <span className="font-mono text-xs text-zinc-500">• {active.badge}</span>
            </div>
            <h3 className="text-2xl font-bold font-mono text-white mt-1">
              {active.title}
            </h3>
            <p className="text-xs sm:text-sm text-zinc-400 mt-1 max-w-xl">
              {active.description}
            </p>
          </div>

          {/* Invariants Checklist */}
          <div className="w-full lg:w-auto min-w-[280px] p-4 rounded-xl bg-black/60 border border-white/10 space-y-2 font-mono text-xs">
            <div className="text-zinc-400 font-bold uppercase tracking-wider text-[10px]">
              Gate Invariants Enforced:
            </div>
            {active.invariants.map((inv, idx) => (
              <div key={idx} className="flex items-start gap-2 text-zinc-300 text-[11px]">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0 mt-0.5" />
                <span>{inv}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Live Code Diff: Rejected vs Approved */}
        <div className="mt-6">
          <div className="flex items-center gap-2 mb-3">
            <Code className="w-4 h-4 text-cyan-400" />
            <h4 className="font-mono text-xs font-bold uppercase tracking-wider text-zinc-300">
              Live AST Audit Comparison (Rejected vs. Approved)
            </h4>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Rejected candidate */}
            <div className="rounded-xl overflow-hidden border border-rose-500/30 bg-[#070305]/95 p-4 font-mono text-xs">
              <div className="text-rose-400 font-bold flex items-center justify-between pb-2 border-b border-rose-500/20 mb-3">
                <span>REJECTED CANDIDATE</span>
                <span className="text-[10px] bg-rose-950/80 px-2 py-0.5 rounded text-rose-300">BLOCKED</span>
              </div>
              <pre className="text-rose-200/90 whitespace-pre-wrap leading-relaxed overflow-x-auto text-[11px]">
                {active.codeDiff.rejected}
              </pre>
            </div>

            {/* Approved candidate */}
            <div className="rounded-xl overflow-hidden border border-emerald-500/30 bg-[#020705]/95 p-4 font-mono text-xs">
              <div className="text-emerald-400 font-bold flex items-center justify-between pb-2 border-b border-emerald-500/20 mb-3">
                <span>APPROVED &amp; SIGNED</span>
                <span className="text-[10px] bg-emerald-950/80 px-2 py-0.5 rounded text-emerald-300">PASSED</span>
              </div>
              <pre className="text-emerald-200/90 whitespace-pre-wrap leading-relaxed overflow-x-auto text-[11px]">
                {active.codeDiff.approved}
              </pre>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default QualityGateCards;
