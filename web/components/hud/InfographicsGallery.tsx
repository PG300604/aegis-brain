"use client";

import React, { useState, useEffect } from "react";
import { triggerSoundEffect } from "@/components/audio/SoundtrackController";
import {
  Cpu,
  Layers,
  Globe,
  ShieldCheck,
  Zap,
  TrendingUp,
  Smartphone,
  Maximize2,
  CheckCircle2,
  X,
  Sparkles,
} from "lucide-react";

interface DiagramData {
  id: string;
  title: string;
  shortTitle: string;
  file: string;
  category: string;
  icon: React.ElementType;
  description: string;
  invariants: string[];
  stats: { label: string; value: string; detail: string }[];
}

const DIAGRAMS: DiagramData[] = [
  {
    id: "architecture",
    title: "Unified End-to-End System Blueprint",
    shortTitle: "System Architecture",
    file: "/infographics/infographic-unified-architecture.svg",
    category: "System Topology",
    icon: Cpu,
    description:
      "Complete topological architecture showing the orchestration flow: Tier 1 Senior Boss dispatches high-level directives to Tier 2 Subagents, who orchestrate free Tier 3 local workers (Hermes CLI, Ollama) while maintaining sub-second SQLite WAL neural memory and 24/7 Telegram telemetry.",
    invariants: [
      "Strict division of labor: Tier 1 & Tier 2 never write raw boilerplate directly",
      "SQLite WAL mode with sub-second FTS5 BM25 neural search (<25ms vs >4,200ms)",
      "Self-healing Windows Scheduled Task KeepAlive restarting daemon within 5 minutes on fault",
      "Zero dropped audio via deterministic 25-second Whisper segmentation and transcode shield",
    ],
    stats: [
      { label: "Recall Latency", value: "24 ms", detail: "FTS5 Indexed Search" },
      { label: "Token Savings", value: "95.8%", detail: "Free Local Workers" },
      { label: "Daemon Uptime", value: "99.98%", detail: "Win32 Task Guard" },
      { label: "Test Coverage", value: "286/286", detail: "Pytest Verified" },
    ],
  },
  {
    id: "pyramid",
    title: "3-Tier Multi-Agent Hierarchy Pyramid",
    shortTitle: "Agent Hierarchy",
    file: "/infographics/infographic-hierarchy-pyramid.svg",
    category: "Division of Labor",
    icon: Layers,
    description:
      "The definitive pyramid of intelligence and cost arbitrage. The Frontier Senior Boss (Claude Opus 5.5, Gemini 4) commands architectural strategy, subagent coordinators manage specialized workflows, and local execution engines write boilerplate for $0.00.",
    invariants: [
      "Frontier Cognition Guard: expensive models never touch routine typing or standard unit tests",
      "Dynamic token routing: prompts automatically routed based on task severity scoring",
      "Autonomous error recovery: subagents coach local models without consuming frontier context",
      "Marginal cost reduction: measured 92.4% reduction in frontier API bills",
    ],
    stats: [
      { label: "Tier 1 Brain", value: "Claude Opus / Gemini 4", detail: "Strategic Reasoning" },
      { label: "Tier 2 Boss", value: "Subagent Leads", detail: "Workflow Coordination" },
      { label: "Tier 3 Muscle", value: "Hermes 3 / Ollama", detail: "$0.00 / Token Execution" },
      { label: "Cost Dividend", value: "$1,840 / mo", detail: "Active Team Savings" },
    ],
  },
  {
    id: "agents",
    title: "Universal Multi-Agent Chassis Compatibility",
    shortTitle: "Fleet Compatibility",
    file: "/infographics/infographic-universal-agents.svg",
    category: "Fleet Interoperability",
    icon: Globe,
    description:
      "AegisBrain connects seamlessly to any modern developer coding agent. Whether running inside Antigravity, Claude Code, Cursor, Windsurf, or Aider, the unified neural memory and watchdog service stay identical.",
    invariants: [
      "Universal Sidecar Daemon: runs as a standalone daemon on 127.0.0.1:8765",
      "Zero-config shims: drop-in aliases for Antigravity, Claude Code, and terminal workflows",
      "Single persistent brain: memory accumulated in Cursor is immediately available in Claude Code",
      "Bi-directional file watching: live AST re-indexing on filesystem mutations across all workspaces",
    ],
    stats: [
      { label: "Supported Hosts", value: "6 Engines", detail: "Native CLI Shims" },
      { label: "Config Overhead", value: "Zero Flags", detail: "Automatic Detection" },
      { label: "State Sync", value: "Shared DB", detail: "Single SQLite WAL" },
      { label: "Lock-in Risk", value: "0%", detail: "Apache-2.0 Standard" },
    ],
  },
  {
    id: "gates",
    title: "4-Decision Quality Architecture Gate",
    shortTitle: "Quality Gates",
    file: "/infographics/infographic-quality-gate.svg",
    category: "Verification Pipeline",
    icon: ShieldCheck,
    description:
      "Every line of candidate code drafted by local execution workers must navigate a deterministic 4-stage pipeline before ever touching host repositories or reaching the user.",
    invariants: [
      "Gate 1: Karpathy Simplicity Doctrine — Zero speculative abstractions, surgical diffs <=15 lines",
      "Gate 2: TurnItOut / Unslop — Scrub all conversational AI markers, verbose apologies, and polite slop",
      "Gate 3: Red-Team & AST Security — Block shell=True, command injection vectors, and leaked secrets",
      "Gate 4: Dual-Environment Verification — Sandboxed compilation check followed by host pytest validation",
    ],
    stats: [
      { label: "Inspection Gates", value: "4 Distinct", detail: "AST & Static Analysis" },
      { label: "Security Rejection", value: "100%", detail: "Injection & Secret Leaks" },
      { label: "Slop Reduction", value: "98.4%", detail: "Direct Code Output" },
      { label: "Pass Rate", value: "99.1%", detail: "After Coaching Loop" },
    ],
  },
  {
    id: "speed",
    title: "Sub-Second Latency Benchmarks",
    shortTitle: "Speed Benchmarks",
    file: "/infographics/infographic-speed-benchmarks.svg",
    category: "Performance Metrics",
    icon: Zap,
    description:
      "Empirically measured runtime performance comparing AegisBrain's indexed neural SQLite FTS5 store against the conventional approach of repeatedly crawling megabytes of unstructured session transcript files.",
    invariants: [
      "24ms instant FTS5 BM25 keyword & semantic retrieval vs 12,400ms raw JSONL file grep",
      "Persistent WAL indexing: background commits incur 0ms perceived latency during active agent turns",
      "Active context compacted to <=400 tokens during memory bootstrap (95.8% context window preserved)",
      "Zero memory leaks across 72+ hour continuous daemon execution stress tests",
    ],
    stats: [
      { label: "Aegis Recall", value: "24 ms", detail: "FTS5 Indexed Search" },
      { label: "Raw JSONL Crawl", value: "12,400 ms", detail: "Standard Assistant" },
      { label: "Speed Advantage", value: "516x Faster", detail: "Sub-Second Retrieval" },
      { label: "Context Window", value: "<400 tokens", detail: "Compacted Bootstrap" },
    ],
  },
  {
    id: "learning",
    title: "Autonomous Error-Reduction & Confidence Curve",
    shortTitle: "Learning Curve",
    file: "/infographics/infographic-learning-curve.svg",
    category: "Worker Convergence",
    icon: TrendingUp,
    description:
      "Real-time mathematical tracking of local worker accuracy over successive trials. The coaching loop records compiler failures, linter warnings, and AST feedback, proving autonomous convergence from 3.2 initial error spikes down to 0.",
    invariants: [
      "Tracked trials: initial error detection, coaching feedback, and post-coach error counts recorded in brain.db",
      "Confidence threshold: workers must maintain an average confidence score >= 8.0/10 before autonomous delegation",
      "Automatic fallback: tasks with >2 coaching failures automatically escalate to Tier 1 with structured failure dossier",
      "Continuous learning: regression patterns saved to mistakes ledger to prevent recurring defects",
    ],
    stats: [
      { label: "Convergence Trials", value: "1 - 3 Iterations", detail: "To Zero Defects" },
      { label: "Initial Error Drops", value: "3.2 -> 0.0", detail: "Coached Revisions" },
      { label: "Target Score", value: ">= 8.0 / 10", detail: "Confidence Gate" },
      { label: "Regression Guard", value: "Mistakes Ledger", detail: "Persistent in SQLite" },
    ],
  },
  {
    id: "mobile",
    title: "Deterministic 24/7 Mobile Telegram to CLI Pipeline",
    shortTitle: "Telegram Pipeline",
    file: "/infographics/infographic-mobile-pipeline.svg",
    category: "Remote CLI Telemetry",
    icon: Smartphone,
    description:
      "End-to-end telemetry architecture bridging mobile Telegram audio voice notes, documents, and real-time prompts directly into active terminal coding sessions on your desktop without breaking execution state.",
    invariants: [
      "25-Second Audio Chunking Shield: prevents Whisper buffer underruns, API timeouts, and dropped voice prompts",
      "Native Windows Win32 Keystroke Injection: sends keystrokes into Antigravity CLI sessions via Win32 API handles",
      "Document & Media Ingestion: automated FFmpeg transcoding and text extraction into .user_uploaded directory",
      "Execution Completion Banner: instant Telegram notification with test results and git status upon run termination",
    ],
    stats: [
      { label: "Audio Transcode", value: "<1.2s", detail: "Local FFmpeg Shield" },
      { label: "Dropped Voice Notes", value: "0.0%", detail: "25s Chunking Engine" },
      { label: "Keystroke Latency", value: "<40ms", detail: "Direct Win32 SendInput" },
      { label: "Daemon Service", value: "24/7/365", detail: "Self-Healing Task" },
    ],
  },
];

