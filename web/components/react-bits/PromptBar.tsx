"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import {
  Terminal,
  Cpu,
  CheckCircle2,
  Clock,
  Send,
  Database,
  ArrowRight,
  Repeat,
} from "lucide-react";
import "./PromptBar.css";

interface SimulationStep {
  command: string;
  model: string;
  tier: string;
  badge: string;
  latency: string;
  outputTitle: string;
  outputLines: string[];
  tokensSaved: string;
}

const SIMULATION_STEPS: SimulationStep[] = [
  {
    command: 'aegis recall "AST parser invariants"',
    model: "Gemini 4 Flash",
    tier: "Tier 1 Senior Boss",
    badge: "Cloud Brain",
    latency: "22 ms",
    outputTitle: "✓ 4 AST symbols retrieved from brain.db in 22ms (<25ms SLA)",
    outputLines: [
      "• ASTTaintChecker (src/gates/redteam_ast.py:16)",
      "• InvariantGuard.assert_no_shell(cmd) [PASS]",
      "• SymbolResolver.find_ast_nodes(\"invariants\") [Node #1409]",
      "• Zero context bloat: 380 tokens vs 54,200 tokens crawl",
    ],
    tokensSaved: "99.3% tokens saved",
  },
  {
    command: "aegis challenge src/engine.py",
    model: "Claude Opus 5.5",
    tier: "Tier 2 Subagent Gate",
    badge: "Security Audit",
    latency: "18 ms",
    outputTitle: "✓ 0 vulnerabilities detected (Cloudflare AST audit clean)",
    outputLines: [
      "• subprocess.run(shell=False) verified [Gate 03 PASS]",
      "• 0 API keys / secrets exposed in AST tree [GitGuardian PASS]",
      "• Karpathy simplicity: 12 lines diff [Fast-Path ≤15 Lines PASS]",
      "• Dual-env syntax compilation verified in isolated sandbox",
    ],
    tokensSaved: "Zero exploit vectors",
  },
  {
    command: "aegis briefing",
    model: "Fable Orchestrator",
    tier: "Tier 1 Boss",
    badge: "State Digest",
    latency: "24 ms",
    outputTitle: "✓ Snapshot snap-20261108 active • 24/7 daemon healthy (:8765)",
    outputLines: [
      "• 286/286 pytest unit tests passing [100% clean test suite]",
      "• Telegram bridge @HHAACLIBot active on Win32 host",
      "• Local worker pool: Hermes CLI (Idle), Ollama 7B (Ready)",
      "• $1,840/mo token savings active across 3-tier hierarchy",
    ],
    tokensSaved: "Host persistent",
  },
  {
    command: 'aegis delegate "Implement token counter"',
    model: "Hermes 3 (Local)",
    tier: "Tier 3 Worker",
    badge: "$0.00 / Token",
    latency: "180 ms",
    outputTitle: "✓ Hermes 3 generated candidate on host hardware ($0.00 cost)",
    outputLines: [
      "• Directive dispatched via run_command to local hermes CLI",
      "• 0 frontier tokens consumed • $0.00 billed to developer",
      "• 4-Decision Quality Architecture Gate: ALL 4 GATES PASSED",
      "• Coached to 9.4/10 confidence score in 1 verification loop",
    ],
    tokensSaved: "100% free tokens",
  },
];

