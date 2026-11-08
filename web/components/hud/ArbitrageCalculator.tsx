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
          <p className="text-xs sm:text-sm text-zinc-400 font-gt-era max-w-xl mt-1">
            Offload 92% of verbose boilerplate to free local workers. Reserve precious frontier cognition exclusively for architecture.
          </p>
        </div>

        <div className="px-4 py-2 bg-emerald-950/80 border-2 border-emerald-500 rounded text-center shadow-[3px_3px_0px_#000000]">
          <div className="font-nikkei text-xl sm:text-2xl font-extrabold text-emerald-400">
            {reductionPercentage}%
          </div>
          <div className="text-[10px] font-mono uppercase text-emerald-300">Frontier Cost Reduction</div>
        </div>
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
              onChange={(e) => setTurns(Number(e.target.value))}
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
                    onClick={() => setSelectedWorker(w.id)}
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

        {/* Right Financial Ledger Readout (5 cols) */}
        <div className="lg:col-span-5 p-6 sm:p-8 rounded-lg bg-[#FAF8F5] text-black border-2 border-black shadow-[6px_6px_0px_#000000] space-y-6">
          <div className="flex items-center justify-between border-b-2 border-black pb-3">
            <span className="font-nikkei text-xs uppercase tracking-wider text-black font-extrabold">
              Audited Savings Ledger
            </span>
            <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 text-[10px] font-mono font-bold">
              ESTIMATED ROI
            </span>
          </div>

          <div className="space-y-4 font-mono">
            <div>
              <div className="text-[11px] text-black/60 uppercase">Traditional Frontier API Spend</div>
              <div className="text-2xl font-bold text-[#B91C1C] line-through mt-0.5">
                ${frontierMonthly.toLocaleString()} / month
              </div>
            </div>

            <div>
              <div className="text-[11px] text-black/60 uppercase">Aegis 3-Tier Arbitrage Spend</div>
              <div className="text-xl font-bold text-black mt-0.5">
                ${aegisMonthly.toLocaleString()} / month
              </div>
            </div>

            <div className="p-4 bg-white border-2 border-black rounded shadow-[3px_3px_0px_#10B981]">
              <div className="text-[11px] text-emerald-800 font-nikkei uppercase font-extrabold">Net Monthly Savings</div>
              <div className="text-3xl font-extrabold text-emerald-700 mt-1">
                +${monthlySavings.toLocaleString()}
                <span className="text-xs text-black/60 font-normal"> / mo</span>
              </div>
              <div className="text-[11px] text-black/70 mt-1">
                Annual runway dividend: <strong>+${annualSavings.toLocaleString()} / yr</strong>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
