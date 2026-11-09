"use client";

import React from "react";
import { Zap, ShieldCheck, Activity, Terminal, Lock } from "lucide-react";

export interface Feature06StatsBadgeProps {
  className?: string;
}

const STATS = [
  {
    label: "SYNTHESIS SPEED",
    value: "1.8s",
    sub: "DETERMINISTIC DAG",
    icon: Zap,
    accent: false,
  },
  {
    label: "COMPUTE SAVED",
    value: "95.8%",
    sub: "ZERO-REDUNDANCY",
    icon: ShieldCheck,
    accent: true,
  },
  {
    label: "NEURAL LATENCY",
    value: "24ms",
    sub: "SUB-TICK DISPATCH",
    icon: Activity,
    accent: false,
  },
  {
    label: "VERIFIED SUITE",
    value: "286/286",
    sub: "100% INVARIANT PASS",
    icon: Terminal,
    accent: false,
  },
] as const;

const INVARIANTS = [
  {
    id: "INV-01",
    formula: "∀ G ∈ Blueprint : Acyclic(G) ∧ Deterministic(G)",
    desc: "Strict topological execution order without cyclic state mutation.",
  },
  {
    id: "INV-02",
    formula: "ΔCost(Aegis) ≤ 0.042 · Cost(Baseline)",
    desc: "Guaranteed 95.8% reduction in token and graph traversal overhead.",
  },
  {
    id: "INV-03",
    formula: "T_dispatch(n) < 25ms ∀ n ∈ ActiveNodes",
    desc: "Hard real-time neural routing latency bound across all blueprint layers.",
  },
  {
    id: "INV-04",
    formula: "∑ Pass(Test_i) / 286 = 1.000",
    desc: "Zero-tolerance formal verification gate prior to blueprint lock.",
  },
] as const;

export function Feature06StatsBadge({ className = "" }: Feature06StatsBadgeProps) {
  return (
    <section
      className={`bg-[#070709] text-zinc-100 p-6 md:p-8 border-2 border-zinc-800 rounded-none font-sans selection:bg-[#B91C1C] selection:text-white ${className}`}
    >
      <div className="max-w-5xl mx-auto space-y-6">
        {/* Top Editorial Plate Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b-2 border-zinc-800 pb-5">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 bg-[#B91C1C] text-white px-2.5 py-1 border-2 border-black shadow-[3px_3px_0px_#000000]">
              <Lock className="w-3.5 h-3.5 stroke-[2.5]" />
              <span className="font-mono text-xs uppercase tracking-widest font-bold">
                FEATURE 06 // AEGISBRAIN CORE
              </span>
            </div>
            <h2 className="text-2xl md:text-4xl font-black tracking-tight uppercase text-[#FAF8F5]">
              Master Architectural Blueprints
            </h2>
          </div>

          <div className="bg-[#101116] border-2 border-zinc-800 px-3.5 py-2 self-start md:self-end">
            <div className="font-mono text-xs uppercase tracking-widest text-zinc-400">
              STATUS: <span className="text-[#DC2626] font-bold">LOCKED & VERIFIED</span>
            </div>
            <div className="font-mono text-[11px] text-zinc-500 uppercase tracking-widest">
              REV 06.4 // PLATE #A86
            </div>
          </div>
        </div>

        {/* 4 Key Metrics Grid (Paper-Plate Contrast) */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {STATS.map((stat) => {
            const Icon = stat.icon;
            return (
              <div
                key={stat.label}
                className={`bg-[#FAF8F5] text-[#0D0D11] border-2 border-black p-4 rounded-none transition-transform duration-150 hover:-translate-y-0.5 ${
                  stat.accent
                    ? "shadow-[4px_4px_0px_#B91C1C]"
                    : "shadow-[4px_4px_0px_#000000]"
                }`}
              >
                <div className="flex items-center justify-between border-b-2 border-black pb-2 mb-3">
                  <span className="font-mono text-xs uppercase tracking-widest font-bold text-[#0D0D11]">
                    {stat.label}
                  </span>
                  <div
                    className={`p-1 border border-black ${
                      stat.accent ? "bg-[#B91C1C] text-white" : "bg-black text-[#FAF8F5]"
                    }`}
                  >
                    <Icon className="w-3.5 h-3.5 stroke-[2.5]" />
                  </div>
                </div>

                <div className="flex items-baseline justify-between">
                  <span
                    className={`text-3xl md:text-4xl font-black tracking-tighter font-mono ${
                      stat.accent ? "text-[#B91C1C]" : "text-black"
                    }`}
                  >
                    {stat.value}
                  </span>
                </div>

                <div className="mt-3 pt-2 border-t border-zinc-300 flex items-center justify-between">
                  <span className="font-mono text-[11px] uppercase tracking-widest text-zinc-700 font-semibold">
                    {stat.sub}
                  </span>
                  <span className="w-2 h-2 bg-[#B91C1C] border border-black" />
                </div>
              </div>
            );
          })}
        </div>

        {/* 4 Core Mathematical Invariants Ledger */}
        <div className="bg-[#FAF8F5] text-[#0D0D11] border-2 border-black shadow-[4px_4px_0px_#B91C1C] rounded-none">
          <div className="bg-black text-[#FAF8F5] px-4 py-2.5 border-b-2 border-black flex flex-wrap items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 bg-[#DC2626] inline-block" />
              <span className="font-mono text-xs uppercase tracking-widest font-bold">
                CORE MATHEMATICAL INVARIANTS // FORMAL PROOF LEDGER
              </span>
            </div>
            <span className="font-mono text-xs uppercase tracking-widest text-zinc-400">
              Q.E.D. ENFORCED
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 divide-y-2 md:divide-y-0 md:divide-x-2 divide-black">
            {INVARIANTS.map((inv, idx) => (
              <div
                key={inv.id}
                className={`p-4 flex flex-col justify-between gap-2 ${
                  idx >= 2 ? "md:border-t-2 md:border-black" : ""
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <span className="font-mono text-xs uppercase tracking-widest font-bold px-2 py-0.5 bg-black text-[#FAF8F5] border border-black shrink-0">
                    {inv.id}
                  </span>
                  <code className="font-mono text-xs md:text-sm font-bold text-[#B91C1C] bg-zinc-200/80 px-2 py-0.5 border border-black break-all">
                    {inv.formula}
                  </code>
                </div>
                <p className="text-xs md:text-sm font-medium text-zinc-800 leading-snug mt-1">
                  {inv.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

export default Feature06StatsBadge;
