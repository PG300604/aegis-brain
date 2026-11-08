"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import {
  ChevronDown,
  ChevronUp,
  Clock,
  CheckCircle2,
  Terminal,
  Cpu,
  Database,
  Layers,
  Activity,
} from "lucide-react";
import "./ThoughtLine.css";

interface TraceStep {
  id: string;
  title: string;
  detail: string;
  latency: string;
  icon?: React.ElementType;
}

interface ThoughtLineProps {
  summary?: string;
  totalTime?: string;
  steps?: TraceStep[];
  defaultExpanded?: boolean;
  className?: string;
}

const DEFAULT_STEPS: TraceStep[] = [
  {
    id: "1",
    title: "Cognitive Invariant Triage",
    detail: "Tier 1 Senior Boss evaluates task severity. Detects macro feature (>15 lines). Spawns Tier 2 Junior Boss.",
    latency: "3 ms",
    icon: Cpu,
  },
  {
    id: "2",
    title: "Neural Memory Indexed Recall",
    detail: "Executed FTS5 BM25 search over brain.db WAL. 2 memories retrieved, compacted to 310 tokens.",
    latency: "21 ms",
    icon: Database,
  },
  {
    id: "3",
    title: "Tier 3 Local Worker Dispatch",
    detail: "Hermes 3 worker invoked via local CLI. Candidate code draft generated at $0.00 marginal cost.",
    latency: "420 ms",
    icon: Terminal,
  },
  {
    id: "4",
    title: "4-Decision Quality Gate Execution",
    detail: "Karpathy simplicity check passed (0 orphan abstractions). Red-team AST audit clear (0 injection vectors).",
    latency: "14 ms",
    icon: CheckCircle2,
  },
];

export function ThoughtLine({
  summary = "Thinking: Decomposed query into 4-stage pipeline, retrieved indexed memory, verified 0 token leak...",
  totalTime = "24 ms total",
  steps = DEFAULT_STEPS,
  defaultExpanded = false,
  className = "",
}: ThoughtLineProps) {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);

  return (
    <div className={`thought-line-container relative ${className}`}>
      {/* Background Subtle Shimmer Sweep */}
      <div className="thought-shimmer-sweep" />

      {/* Header Bar */}
      <button
        type="button"
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full p-3 sm:p-3.5 flex items-center justify-between gap-3 text-left transition-colors hover:bg-black/5 cursor-pointer bg-[#FAF8F5]"
      >
        <div className="flex items-center gap-2.5 min-w-0">
          <div className="flex items-center justify-center w-6 h-6 rounded bg-black text-[#D4AF37] shrink-0 border border-black shadow-[1px_1px_0px_#000000]">
            <Activity className="w-3.5 h-3.5 text-[#D4AF37]" />
          </div>
          <span className="text-xs sm:text-sm font-gt-era text-black font-semibold truncate">
            {summary}
          </span>
        </div>

        <div className="flex items-center gap-2.5 shrink-0 font-mono text-xs text-black">
          <div className="flex items-center gap-1 text-[11px] px-2 py-0.5 rounded bg-white border border-black text-black font-bold shadow-[1px_1px_0px_#000000]">
            <Clock className="w-3 h-3 text-[#B91C1C]" />
            <span>{totalTime}</span>
          </div>
          {isExpanded ? (
            <ChevronUp className="w-4 h-4 text-black" />
          ) : (
            <ChevronDown className="w-4 h-4 text-black" />
          )}
        </div>
      </button>

      {/* Expanded Step Trace */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
            className="border-t-2 border-black bg-white p-3 sm:p-4 space-y-3"
          >
            <div className="text-[10px] font-nikkei uppercase text-black/60 font-bold tracking-wider">
              Autonomous Step Execution Trace Ticks
            </div>

            <div className="space-y-2.5">
              {steps.map((step, idx) => {
                const Icon = step.icon || CheckCircle2;
                return (
                  <div
                    key={step.id || idx}
                    className="flex items-start justify-between gap-3 p-2.5 rounded bg-[#FAF8F5] border border-black shadow-[2px_2px_0px_#000000] text-xs font-mono"
                  >
                    <div className="flex items-start gap-2.5 min-w-0">
                      <div className="p-1 rounded bg-black text-[#D4AF37] shrink-0 mt-0.5">
                        <Icon className="w-3.5 h-3.5" />
                      </div>
                      <div>
                        <div className="font-nikkei font-bold uppercase text-black tracking-wide">{step.title}</div>
                        <div className="text-[11px] text-black/70 font-gt-era mt-0.5 leading-relaxed">
                          {step.detail}
                        </div>
                      </div>
                    </div>
                    <span className="text-[11px] font-mono font-bold text-[#B91C1C] shrink-0 px-1.5 py-0.5 rounded bg-white border border-black shadow-[1px_1px_0px_#000000]">
                      +{step.latency}
                    </span>
                  </div>
                );
              })}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
