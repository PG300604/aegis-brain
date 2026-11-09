"use client";

import React, { useState } from "react";
import { Zap, DollarSign, Database, ShieldCheck, CheckCircle2, ChevronRight } from "lucide-react";

export interface MetricItem {
  id: string;
  label: string;
  value: string;
  detail: string;
  icon: React.ElementType;
}

export interface InvariantItem {
  id: string;
  tag: string;
  text: string;
}

const DEFAULT_METRICS: MetricItem[] = [
  {
    id: "speed",
    label: "End-to-End Speed",
    value: "1.8s",
    detail: "Full turnaround pipeline",
    icon: Zap,
  },
  {
    id: "cost",
    label: "API Cost Saved",
    value: "95.8%",
    detail: "Free local token arbitrage",
    icon: DollarSign,
  },
  {
    id: "latency",
    label: "Neural Latency",
    value: "24ms",
    detail: "SQLite FTS5 bus retrieval",
    icon: Database,
  },
  {
    id: "tests",
    label: "Test Reliability",
    value: "286/286",
    detail: "Autonomous verification passes",
    icon: ShieldCheck,
  },
];

const DEFAULT_INVARIANTS: InvariantItem[] = [
  {
    id: "inv-1",
    tag: "INV-01",
    text: "Zero Token Waste: Frontier models never write repetitive boilerplate.",
  },
  {
    id: "inv-2",
    tag: "INV-02",
    text: "Zero Amnesia: Decisions and patterns persist across sessions in brain.db.",
  },
  {
    id: "inv-3",
    tag: "INV-03",
    text: "Zero Blind Commits: Sandboxed tests pass before code touches git.",
  },
  {
    id: "inv-4",
    tag: "INV-04",
    text: "Immortal Daemon: 24/7 background scheduler self-heals across reboots.",
  },
];

interface Feature06StatsBadgeProps {
  metrics?: MetricItem[];
  invariants?: InvariantItem[];
  className?: string;
}

export function Feature06StatsBadge({
  metrics = DEFAULT_METRICS,
  invariants = DEFAULT_INVARIANTS,
  className = "",
}: Feature06StatsBadgeProps) {
  const [activeTab, setActiveTab] = useState<"metrics" | "invariants">("metrics");

  return (
    <div
      className={`relative w-full border-2 border-black bg-[#FAF8F5] p-5 sm:p-7 shadow-[6px_6px_0px_#000000] text-[#0D0D11] ${className}`}
    >
      {/* Top Graphic Novel Header Strip */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b-2 border-black pb-4 mb-6">
        <div className="flex items-center gap-2.5">
          <div className="bg-black text-[#FAF8F5] px-2.5 py-1 text-xs font-mono uppercase tracking-widest font-bold shadow-[2px_2px_0px_#B91C1C]">
            SYSTEM SPECS
          </div>
          <span className="text-xs font-mono uppercase tracking-wider text-black/70 font-bold">
            FEATURE 06 • TOPOLOGY METRICS
          </span>
        </div>

        {/* Tab Selector */}
        <div className="flex items-center gap-1.5 border border-black p-0.5 bg-black/5">
          <button
            type="button"
            onClick={() => setActiveTab("metrics")}
            className={`px-3 py-1 text-xs font-mono font-bold uppercase transition-transform ${
              activeTab === "metrics"
                ? "bg-black text-[#FAF8F5] shadow-[2px_2px_0px_#B91C1C]"
                : "text-black/75 hover:bg-black/10"
            }`}
          >
            Metrics
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("invariants")}
            className={`px-3 py-1 text-xs font-mono font-bold uppercase transition-transform ${
              activeTab === "invariants"
                ? "bg-black text-[#FAF8F5] shadow-[2px_2px_0px_#B91C1C]"
                : "text-black/75 hover:bg-black/10"
            }`}
          >
            Invariants
          </button>
        </div>
      </div>

      {/* Content View: Metrics Grid */}
      {activeTab === "metrics" ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {metrics.map((item) => {
            const Icon = item.icon;
            return (
              <div
                key={item.id}
                className="group relative border-2 border-black bg-white p-4 shadow-[4px_4px_0px_#000000] hover:-translate-y-0.5 hover:shadow-[5px_5px_0px_#B91C1C] transition-all"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-mono text-[11px] font-bold uppercase tracking-wider text-black/60">
                    {item.label}
                  </span>
                  <div className="p-1 border border-black bg-[#FAF8F5]">
                    <Icon className="w-3.5 h-3.5 text-[#B91C1C]" />
                  </div>
                </div>
                <div className="font-mono text-3xl font-black text-black tracking-tight mb-1">
                  {item.value}
                </div>
                <div className="text-xs font-mono text-black/75 leading-tight">
                  {item.detail}
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        /* Content View: Invariants List */
        <div className="space-y-3">
          {invariants.map((inv) => (
            <div
              key={inv.id}
              className="flex items-start gap-3 border-2 border-black bg-white p-3.5 shadow-[3px_3px_0px_#000000] hover:-translate-y-0.5 hover:shadow-[4px_4px_0px_#B91C1C] transition-all"
            >
              <div className="shrink-0 bg-black text-[#FAF8F5] font-mono text-[10px] font-bold px-2 py-0.5 tracking-wider shadow-[1px_1px_0px_#B91C1C]">
                {inv.tag}
              </div>
              <p className="text-xs font-mono text-black font-medium leading-relaxed">
                {inv.text}
              </p>
            </div>
          ))}
        </div>
      )}

      {/* Bottom Footer Callout */}
      <div className="mt-6 flex flex-wrap items-center justify-between gap-2 border-t-2 border-black pt-3.5 text-xs font-mono">
        <div className="flex items-center gap-1.5 text-black/70">
          <CheckCircle2 className="w-4 h-4 text-[#B91C1C]" />
          <span>Andrej Karpathy Simplicity Doctrine Enforced</span>
        </div>
        <div className="text-black/50 uppercase tracking-widest text-[10px]">
          AegisBrain • Dual-Engine Architecture
        </div>
      </div>
    </div>
  );
}
