"use client";

import React, { useState, useEffect, useId } from "react";
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
  Repeat,
} from "lucide-react";

export function ArbitrageCalculator() {
  const [turns, setTurns] = useState<number>(250);
  const [selectedWorker, setSelectedWorker] = useState<string>("hermes");
  const [isAutoPlaying, setIsAutoPlaying] = useState<boolean>(true);
  const sliderId = useId();

  const turnsCycle = [100, 250, 500, 750, 1000];
  const workers = [
    { id: "hermes", name: "Hermes Agent CLI", model: "Hermes-3 Llama-3.1 8B", cost: "$0.00 / token" },
    { id: "ollama", name: "Ollama Local MoE", model: "Qwen2.5-Coder 7B", cost: "$0.00 / token" },
    { id: "opencode", name: "OpenCode Engine", model: "DeepSeek-Coder V2", cost: "$0.00 / token" },
  ];

  // Autoplay simulation loop: cycle through workloads every 4s
  useEffect(() => {
    if (!isAutoPlaying) return;

    const interval = setInterval(() => {
      setTurns((current) => {
        const idx = turnsCycle.indexOf(current);
        const nextIdx = (idx + 1) % turnsCycle.length;
        return turnsCycle[nextIdx];
      });
      setSelectedWorker((current) => {
        const workerIds = workers.map((w) => w.id);
        const idx = workerIds.indexOf(current);
        return workerIds[(idx + 1) % workerIds.length];
      });
    }, 4000);

    return () => clearInterval(interval);
  }, [isAutoPlaying]);

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

  return (
    <div className="relative p-6 sm:p-8 bg-[#101116] text-[#FBF9F5] border-2 border-black rounded-lg">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-black/40">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#B91C1C] text-white font-nikkei text-xs uppercase tracking-widest shadow-[2px_2px_0px_#000000]">
            <Calculator className="w-3.5 h-3.5" />
            <span>TOKEN ARBITRAGE SIMULATOR</span>
          </div>
          <h3 className="text-2xl sm:text-3xl font-charles-rosie text-white uppercase tracking-tight mt-2">
            Dynamic Token Arbitrage Calculator
          </h3>
          <p className="text-xs sm:text-sm text-zinc-200 font-sans font-medium max-w-xl mt-1 leading-relaxed">
            Offload 92% of verbose boilerplate to free local workers. Reserve precious frontier cognition exclusively for architecture.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="px-4 py-2 bg-emerald-950/80 border-2 border-emerald-500 rounded text-center shadow-[3px_3px_0px_#000000]">
            <div className="font-nikkei text-xl sm:text-2xl font-extrabold text-emerald-400">
              {reductionPercentage}%
            </div>
            <div className="text-[10px] font-mono uppercase text-emerald-300">Frontier Cost Reduction</div>
          </div>
        </div>
      </div>

      {/* Graphic Novel Narration Box matching Santioni style */}
      <div className="narration-box my-4">
        <p className="narration-text">
          THE SENIOR REASONING BRAIN DIRECTS ARCHITECTURE ALONE. VERBOSE BOILERPLATE AND BRUTE IMPLEMENTATION DRAFTS ARE DISPATCHED TO FREE LOCAL WORKERS.
        </p>
      </div>

      {/* Main Calculator Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center mt-6">
        {/* Left Controller Panel (7 cols) */}
        <div className="lg:col-span-7 p-6 rounded-lg bg-[#181822] border-2 border-black shadow-[4px_4px_0px_#000000] space-y-6">
          {/* Turns Slider */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <label htmlFor={sliderId} className="font-nikkei text-xs uppercase tracking-wider text-white">
                Daily Developer Interaction Turns
              </label>
              <div className="font-mono text-sm font-bold text-[#D4AF37] px-3 py-1 rounded bg-black border border-black shadow-[2px_2px_0px_#000000]">
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
              onChange={(e) => {
                setTurns(Number(e.target.value));
                setIsAutoPlaying(false);
              }}
              className="w-full h-2.5 bg-black rounded appearance-none cursor-pointer accent-[#B91C1C]"
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
            <span className="block font-nikkei text-xs uppercase tracking-wider text-white mb-3">
              Active Tier 3 Execution Worker
            </span>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
              {workers.map((w) => {
                const active = selectedWorker === w.id;
                return (
                  <button
                    key={w.id}
                    type="button"
                    onClick={() => {
                      setSelectedWorker(w.id);
                      setIsAutoPlaying(false);
                    }}
                    className={`p-3 rounded-lg border-2 border-black font-mono text-left transition-all cursor-pointer ${
                      active
                        ? "bg-[#B91C1C]/20 border-[#B91C1C] shadow-[3px_3px_0px_#B91C1C]"
                        : "bg-black/60 hover:bg-black/80 shadow-[2px_2px_0px_#000000]"
                    }`}
                  >
                    <div className="text-xs font-bold text-white flex items-center justify-between font-nikkei uppercase">
                      <span className={active ? "text-[#D4AF37]" : ""}>{w.name}</span>
                      {active && <span className="h-2 w-2 rounded-full bg-[#B91C1C] animate-ping" />}
                    </div>
                    <div className="text-[10px] text-zinc-400 mt-0.5">{w.model}</div>
                    <div className="text-[10px] text-emerald-400 font-bold mt-1">{w.cost}</div>
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
            <div className="h-3 w-full rounded bg-black border border-black overflow-hidden flex">
              <div
                className="h-full bg-emerald-500 transition-all duration-300"
                style={{ width: "92%" }}
                title="Tier 3 Local Workers (92% free execution)"
              />
              <div
                className="h-full bg-[#B91C1C] transition-all duration-300"
                style={{ width: "8%" }}
                title="Tier 1 Frontier Senior Boss (8% high-cognition guidance)"
              />
            </div>
            <div className="flex items-center justify-between text-[11px] font-mono text-zinc-400 mt-2">
              <span className="flex items-center gap-1.5 text-emerald-400">
                <span className="w-2 h-2 rounded-full bg-emerald-400" /> Tier 3 Free Local Workers
              </span>
              <span className="flex items-center gap-1.5 text-red-400">
                <span className="w-2 h-2 rounded-full bg-[#B91C1C]" /> Tier 1 Frontier Cognition
              </span>
            </div>
          </div>
        </div>

        {/* Right Output Dashboard (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          <div className="comic-plate p-6 rounded-lg text-black space-y-4">
            <div className="flex items-center justify-between border-b-2 border-black pb-3">
              <span className="font-nikkei text-xs uppercase tracking-wider text-black font-extrabold">
                Monthly Spend Comparison
              </span>
              <span className="text-[10px] font-mono text-zinc-500">30-Day Billing Cycle</span>
            </div>

            {/* Traditional Direct Cost */}
            <div className="p-3 bg-red-50 border-2 border-black rounded shadow-[2px_2px_0px_#B91C1C]">
              <div className="flex justify-between items-center text-xs font-mono text-red-900">
                <span>Traditional (100% Frontier API)</span>
                <span className="font-bold text-base text-[#B91C1C]">
                  ${frontierMonthly.toLocaleString()} / mo
                </span>
              </div>
              <div className="text-[10px] font-mono text-red-700/80 mt-1">
                Burning expensive tokens on repetitive boilerplate &amp; raw JSON logs.
              </div>
            </div>

            {/* Aegis 3-Tier Cost */}
            <div className="p-3 bg-emerald-50 border-2 border-black rounded shadow-[2px_2px_0px_#10B981]">
              <div className="flex justify-between items-center text-xs font-mono text-emerald-900">
                <span>AegisBrain 3-Tier Arbitrage</span>
                <span className="font-bold text-base text-emerald-700">
                  ${aegisMonthly.toLocaleString()} / mo
                </span>
              </div>
              <div className="text-[10px] font-mono text-emerald-700/80 mt-1">
                92% generated by free local workers. Only architecture calls frontier APIs.
              </div>
            </div>

            {/* Realized Savings Highlight */}
            <div className="pt-2 border-t-2 border-black">
              <div className="flex items-baseline justify-between">
                <div>
                  <div className="text-[10px] uppercase font-nikkei text-black font-extrabold tracking-wider">
                    Total Realized Savings
                  </div>
                  <div className="text-3xl font-nikkei font-extrabold text-[#B91C1C]">
                    +${monthlySavings.toLocaleString()} <span className="text-xs text-black font-normal font-mono">/ month</span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-[10px] uppercase font-nikkei text-zinc-500 tracking-wider">
                    Annual Value
                  </div>
                  <div className="text-base font-mono font-bold text-emerald-700">
                    +${annualSavings.toLocaleString()} / yr
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
