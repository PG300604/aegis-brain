"use client";

import React, { useState } from "react";
import { motion } from "motion/react";
import { Crown, Network, Cpu, ArrowDown, CheckCircle2 } from "lucide-react";
import { triggerSoundEffect } from "@/components/audio/SoundtrackController";

interface TierNode {
  tier: string;
  name: string;
  role: string;
  models: string;
  tokenCost: string;
  color: string;
  borderColor: string;
  badge: string;
  responsibilities: string[];
}

const TIERS: TierNode[] = [
  {
    tier: "TIER 1",
    name: "Senior Boss (Strategic Brain)",
    role: "System Architecture & High Cognition Review",
    models: "Gemini 4 / Claude Opus / Fable",
    tokenCost: "Premium Frontier Tokens (Minimal Calls)",
    color: "#B91C1C",
    borderColor: "border-[#B91C1C]",
    badge: "BRAIN ONLY",
    responsibilities: [
      "Zero direct boilerplate / implementation writing",
      "Defines mathematical invariants & test criteria",
      "Performs AST diff audit and final sign-off",
    ],
  },
  {
    tier: "TIER 2",
    name: "Junior Bosses (Domain Subagents)",
    role: "QA, Backend, Security & Frontend Leads",
    models: "Gemini Flash / Claude Sonnet / Subagents",
    tokenCost: "Balanced Tokens (Task Orchestration)",
    color: "#D4AF37",
    borderColor: "border-[#D4AF37]",
    badge: "ORCHESTRATOR",
    responsibilities: [
      "Formats strict prompt contracts for Tier 3 workers",
      "Executes 4-Stage Quality Gate on raw worker output",
      "Coaches workers in continuous error-reduction loops",
    ],
  },
  {
    tier: "TIER 3",
    name: "Execution Workers (Local Muscle)",
    role: "Fast Implementation & Boilerplate Generation",
    models: "Hermes CLI / Ollama Qwen2.5-Coder / OpenCode",
    tokenCost: "$0.00 (100% Free Local Hardware Tokens)",
    color: "#10B981",
    borderColor: "border-emerald-500",
    badge: "100% FREE",
    responsibilities: [
      "Writes 100% of candidate code drafts & test suites",
      "Runs locally on host hardware with 0 API tokens",
      "Iterates until all AST and pytest gates pass 100%",
    ],
  },
];

export function InteractiveTierDiagram() {
  const [activeTier, setActiveTier] = useState<number>(0);

  return (
    <div className="relative w-full p-5 sm:p-7 bg-[#0E0F15] rounded-none border-2 border-black text-[#FBF9F5] shadow-[6px_6px_0px_#000000] overflow-hidden">
      {/* Background Graphic Grid */}
      <div
        className="absolute inset-0 pointer-events-none opacity-10"
        style={{
          backgroundImage: `radial-gradient(circle, #D4AF37 1px, transparent 1px)`,
          backgroundSize: "24px 24px",
        }}
      />

      {/* Header */}
      <div className="relative z-10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pb-5 border-b border-white/10">
        <div>
          <div className="font-nikkei text-xs uppercase tracking-[0.2em] text-[#B91C1C] font-extrabold flex items-center gap-2">
            <span className="w-2.5 h-2.5 bg-[#B91C1C] border border-black inline-block" />
            TRI-TIER ARCHITECTURE SPECIFICATION
          </div>
          <h3 className="font-charles-rosie text-xl sm:text-2xl text-white uppercase tracking-tight mt-1.5">
            Tri-Tier Token Arbitrage Flow
          </h3>
          <p className="text-xs text-zinc-300 font-gt-era">
            Hover over any tier layer to inspect the division of labor and real-time laser signal paths.
          </p>
        </div>

        <div className="px-3 py-1.5 bg-black border border-white/20 rounded-none font-mono text-xs text-emerald-400 flex items-center gap-2 shadow-[2px_2px_0px_#10B981]">
          <span className="w-2.5 h-2.5 bg-emerald-400 border border-black inline-block" />
          <span>92.4% Token Cost Reduction</span>
        </div>
      </div>

      {/* 3D Tier Stack Diagram with Laser Signal Flows */}
      <div className="relative z-10 py-6 grid grid-cols-1 lg:grid-cols-3 gap-4 items-stretch">
        {TIERS.map((tier, idx) => {
          const isSelected = activeTier === idx;
          return (
            <motion.div
              key={tier.tier}
              onMouseEnter={() => {
                setActiveTier(idx);
                triggerSoundEffect("click");
              }}
              whileHover={{ y: -6, scale: 1.02 }}
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
              className={`relative flex flex-col justify-between p-5 rounded-none border-2 transition-all cursor-pointer select-none ${
                isSelected
                  ? `bg-[#181922] ${tier.borderColor} shadow-[6px_6px_0px_#000000]`
                  : "bg-black/70 border-white/15 opacity-80 hover:opacity-100 shadow-[3px_3px_0px_#000000]"
              }`}
            >
              {/* Top Accent Tag */}
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span
                    className="font-nikkei text-[11px] uppercase tracking-wider px-2 py-0.5 rounded-none font-extrabold border border-black"
                    style={{ backgroundColor: tier.color, color: "#FFFFFF" }}
                  >
                    {tier.tier}
                  </span>
                  <span className="text-[10px] font-mono uppercase text-zinc-400 bg-white/5 px-2 py-0.5 rounded-none border border-white/10">
                    {tier.badge}
                  </span>
                </div>

                <h4 className="font-charles-rosie text-lg text-white uppercase tracking-tight">
                  {tier.name}
                </h4>
                <div className="text-xs text-zinc-300 font-gt-era font-medium mt-1">
                  {tier.role}
                </div>

                <div className="mt-3 p-2 bg-black/80 rounded-none border border-white/10 font-mono text-[11px]">
                  <div className="text-zinc-400 text-[10px] uppercase">Engine Models:</div>
                  <div className="text-white font-semibold">{tier.models}</div>
                  <div className="text-[10px] text-emerald-400 mt-1 font-bold">
                    {tier.tokenCost}
                  </div>
                </div>

                <div className="mt-3 space-y-1.5">
                  <div className="text-[10px] font-nikkei uppercase text-[#D4AF37] font-bold">
                    Invariants:
                  </div>
                  {tier.responsibilities.map((resp, rIdx) => (
                    <div key={rIdx} className="flex items-start gap-1.5 text-[11px] text-zinc-300 font-gt-era">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                      <span>{resp}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Pulsing Signal Packet Rail */}
              <div className="mt-4 pt-3 border-t border-white/10 flex items-center justify-between text-[10px] font-mono text-zinc-400">
                <span className="flex items-center gap-1.5">
                  <span
                    className="w-2.5 h-2.5 border border-black inline-block"
                    style={{ backgroundColor: tier.color }}
                  />
                  <span>Active Channel</span>
                </span>
                <span className="text-white/60">Sub-25ms Latency</span>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Laser Schematic Pulse Footer */}
      <div className="relative z-10 pt-4 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs font-mono text-zinc-400">
        <div className="flex items-center gap-2">
          <span className="text-[#D4AF37] font-bold">&gt;&gt;</span>
          <span>DETERMINISTIC INVARIANT: Tier 1 &amp; Tier 2 NEVER burn frontier tokens on implementation boilerplate.</span>
        </div>
        <div className="text-[10px] text-emerald-400 font-bold bg-emerald-950/60 px-2.5 py-1 rounded border border-emerald-500/30">
          ZERO FRONTIER TOKEN WASTE
        </div>
      </div>
    </div>
  );
}
