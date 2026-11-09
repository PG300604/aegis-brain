"use client";

import React, { useState } from "react";
import { triggerSoundEffect } from "@/components/audio/SoundtrackController";
import { CheckCircle2, Terminal } from "lucide-react";

interface QualityGate {
  id: string;
  number: string;
  title: string;
  subtitle: string;
  tag: string;
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
    tag: "SIMPLICITY",
    description:
      "Every single changed line must directly trace to what you asked. For small edits under 15 lines, changes happen surgically with zero heavy tool overhead. No premature factories, no single-use abstractions, and no speculative flexibility.",
    invariants: [
      "No abstractions for single-use functions",
      "No speculative flexibility or unused configurability",
      "Surgical edits: never refactor adjacent working code",
      "Fast-path execution: avoid heavy CLI overhead for tiny fixes",
    ],
    codeDiff: {
      rejected: `// ❌ Rejected (Over-engineered wrapper)\nclass AbstractConnectionPoolManagerFactorySingleton {\n  constructor(config: GenericProviderInterface) { ... }\n}`,
      approved: `// ✓ Approved (Karpathy Simplicity)\nexport function connectDb(url: string) {\n  return new Database(url);\n}`,
    },
  },
  {
    id: "unslop",
    number: "02",
    title: "Conversational Watermark Scrubber",
    subtitle: "Dense Human-Grade Code",
    tag: "UNSLOP",
    description:
      "Removes all artificial AI filler, apologies, 'Certainly!', 'I have updated...', and conversational residue from candidate drafts, delivering clean, production-grade source code indistinguishable from a senior human engineer.",
    invariants: [
      "100% removal of AI preambles and apologetic tone",
      "Zero redundant explanatory comments for trivial syntax",
      "Clean, professional, human-equivalent code style",
      "Docstrings strictly follow standard engineering conventions",
    ],
    codeDiff: {
      rejected: `// ❌ Rejected (Conversational AI Slop)\n// Certainly! Here is the updated code that fulfills your request.\n// I made sure to add great comments for you:\nlet x = 1; // assigning 1 to x`,
      approved: `// ✓ Approved (Clean Production Code)\nconst retryAttempts = 3;\nawait executeWithRetry(fn, retryAttempts);`,
    },
  },
  {
    id: "security",
    number: "03",
    title: "Red-Team Security & Injection Defense",
    subtitle: "AST Parameterization & Secret Protection",
    tag: "SECURITY",
    description:
      "Static code analysis catches vulnerabilities before compilation. Zero tolerance for dangerous shell invocations, unsanitized subprocesses, path traversals, or committed secrets and API credentials.",
    invariants: [
      "Strict ban on unsafe shell executions (shell=True, os.system)",
      "Taint analysis on all subprocess inputs and external parameters",
      "Entropy scan preventing leaked API keys and private tokens",
      "Strict process boundary compliance across all child workers",
    ],
    codeDiff: {
      rejected: `// ❌ Rejected (Severe Vulnerability)\nsubprocess.Popen(f"ping {user_ip}", shell=True)\napi_key = "sk_live_9948271038194"`,
      approved: `// ✓ Approved (Secure AST Parameterized)\nsubprocess.run(["ping", "-c", "1", sanitized_ip], check=True)\napi_key = os.environ["API_KEY"]`,
    },
  },
  {
    id: "verification",
    number: "04",
    title: "Dual-Environment Verification Gate",
    subtitle: "Isolated Sandbox & Local Host Testing",
    tag: "VERIFICATION",
    description:
      "No code is committed or delivered until it compiles cleanly in an isolated sandbox, passes all test invariants, and verifies in the host runtime with zero regressions.",
    invariants: [
      "Sandboxed trial compilation before touching host files",
      "All 286 automated tests must pass with 100% parity",
      "Deterministic verification gate before git commit",
      "Zero broken imports or untested breaking mutations",
    ],
    codeDiff: {
      rejected: `// ❌ Rejected (Unverified Candidate)\ngit.commit("Fix bug") // Tests skipped, syntax unverified`,
      approved: `// ✓ Approved (Dual-Environment Verified)\npytest tests/ -> 286 passed in 53s\nnpm run build -> Compiled with 0 errors\ngit.commit("fix: verified with passing tests")`,
    },
  },
];

