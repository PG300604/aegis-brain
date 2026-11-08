"use client";

import React, { useState, useId } from "react";
import {
  DollarSign,
  TrendingUp,
  Cpu,
  Layers,
  Sparkles,
  Bot,
  ShieldCheck,
  Zap,
  ArrowRight,
  Calculator,
} from "lucide-react";

export function ArbitrageCalculator() {
  const [turns, setTurns] = useState<number>(250);
  const [selectedWorker, setSelectedWorker] = useState<string>("hermes");
  const sliderId = useId();

  // Dynamic pricing formulas:
  // Direct Frontier Spend: ~ $0.128 per turn (assuming ~16k tokens in/out on high reasoning models) * turns * 30 days
  const frontierMonthly = Math.round(turns * 0.128 * 30);

  // Aegis 3-Tier Arbitrage Spend: Only ~8% frontier tokens for architectural planning & coaching:
  // ~ $0.0102 per turn * turns * 30 days
  const aegisMonthly = Math.round(turns * 0.0102 * 30);

  // Monthly Savings:
  const monthlySavings = frontierMonthly - aegisMonthly;
  const annualSavings = monthlySavings * 12;
  const reductionPercentage = Math.round(((frontierMonthly - aegisMonthly) / frontierMonthly) * 100);

  const workers = [
    { id: "hermes", name: "Hermes Agent CLI", model: "Hermes-3 Llama-3.1 8B", cost: "$0.00 / token" },
    { id: "ollama", name: "Ollama Local MoE", model: "Qwen2.5-Coder 7B", cost: "$0.00 / token" },
    { id: "opencode", name: "OpenCode Engine", model: "DeepSeek-Coder V2", cost: "$0.00 / token" },
  ];

  return (
    <section id="arbitrage" className="relative py-20 px-4 sm:px-6 max-w-6xl mx-auto">
      {/* Background glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-emerald-500/10 blur-[140px] rounded-full pointer-events-none" />

      {/* Section Header */}
      <div className="text-center mb-12 space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-950/60 border border-emerald-500/30 text-emerald-400 font-mono text-xs">
          <Calculator className="w-3.5 h-3.5" />
          <span>TOKEN ARBITRAGE SIMULATOR</span>
        </div>
        <h2 className="text-3xl sm:text-4xl font-bold tracking-tight text-white font-mono">
          Dynamic Token Arbitrage Calculator
        </h2>
        <p className="text-sm sm:text-base text-zinc-400 max-w-2xl mx-auto">
          Offload 92% of verbose boilerplate generation to free local workers (Hermes, Ollama, OpenCode).
          Reserve precious frontier cognition exclusively for architecture, invariants, and coaching.
        </p>
      </div>

      {/* Main Calculator Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
        {/* Left Controller Panel (7 cols) */}
        <div className="lg:col-span-7 glass-panel p-6 sm:p-8 rounded-2xl border border-white/10 space-y-8 shadow-2xl">
          {/* Turns Slider */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <label htmlFor={sliderId} className="font-mono text-xs font-semibold uppercase tracking-wider text-zinc-300">
                Daily Developer Interaction Turns
              </label>
              <div className="font-mono text-base font-bold text-cyan-400 px-3 py-1 rounded-lg bg-cyan-950/60 border border-cyan-500/30">
                {turns.toLocaleString()} turns / day
              </div>
            </div>

            <input
              id={sliderId}
              type="range"
              min={50}
              max={1000}
              step={25}
              value={turns}
              aria-label="Daily developer turns slider"
              onChange={(e) => setTurns(Number(e.target.value))}
              className="w-full h-2 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-cyan-400 hover:accent-cyan-300 transition-all"
            />

            <div className="flex justify-between text-[11px] font-mono text-zinc-500 mt-2">
              <span>50 (Solo Dev)</span>
              <span>250 (Active Engineer)</span>
              <span>500 (Pair Team)</span>
              <span>1,000 (Org Swarm)</span>
            </div>
          </div>

          {/* Local Worker Engine Selector */}
          <div>
            <span className="block font-mono text-xs font-semibold uppercase tracking-wider text-zinc-300 mb-3">
              Active Tier 3 Execution Worker
            </span>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
              {workers.map((w) => {
                const active = selectedWorker === w.id;
                return (
                  <button
                    key={w.id}
                    onClick={() => setSelectedWorker(w.id)}
                    className={`p-3 rounded-xl border font-mono text-left transition-all ${
                      active
                        ? "bg-cyan-500/10 border-cyan-400/80 shadow-[0_0_15px_rgba(0,240,255,0.15)]"
                        : "bg-black/40 border-white/5 hover:border-white/10 hover:bg-white/5"
                    }`}
                  >
                    <div className="text-xs font-bold text-white flex items-center justify-between">
                      <span className={active ? "text-cyan-300" : ""}>{w.name}</span>
                      {active && <span className="h-1.5 w-1.5 rounded-full bg-cyan-400 animate-pulse" />}
                    </div>
                    <div className="text-[10px] text-zinc-400 mt-0.5">{w.model}</div>
                    <div className="text-[10px] text-emerald-400 font-semibold mt-1">{w.cost}</div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Token Distribution Split Bar */}
          <div>
            <div className="flex items-center justify-between text-xs font-mono mb-2">
              <span className="text-zinc-400">Token Workload Distribution</span>
              <span className="text-emerald-400 font-bold">92% Free Local • 8% Frontier</span>
            </div>
            <div className="h-3 w-full rounded-full bg-zinc-800 overflow-hidden flex">
              <div
                className="h-full bg-gradient-to-r from-emerald-500 to-cyan-400 transition-all duration-300 relative group"
                style={{ width: "92%" }}
                title="Tier 3 Local Workers (92% free execution)"
              />
              <div
                className="h-full bg-gradient-to-r from-purple-500 to-rose-500 transition-all duration-300"
                style={{ width: "8%" }}
                title="Tier 1 Frontier Senior Boss (8% high-cognition guidance)"
              />
            </div>
            <div className="flex items-center justify-between text-[11px] font-mono text-zinc-500 mt-1.5">
              <span className="flex items-center gap-1 text-emerald-400">
                <span className="w-2 h-2 rounded-full bg-emerald-400" /> Tier 3 Local Boilerplate
              </span>
              <span className="flex items-center gap-1 text-purple-400">
                <span className="w-2 h-2 rounded-full bg-purple-400" /> Tier 1 Architectural Brain
              </span>
            </div>
          </div>
        </div>

        {/* Right Metric Summary Card (5 cols) */}
        <div className="lg:col-span-5 glass-panel-glow p-6 sm:p-8 rounded-2xl border border-emerald-500/30 space-y-6 shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 w-36 h-36 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />

          {/* Big Green Glowing Counter */}
          <div className="space-y-1">
            <span className="font-mono text-xs text-emerald-400 uppercase tracking-widest font-semibold flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5" />
              MONTHLY NET SAVINGS
            </span>
            <div className="text-5xl sm:text-6xl font-extrabold font-mono text-emerald-400 text-glow-emerald tracking-tight">
              ${monthlySavings.toLocaleString()}
              <span className="text-xl font-normal text-zinc-400"> /mo</span>
            </div>
            <p className="text-xs font-mono text-zinc-400">
              Equivalent to <span className="text-emerald-400 font-bold">${annualSavings.toLocaleString()} / year</span> saved across developer seats.
            </p>
          </div>

          {/* Direct Spend Comparison Box */}
          <div className="p-4 rounded-xl bg-black/60 border border-white/5 space-y-3 font-mono text-xs">
            <div className="flex items-center justify-between">
              <span className="text-zinc-400">Direct Frontier Spend:</span>
              <span className="text-rose-400 line-through font-semibold">
                ${frontierMonthly.toLocaleString()} /mo
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-zinc-400">Aegis 3-Tier Arbitrage:</span>
              <span className="text-cyan-400 font-bold">
                ${aegisMonthly.toLocaleString()} /mo
              </span>
            </div>
            <div className="pt-2 border-t border-white/10 flex items-center justify-between text-emerald-400 font-bold">
              <span>Cost Reduction:</span>
              <span>{reductionPercentage}% Less Spend</span>
            </div>
          </div>

          {/* 3-Tier Explanation Pills */}
          <div className="space-y-2 pt-2 border-t border-white/10">
            <div className="text-[11px] font-mono uppercase tracking-wider text-zinc-400 font-semibold mb-2">
              Autonomous Division of Labor:
            </div>

            <div className="flex items-start gap-2.5 p-2 rounded-lg bg-white/5 border border-white/5 text-xs">
              <span className="px-1.5 py-0.5 rounded bg-purple-500/20 text-purple-300 font-mono text-[10px] font-bold mt-0.5">
                T1
              </span>
              <div className="text-zinc-300 text-[11px]">
                <strong className="text-white">Senior Boss:</strong> High cognition, system invariants, coaching loop, final verification.
              </div>
            </div>

            <div className="flex items-start gap-2.5 p-2 rounded-lg bg-white/5 border border-white/5 text-xs">
              <span className="px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-300 font-mono text-[10px] font-bold mt-0.5">
                T2
              </span>
              <div className="text-zinc-300 text-[11px]">
                <strong className="text-white">Junior Bosses:</strong> Subagent domain gatekeepers enforcing the 4-Decision Quality Gates.
              </div>
            </div>

            <div className="flex items-start gap-2.5 p-2 rounded-lg bg-white/5 border border-white/5 text-xs">
              <span className="px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-[10px] font-bold mt-0.5">
                T3
              </span>
              <div className="text-zinc-300 text-[11px]">
                <strong className="text-white">Local Workers:</strong> Free boilerplate generation via Hermes CLI, Ollama & OpenCode.
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default ArbitrageCalculator;
