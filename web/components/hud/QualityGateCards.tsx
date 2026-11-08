"use client";

import React, { useState } from "react";
import { triggerSoundEffect } from "@/components/audio/SoundtrackController";
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
  badgeStyle: string;
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
    badgeStyle: "bg-black text-[#D4AF37] border-black",
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
    badgeStyle: "bg-emerald-950 text-emerald-300 border-emerald-600",
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
    badgeStyle: "bg-[#B91C1C] text-white border-black",
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
    badgeStyle: "bg-black text-[#D4AF37] border-black",
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

  return (
    <div className="relative p-6 sm:p-8 bg-[#101116] text-[#FBF9F5] border-2 border-black rounded-lg">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-black/40">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#B91C1C] text-white font-nikkei text-xs uppercase tracking-widest shadow-[2px_2px_0px_#000000]">
            <ShieldAlert className="w-3.5 h-3.5" />
            <span>FOUR-TIER PRODUCTION SAFETY</span>
          </div>
          <h3 className="text-2xl sm:text-3xl font-charles-rosie text-white uppercase tracking-tight mt-2">
            The 4-Decision Quality Architecture Gate
          </h3>
          <p className="text-xs sm:text-sm text-zinc-200 font-sans font-medium max-w-xl mt-1 leading-relaxed">
            Before any candidate code from local workers or subagents reaches production, it must pass all 4 rigorous
            architectural and security filters.
          </p>
        </div>

        <div className="px-4 py-2 bg-black border-2 border-black rounded text-center shadow-[3px_3px_0px_#B91C1C]">
          <div className="font-nikkei text-xl sm:text-2xl font-extrabold text-[#D4AF37]">
            4/4 GATES
          </div>
          <div className="text-[10px] font-mono uppercase text-zinc-400">Strict Enforcement</div>
        </div>
      </div>

      {/* Graphic Novel Narration Box matching Santioni style */}
      <div className="narration-box my-4">
        <p className="narration-text">
          FOUR GATES OF STEEL STAND GUARD. SURGICAL SIMPLICITY, ZERO SLOP WATERMARKS, AST INJECTION BLOCKING, AND DUAL-ENVIRONMENT PROOF.
        </p>
      </div>

      {/* Gate Tabs Selector */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 my-6">
        {GATES.map((gate) => {
          const isSelected = selectedGate === gate.id;
          const Icon = gate.icon;
          return (
            <button
              key={gate.id}
              type="button"
              onClick={() => {
                setSelectedGate(gate.id);
                setExpandedDiff(gate.id);
              }}
              className={`p-4 rounded-lg border-2 text-left transition-all cursor-pointer ${
                isSelected
                  ? "bg-[#181822] border-[#B91C1C] shadow-[4px_4px_0px_#B91C1C]"
                  : "bg-black/40 border-black hover:bg-black/60 shadow-[2px_2px_0px_#000000]"
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-mono text-xs font-bold text-[#D4AF37]">GATE {gate.number}</span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${gate.badgeStyle}`}>
                  {gate.badge}
                </span>
              </div>
              <div className="font-nikkei font-bold uppercase text-white text-sm tracking-wide">
                {gate.title}
              </div>
              <div className="text-[11px] text-zinc-400 font-gt-era mt-1">
                {gate.subtitle}
              </div>
            </button>
          );
        })}
      </div>

      {/* Active Gate Deep Dive Plate */}
      <div className="p-6 sm:p-8 rounded-lg bg-[#FAF8F5] text-black border-2 border-black shadow-[6px_6px_0px_#000000] space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b-2 border-black pb-4">
          <div>
            <div className="font-nikkei text-xs uppercase text-[#B91C1C] font-extrabold tracking-wider">
              GATE {active.number} • COMPLIANCE AUDIT
            </div>
            <h4 className="font-charles-rosie text-2xl text-black uppercase tracking-tight mt-1">
              {active.title}
            </h4>
          </div>
          <span className={`px-3 py-1 rounded text-xs font-mono font-bold border-2 ${active.badgeStyle} shadow-[2px_2px_0px_#000000]`}>
            {active.badge}
          </span>
        </div>

        <p className="font-gt-era text-sm text-black/80 leading-relaxed">
          {active.description}
        </p>

        {/* Invariants Grid */}
        <div>
          <div className="font-nikkei text-xs uppercase tracking-wider text-black font-extrabold mb-3">
            Strict Architecture Invariants:
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            {active.invariants.map((inv, idx) => (
              <div
                key={idx}
                className="flex items-start gap-2 p-2.5 bg-white border border-black shadow-[2px_2px_0px_#000000] text-xs font-gt-era"
              >
                <CheckCircle2 className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
                <span className="font-medium text-black">{inv}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Before / After Code Diff */}
        <div>
          <div className="font-nikkei text-xs uppercase tracking-wider text-black font-extrabold mb-3">
            Real-Time AST Filter Diff:
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono text-xs">
            {/* Rejected */}
            <div className="p-4 bg-[#14141A] text-red-200 border-2 border-black shadow-[4px_4px_0px_#B91C1C] rounded">
              <div className="text-[11px] font-nikkei uppercase font-extrabold text-[#B91C1C] mb-2 border-b border-white/10 pb-1">
                Rejected by Gate
              </div>
              <pre className="whitespace-pre-wrap leading-relaxed overflow-x-auto text-[11px]">
                {active.codeDiff.rejected}
              </pre>
            </div>

            {/* Approved */}
            <div className="p-4 bg-[#14141A] text-emerald-200 border-2 border-black shadow-[4px_4px_0px_#10B981] rounded">
              <div className="text-[11px] font-nikkei uppercase font-extrabold text-emerald-400 mb-2 border-b border-white/10 pb-1">
                Approved by Gate
              </div>
              <pre className="whitespace-pre-wrap leading-relaxed overflow-x-auto text-[11px]">
                {active.codeDiff.approved}
              </pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