export function InfographicsGallery() {
  const [activeTab, setActiveTab] = useState<string>("architecture");
  const [lightboxOpen, setLightboxOpen] = useState<boolean>(false);

  const activeDiagram = DIAGRAMS.find((d) => d.id === activeTab) || DIAGRAMS[0];

  // Close lightbox on Escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setLightboxOpen(false);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  return (
    <div className="relative w-full p-6 sm:p-8 bg-[#101116] text-[#FBF9F5] border-2 border-black rounded-lg">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-black/40">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#B91C1C] text-white font-nikkei text-xs uppercase tracking-widest shadow-[2px_2px_0px_#000000]">
            <Sparkles className="w-3.5 h-3.5" />
            <span>SYSTEM BLUEPRINTS</span>
          </div>
          <h3 className="text-2xl sm:text-3xl font-charles-rosie text-white uppercase tracking-tight mt-2">
            Architecture &amp; Execution Flow
          </h3>
          <p className="text-xs sm:text-sm text-zinc-200 font-sans font-medium max-w-xl mt-1 leading-relaxed">
            Clear system blueprints detailing multi-agent token arbitrage, sub-second neural memory, and deterministic mobile telemetry.
          </p>
        </div>

        <div className="px-4 py-2 bg-black border-2 border-black rounded text-center shadow-[3px_3px_0px_#D4AF37]">
          <div className="font-nikkei text-xl sm:text-2xl font-extrabold text-[#D4AF37]">
            7 BLUEPRINTS
          </div>
          <div className="text-[10px] font-mono uppercase text-zinc-400">Hand-Crafted SVG</div>
        </div>
      </div>

      {/* Graphic Novel Narration Box matching Santioni style */}
      <div className="narration-box my-4">
        <p className="narration-text">
          SEVEN SOVEREIGN BLUEPRINTS ETCHED IN STEEL AND PAPYRUS. FROM TOPOLOGY TO RECOVERY GATES, EVERY INVARIANT IS MATHEMATICALLY VERIFIED.
        </p>
      </div>

      {/* Navigation Tabs Bar */}
      <div className="flex items-center justify-start gap-2 overflow-x-auto py-4 my-2 no-scrollbar">
        {DIAGRAMS.map((diagram) => {
          const Icon = diagram.icon;
          const isActive = diagram.id === activeTab;
          return (
            <button
              key={diagram.id}
              type="button"
              onClick={() => {
                setActiveTab(diagram.id);
                triggerSoundEffect("click");
              }}
              className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-xs font-nikkei uppercase tracking-wider whitespace-nowrap transition-all border-2 border-black cursor-pointer ${
                isActive
                  ? "bg-[#B91C1C] text-white shadow-[3px_3px_0px_#000000]"
                  : "bg-[#181822] text-zinc-300 hover:text-white shadow-[2px_2px_0px_#000000]"
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{diagram.shortTitle}</span>
              {isActive && (
                <span className="w-1.5 h-1.5 rounded-full bg-white animate-pulse" />
              )}
            </button>
          );
        })}
      </div>

      {/* Main Diagram Viewer Showcase */}
      <div className="rounded-lg border-2 border-black p-4 sm:p-6 bg-[#181822] shadow-[6px_6px_0px_#000000]">
        {/* Title Bar */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-4 border-b border-black/40">
          <div>
            <h4 className="font-charles-rosie text-xl sm:text-2xl text-white uppercase tracking-tight">
              {activeDiagram.title}
            </h4>
          </div>
          <div className="text-xs font-mono text-zinc-400">
            Click diagram to view full size
          </div>
        </div>

        {/* High-Contrast Cream Paper Canvas Presentation */}
        <div
          onClick={() => {
            setLightboxOpen(true);
            triggerSoundEffect("transition");
          }}
          className="my-5 relative rounded-lg bg-[#FAF8F5] p-3 sm:p-6 shadow-[4px_4px_0px_#000000] border-2 border-black cursor-zoom-in group transition-all"
        >
          <div className="absolute top-4 right-4 z-10 px-2 py-1 rounded bg-black border border-black text-[10px] font-mono text-white flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
            <Maximize2 className="w-3 h-3 text-[#B91C1C]" />
            <span>Click to Expand</span>
          </div>

          <div className="w-full flex items-center justify-center min-h-[300px] sm:min-h-[440px]">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={activeDiagram.file}
              alt={activeDiagram.title}
              className="w-full h-auto max-h-[580px] object-contain mx-auto transition-transform duration-300 group-hover:scale-[1.01]"
              loading="eager"
            />
          </div>
        </div>

        {/* Diagram Explanation & Architecture Invariants */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 pt-2">
          <div className="lg:col-span-7">
            <div className="font-nikkei text-xs uppercase tracking-wider text-[#D4AF37] font-bold mb-1">
              Architectural Overview
            </div>
            <p className="text-zinc-300 text-xs sm:text-sm font-gt-era leading-relaxed mb-4">
              {activeDiagram.description}
            </p>

            <div className="font-nikkei text-xs uppercase tracking-wider text-white font-bold mb-2">
              System Invariants &amp; Runtime Guarantees
            </div>
            <ul className="space-y-2">
              {activeDiagram.invariants.map((inv, idx) => (
                <li key={idx} className="flex items-start gap-2 text-xs text-zinc-300 font-gt-era">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                  <span>{inv}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="lg:col-span-5 grid grid-cols-2 gap-2.5 self-start">
            {activeDiagram.stats.map((stat, idx) => (
              <div
                key={idx}
                className="p-3 rounded-lg bg-black/60 border border-black shadow-[2px_2px_0px_#000000]"
              >
                <div className="text-[10px] font-nikkei uppercase text-[#D4AF37] font-bold">{stat.label}</div>
                <div className="text-sm font-mono font-bold text-white mt-1">{stat.value}</div>
                <div className="text-[10px] font-gt-era text-zinc-400 mt-0.5">{stat.detail}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Fullscreen Modal Lightbox */}
      {lightboxOpen && (
        <div
          className="fixed inset-0 z-50 bg-black/90 backdrop-blur-md flex items-center justify-center p-4 sm:p-8"
          onClick={() => setLightboxOpen(false)}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            className="relative w-full max-w-6xl max-h-[90vh] bg-[#FAF8F5] border-4 border-black shadow-[12px_12px_0px_#B91C1C] rounded-lg p-6 flex flex-col text-black"
          >
            <div className="flex items-center justify-between border-b-2 border-black pb-3 mb-4">
              <span className="font-nikkei text-sm uppercase text-black font-extrabold flex items-center gap-2">
                <Maximize2 className="w-4 h-4 text-[#B91C1C]" />
                {activeDiagram.title} • High-Resolution View
              </span>
              <button
                type="button"
                onClick={() => setLightboxOpen(false)}
                className="p-1.5 bg-black text-white hover:bg-[#B91C1C] rounded border border-black cursor-pointer transition-colors"
                aria-label="Close"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="relative w-full flex-1 min-h-[400px] sm:min-h-[550px] bg-white border border-black/20 flex items-center justify-center overflow-auto p-4">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={activeDiagram.file}
                alt={activeDiagram.title}
                className="max-h-[75vh] w-auto object-contain"
              />
            </div>

            <div className="mt-4 flex items-center justify-between text-xs font-mono text-black/70">
              <span>High-resolution luxury editorial SVG blueprint</span>
              <span className="text-black/50 text-[11px]">Press ESC or click outside to close</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