export function QualityGateCards() {
  const [selectedGate, setSelectedGate] = useState<string>("karpathy");

  const active = GATES.find((g) => g.id === selectedGate) || GATES[0];

  return (
    <div className="relative p-6 sm:p-10 bg-[#101116] text-[#FBF9F5] border-2 border-black rounded-xl shadow-[8px_8px_0px_#000000]">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-white/10">
        <div>
          <div className="border-l-2 border-[#B91C1C] pl-2 font-nikkei text-xs uppercase tracking-[0.2em] text-[#B91C1C] font-extrabold">
            INSPECTION SPECIFICATION
          </div>
          <h3 className="text-2xl sm:text-3xl font-charles-rosie text-white uppercase tracking-tight mt-2">
            The Four Quality Architecture Gates
          </h3>
          <p className="text-xs sm:text-sm text-zinc-300 font-gt-era max-w-2xl mt-1 leading-relaxed">
            Four automated safety filters catch bad code, strip AI apologies, and test every line in an isolated sandbox before touching your git tree.
          </p>
        </div>

        <div className="px-5 py-2.5 bg-black border-2 border-white/20 rounded text-center shadow-[3px_3px_0px_#B91C1C]">
          <div className="font-nikkei text-xl sm:text-2xl font-extrabold text-[#D4AF37]">
            4 INSPECTION GATES
          </div>
          <div className="text-[10px] font-gt-era uppercase text-zinc-400">Continuous Enforcement</div>
        </div>
      </div>

      {/* Gate Panels Selector (Clean Graphic Novel Style - Zero Pills) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 my-6">
        {GATES.map((gate) => {
          const isSelected = selectedGate === gate.id;
          return (
            <button
              key={gate.id}
              type="button"
              onClick={() => {
                setSelectedGate(gate.id);
                triggerSoundEffect("tab");
              }}
              className={`p-5 rounded-lg border-2 text-left transition-all cursor-pointer ${
                isSelected
                  ? "bg-[#181822] border-[#B91C1C] shadow-[5px_5px_0px_#B91C1C] translate-y-[-2px]"
                  : "bg-black/60 border-white/15 hover:border-white/40 shadow-[2px_2px_0px_#000000]"
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-nikkei text-xs font-bold text-[#D4AF37]">
                  STAGE {gate.number}
                </span>
                <span className={`font-mono text-[10px] font-bold px-1.5 py-0.5 rounded ${
                  isSelected ? "bg-[#B91C1C] text-white" : "bg-black text-zinc-500"
                }`}>
                  [{gate.tag}]
                </span>
              </div>
              <div className="font-nikkei font-bold uppercase text-white text-sm tracking-wide">
                {gate.title}
              </div>
              <div className="text-xs text-zinc-400 font-gt-era mt-1.5 leading-snug">
                {gate.subtitle}
              </div>
            </button>
          );
        })}
      </div>

      {/* Active Gate Deep Dive Plate */}
      <div className="p-6 sm:p-8 rounded-xl bg-[#FAF8F5] text-black border-2 border-black shadow-[6px_6px_0px_#000000] space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b-2 border-black pb-4">
          <div>
            <div className="font-nikkei text-xs uppercase text-[#B91C1C] font-extrabold tracking-wider">
              FILTER {active.number} • VERIFICATION SPECIFICATION
            </div>
            <h4 className="font-charles-rosie text-2xl sm:text-3xl text-black uppercase tracking-tight mt-1">
              {active.title}
            </h4>
          </div>
          <div className="text-xs font-gt-era font-bold uppercase text-black/60">
            Automated Architecture Check
          </div>
        </div>

        <p className="font-gt-era text-sm sm:text-base text-black/85 leading-relaxed">
          {active.description}
        </p>

        {/* Invariants Grid */}
        <div>
          <div className="font-nikkei text-xs uppercase tracking-wider text-black font-extrabold mb-3">
            Core Invariants Guaranteed:
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {active.invariants.map((inv, idx) => (
              <div
                key={idx}
                className="flex items-start gap-2.5 p-3 rounded bg-white border border-black shadow-[2px_2px_0px_#000000]"
              >
                <CheckCircle2 className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
                <span className="font-gt-era text-xs font-medium text-black/90">{inv}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Code Diff Demonstration */}
        <div className="pt-2">
          <div className="font-nikkei text-xs uppercase tracking-wider text-black font-extrabold mb-3">
            Before &amp; After Inspection:
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono text-xs">
            {/* Rejected */}
            <div className="p-4 rounded bg-[#1A0A0A] border-2 border-[#B91C1C] shadow-[3px_3px_0px_#000000] text-red-200">
              <div className="font-nikkei text-[11px] text-[#B91C1C] uppercase font-bold mb-2 flex items-center justify-between">
                <span>REJECTED DRAFT</span>
                <span className="text-[10px] text-red-400">Violates Gate {active.number}</span>
              </div>
              <pre className="overflow-x-auto whitespace-pre-wrap leading-relaxed text-[11px]">
                {active.codeDiff.rejected}
              </pre>
            </div>

            {/* Approved */}
            <div className="p-4 rounded bg-[#0A1A10] border-2 border-emerald-600 shadow-[3px_3px_0px_#000000] text-emerald-200">
              <div className="font-nikkei text-[11px] text-emerald-400 uppercase font-bold mb-2 flex items-center justify-between">
                <span>APPROVED PRODUCTION CODE</span>
                <span className="text-[10px] text-emerald-300">Verified</span>
              </div>
              <pre className="overflow-x-auto whitespace-pre-wrap leading-relaxed text-[11px]">
                {active.codeDiff.approved}
              </pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