export function PromptBar() {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [typedCommand, setTypedCommand] = useState("");
  const [phase, setPhase] = useState<"typing" | "dispatching" | "executing" | "complete">("typing");

  const currentStep = SIMULATION_STEPS[currentStepIndex];

  useEffect(() => {
    let charIndex = 0;
    const targetText = currentStep.command;
    setTypedCommand("");
    setPhase("typing");

    // Phase 1: Typing effect
    const typingInterval = setInterval(() => {
      if (charIndex <= targetText.length) {
        setTypedCommand(targetText.slice(0, charIndex));
        charIndex++;
      } else {
        clearInterval(typingInterval);
        // Phase 2: Dispatch trigger
        setPhase("dispatching");
        setTimeout(() => {
          // Phase 3: Executing
          setPhase("executing");
          setTimeout(() => {
            // Phase 4: Output Complete
            setPhase("complete");
            // Hold for 3.5 seconds then advance
            setTimeout(() => {
              setCurrentStepIndex((prev) => (prev + 1) % SIMULATION_STEPS.length);
            }, 3600);
          }, 350);
        }, 450);
      }
    }, 45);

    return () => clearInterval(typingInterval);
  }, [currentStepIndex]);

  return (
    <div className="w-full max-w-3xl mx-auto rounded-xl border-2 border-black bg-[#101116] shadow-[8px_8px_0px_#000000] overflow-hidden text-white font-mono text-xs">
      {/* Top Header Pill Bar */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-[#171822] border-b border-white/10">
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full bg-[#B91C1C]" />
          <div className="w-2.5 h-2.5 rounded-full bg-[#D4AF37]" />
          <div className="w-2.5 h-2.5 rounded-full bg-[#10B981]" />
          <span className="ml-2 font-bold text-white text-[11px] tracking-wider uppercase font-nikkei flex items-center gap-1.5">
            <Terminal className="w-3.5 h-3.5 text-[#D4AF37]" />
            Aegis Sovereign Prompt Simulator
          </span>
        </div>

        <div className="flex items-center gap-2">
          <span className="px-2 py-0.5 rounded bg-[#D4AF37]/20 border border-[#D4AF37]/40 text-[#D4AF37] font-bold text-[10px]">
            {currentStep.model}
          </span>
        </div>
      </div>

      {/* Interactive Command Input Line (Video/GIF Typewriter Simulation) */}
      <div className="p-4 sm:p-5 bg-[#0D0E14] space-y-3">
        <div className="flex items-center gap-2.5 px-3.5 py-3 rounded-lg bg-black border border-white/15 shadow-inner">
          <span className="text-[#D4AF37] font-bold text-sm select-none">&gt;_</span>
          <div className="flex-1 font-mono text-sm text-white flex items-center">
            <span>{typedCommand}</span>
            <span
              className={`inline-block w-2 h-4 ml-1 bg-[#B91C1C] ${
                phase === "typing" ? "animate-pulse" : "opacity-0"
              }`}
            />
          </div>

          <motion.div
            animate={{
              scale: phase === "dispatching" ? 0.92 : 1,
              backgroundColor: phase === "dispatching" ? "#B91C1C" : "#1A1B26",
            }}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded border border-white/20 text-[11px] font-bold text-white select-none transition-colors"
          >
            <Send className="w-3 h-3 text-[#D4AF37]" />
            <span className="hidden sm:inline">DISPATCH</span>
          </motion.div>
        </div>

        {/* Dynamic Execution Status & Trace */}
        <AnimatePresence mode="wait">
          {(phase === "executing" || phase === "complete") && (
            <motion.div
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -6 }}
              className="space-y-2 pt-1"
            >
              {/* Shimmer / Latency Header */}
              <div className="flex items-center justify-between text-[11px] px-2 py-1 rounded bg-[#171924] border border-white/10">
                <div className="flex items-center gap-2">
                  <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
                  </span>
                  <span className="text-zinc-300 font-bold">{currentStep.tier}</span>
                  <span className="text-zinc-600">•</span>
                  <span className="text-[#D4AF37]">{currentStep.badge}</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-emerald-400 font-bold">{currentStep.tokensSaved}</span>
                  <span className="text-white font-bold bg-black px-2 py-0.5 rounded border border-white/10">
                    {currentStep.latency}
                  </span>
                </div>
              </div>

              {/* Output Content Terminal Box */}
              {phase === "complete" && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="p-3.5 rounded-lg bg-[#07080C] border border-emerald-500/30 space-y-1.5 font-mono text-[11px]"
                >
                  <div className="text-emerald-400 font-bold flex items-center gap-1.5 pb-1 border-b border-white/10">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    {currentStep.outputTitle}
                  </div>
                  {currentStep.outputLines.map((line, idx) => (
                    <div key={idx} className="text-zinc-300 pl-2">
                      {line}
                    </div>
                  ))}
                </motion.div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Footer Indicators */}
      <div className="flex items-center justify-between px-4 py-2 bg-[#14151E] border-t border-white/10 text-[10px] text-zinc-500 font-gt-era">
        <div className="flex items-center gap-3">
          <span>Engine: <code className="text-zinc-400">brain.db (WAL)</code></span>
          <span>•</span>
          <span>Daemon: <code className="text-emerald-400">127.0.0.1:8765</code></span>
        </div>
        <div className="flex items-center gap-1 text-[#D4AF37]">
          <span>Scenario {currentStepIndex + 1} of {SIMULATION_STEPS.length}</span>
        </div>
      </div>
    </div>
  );
}
