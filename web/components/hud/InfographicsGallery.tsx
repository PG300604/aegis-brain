"use client";

import React, { useState, useEffect } from "react";
import Image from "next/image";
import {
  Cpu,
  Layers,
  Globe,
  ShieldCheck,
  Zap,
  TrendingUp,
  Smartphone,
  Maximize2,
  Download,
  CheckCircle2,
  X,
  ZoomIn,
  ZoomOut,
  RotateCcw,
  Sparkles,
  ArrowRight,
  ExternalLink,
} from "lucide-react";

interface DiagramData {
  id: string;
  title: string;
  shortTitle: string;
  file: string;
  category: string;
  badge: string;
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
    badge: "End-to-End Orchestration",
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
    badge: "Token Arbitrage Engine",
    icon: Layers,
    description:
      "Strict separation of cognitive authority across 3 distinct tiers. High-cognition frontier models govern architecture and verification, domain subagents audit and coach, while free local workers churn out code implementations at zero marginal token cost.",
    invariants: [
      "Tier 1 (Senior Boss): Fable 5.1 / Opus 5.5 / Gemini 4 / Argon — High Cognition & Sign-off",
      "Tier 2 (Junior Bosses): Domain Subagents — Orchestration, AST quality audits, and targeted coaching",
      "Tier 3 (Execution Workers): Hermes CLI / Ollama / Local MoE — 100% of raw code drafts at $0.00/token",
      "Coaching Convergence Loop: Automated compiler and linter feedback loops before escalation",
    ],
    stats: [
      { label: "Tier 1 Cost", value: "100%", detail: "High Cognition Only" },
      { label: "Tier 3 Cost", value: "$0.00", detail: "Local Hardware Free" },
      { label: "Draft Generation", value: "0 tokens", detail: "Zero Frontier Waste" },
      { label: "Escalation Rate", value: "<4.2%", detail: "Autonomous Convergence" },
    ],
  },
  {
    id: "agents",
    title: "Multi-Chassis Universal Compatibility",
    shortTitle: "Universal Hosts",
    file: "/infographics/infographic-universal-agents.svg",
    category: "Host Support",
    badge: "Cross-Agent Protocol",
    icon: Globe,
    description:
      "AegisBrain operates as an invisible sidecar infrastructure across all leading AI coding CLI chassis without vendor lock-in, proprietary runtime entrapment, or breaking developer workflows.",
    invariants: [
      "Antigravity CLI: Native Zero-Prompt pre-flight, memory hooks, and prompt interception",
      "Claude Code: Subagent tooling, CLAUDE.md integration, and automated PR guardrails",
      "OpenCode & Codex: Headless execution harness, benchmark verification, and tool dispatch",
      "Hermes & Gemini CLI: Local token arbitrage routing and real-time terminal streaming",
    ],
    stats: [
      { label: "Supported Hosts", value: "6 Engines", detail: "Native CLI Shims" },
      { label: "Config Overhead", value: "Zero Flags", detail: "Automatic Detection" },
      { label: "State Sync", value: "Shared DB", detail: "Single SQLite WAL" },
      { label: "Lock-in Risk", value: "0%", detail: "GPL-3.0 Open Standard" },
    ],
  },
  {
    id: "gates",
    title: "4-Decision Quality Architecture Gate",
    shortTitle: "Quality Gates",
    file: "/infographics/infographic-quality-gate.svg",
    category: "Verification Pipeline",
    badge: "Zero-Defect AST Audit",
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
    badge: "24ms FTS5 vs 4,200ms Crawling",
    icon: Zap,
    description:
      "Empirically measured runtime performance comparing AegisBrain's indexed neural SQLite FTS5 store against the conventional approach of repeatedly crawling megabytes of unstructured session transcript files.",
    invariants: [
      "24ms instant FTS5 BM25 keyword & semantic retrieval vs 4,200ms raw JSONL file grep",
      "Persistent WAL indexing: background commits incur 0ms perceived latency during active agent turns",
      "Active context compacted to <=400 tokens during memory bootstrap (95.8% context window preserved)",
      "Zero memory leaks across 72+ hour continuous daemon execution stress tests",
    ],
    stats: [
      { label: "Aegis Recall", value: "24 ms", detail: "FTS5 Indexed Search" },
      { label: "Raw JSONL Crawl", value: "4,200 ms", detail: "Standard Assistant" },
      { label: "Speed Advantage", value: "175x Faster", detail: "Sub-Second Retrieval" },
      { label: "Context Window", value: "<400 tokens", detail: "Compacted Bootstrap" },
    ],
  },
  {
    id: "learning",
    title: "Autonomous Error-Reduction & Confidence Curve",
    shortTitle: "Learning Curve",
    file: "/infographics/infographic-learning-curve.svg",
    category: "Worker Convergence",
    badge: "Confidence Scoring",
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
    badge: "Whisper Shield & Keystroke Injection",
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
  const [zoomLevel, setZoomLevel] = useState<number>(1);

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

  const handleDownload = (file: string, title: string) => {
    const link = document.createElement("a");
    link.href = file;
    link.download = `${title.toLowerCase().replace(/\s+/g, "-")}.svg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <section className="relative w-full py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      {/* Section Header */}
      <div className="text-center max-w-3xl mx-auto mb-10">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/60 border border-cyan-500/30 text-cyan-400 font-mono text-xs uppercase tracking-wider mb-4">
          <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
          <span>Interactive Architectural Blueprints</span>
        </div>
        <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-white tracking-tight">
          High-Fidelity <span className="text-cyan-400">System Infographics</span>
        </h2>
        <p className="mt-4 text-base sm:text-lg text-zinc-400 leading-relaxed">
          Examine the exact hand-drawn Excalidraw architecture blueprints detailing multi-agent token arbitrage, sub-second neural memory indexing, and deterministic 24/7 mobile telemetry.
        </p>
      </div>

      {/* Navigation Pills Bar */}
      <div className="flex items-center justify-start sm:justify-center gap-2 overflow-x-auto pb-4 mb-8 no-scrollbar">
        {DIAGRAMS.map((diagram) => {
          const Icon = diagram.icon;
          const isActive = diagram.id === activeTab;
          return (
            <button
              key={diagram.id}
              onClick={() => {
                setActiveTab(diagram.id);
                setZoomLevel(1);
              }}
              className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs sm:text-sm font-medium whitespace-nowrap transition-all duration-200 border cursor-pointer ${
                isActive
                  ? "bg-cyan-500/15 border-cyan-400/80 text-cyan-300 shadow-[0_0_20px_rgba(0,240,255,0.25)]"
                  : "bg-zinc-900/60 border-zinc-800 text-zinc-400 hover:text-zinc-200 hover:border-zinc-700 hover:bg-zinc-800/40"
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? "text-cyan-400" : "text-zinc-500"}`} />
              <span>{diagram.shortTitle}</span>
              {isActive && (
                <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse" />
              )}
            </button>
          );
        })}
      </div>

      {/* Main Diagram Viewer Showcase */}
      <div className="glass-panel rounded-2xl border border-zinc-800/80 p-4 sm:p-6 lg:p-8 relative overflow-hidden shadow-2xl">
        {/* Subtle Ambient Radial Glow */}
        <div className="absolute top-0 right-1/4 w-96 h-96 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 left-1/4 w-96 h-96 bg-emerald-500/5 rounded-full blur-3xl pointer-events-none" />

        {/* Top Control Bar */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-zinc-800/80">
          <div>
            <div className="flex items-center gap-2.5">
              <span className="px-2.5 py-0.5 rounded-md text-[11px] font-mono uppercase font-semibold bg-cyan-950/80 text-cyan-400 border border-cyan-500/30">
                {activeDiagram.category}
              </span>
              <span className="px-2.5 py-0.5 rounded-md text-[11px] font-mono uppercase font-semibold bg-emerald-950/80 text-emerald-400 border border-emerald-500/30">
                {activeDiagram.badge}
              </span>
            </div>
            <h3 className="text-xl sm:text-2xl font-bold text-white mt-2">
              {activeDiagram.title}
            </h3>
          </div>

          <div className="flex items-center gap-2 w-full sm:w-auto justify-end">
            <button
              onClick={() => {
                setZoomLevel(1);
                setLightboxOpen(true);
              }}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-zinc-800/80 hover:bg-zinc-700/80 border border-zinc-700 text-xs font-mono text-zinc-300 hover:text-white transition-all cursor-pointer"
            >
              <Maximize2 className="w-3.5 h-3.5" />
              <span>Fullscreen Lightbox</span>
            </button>
            <button
              onClick={() => handleDownload(activeDiagram.file, activeDiagram.title)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-cyan-950/60 hover:bg-cyan-900/60 border border-cyan-500/40 text-xs font-mono text-cyan-300 hover:text-cyan-200 transition-all cursor-pointer"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Download SVG</span>
            </button>
          </div>
        </div>

        {/* High-Contrast Crisp White Canvas Presentation */}
        <div
          onClick={() => {
            setZoomLevel(1);
            setLightboxOpen(true);
          }}
          className="my-6 relative rounded-xl bg-white p-3 sm:p-6 shadow-2xl border border-zinc-300/80 cursor-zoom-in group transition-all duration-300 hover:border-cyan-400 hover:shadow-[0_0_35px_rgba(0,240,255,0.18)]"
        >
          {/* Subtle Canvas Tag */}
          <div className="absolute top-4 right-4 z-10 px-2 py-1 rounded bg-zinc-900/85 backdrop-blur border border-zinc-700 text-[10px] font-mono text-zinc-300 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
            <Maximize2 className="w-3 h-3 text-cyan-400" />
            <span>Click to Expand</span>
          </div>

          <div className="w-full flex items-center justify-center min-h-[340px] sm:min-h-[460px] lg:min-h-[540px]">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={activeDiagram.file}
              alt={activeDiagram.title}
              className="max-h-[580px] w-auto object-contain mx-auto transition-transform duration-300 group-hover:scale-[1.01]"
              loading="eager"
            />
          </div>
        </div>

        {/* Diagram Explanation & Architecture Invariants */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 pt-4">
          <div className="lg:col-span-7">
            <h4 className="text-sm font-semibold font-mono uppercase text-zinc-400 tracking-wider mb-2">
              Architectural Overview
            </h4>
            <p className="text-zinc-300 text-sm leading-relaxed mb-4">
              {activeDiagram.description}
            </p>

            <h4 className="text-xs font-semibold font-mono uppercase text-cyan-400 tracking-wider mb-2">
              System Invariants & Runtime Guarantees
            </h4>
            <ul className="space-y-2">
              {activeDiagram.invariants.map((inv, idx) => (
                <li key={idx} className="flex items-start gap-2 text-xs sm:text-sm text-zinc-300">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                  <span>{inv}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="lg:col-span-5 grid grid-cols-2 gap-3 self-start">
            {activeDiagram.stats.map((stat, idx) => (
              <div
                key={idx}
                className="p-3.5 rounded-xl bg-zinc-900/60 border border-zinc-800/80 hover:border-zinc-700 transition-colors"
              >
                <div className="text-[11px] font-mono text-zinc-400 uppercase">
                  {stat.label}
                </div>
                <div className="text-xl sm:text-2xl font-black font-mono text-cyan-400 mt-1">
                  {stat.value}
                </div>
                <div className="text-[10px] font-mono text-zinc-500 mt-0.5">
                  {stat.detail}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Fullscreen Lightbox Modal */}
      {lightboxOpen && (
        <div
          role="dialog"
          aria-modal="true"
          className="fixed inset-0 z-50 bg-black/90 backdrop-blur-md flex flex-col items-center justify-center p-4"
        >
          {/* Lightbox Toolbar */}
          <div className="w-full max-w-6xl flex items-center justify-between pb-3 text-white border-b border-zinc-800 mb-4">
            <div className="flex items-center gap-3">
              <span className="font-mono text-xs text-cyan-400 uppercase font-bold">
                {activeDiagram.badge}
              </span>
              <span className="text-sm sm:text-base font-bold truncate">
                {activeDiagram.title}
              </span>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => setZoomLevel((z) => Math.max(0.6, z - 0.2))}
                className="p-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 hover:text-white"
                title="Zoom Out"
              >
                <ZoomOut className="w-4 h-4" />
              </button>
              <button
                onClick={() => setZoomLevel(1)}
                className="p-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 hover:text-white text-xs font-mono"
                title="Reset Zoom"
              >
                <RotateCcw className="w-4 h-4" />
              </button>
              <button
                onClick={() => setZoomLevel((z) => Math.min(2.5, z + 0.2))}
                className="p-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 hover:text-white"
                title="Zoom In"
              >
                <ZoomIn className="w-4 h-4" />
              </button>
              <button
                onClick={() => handleDownload(activeDiagram.file, activeDiagram.title)}
                className="p-2 rounded-lg bg-cyan-950/80 border border-cyan-500/40 text-cyan-300 hover:text-white"
                title="Download SVG"
              >
                <Download className="w-4 h-4" />
              </button>
              <button
                onClick={() => setLightboxOpen(false)}
                className="p-2 rounded-lg bg-red-950/80 border border-red-500/40 text-red-300 hover:text-white ml-2"
                title="Close (Esc)"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Modal Lightbox Content */}
          <div className="relative w-full max-w-6xl max-h-[82vh] overflow-auto rounded-xl bg-white p-4 sm:p-8 flex items-center justify-center shadow-2xl border border-zinc-200">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={activeDiagram.file}
              alt={activeDiagram.title}
              style={{ transform: `scale(${zoomLevel})` }}
              className="max-h-[75vh] w-auto object-contain transition-transform duration-200"
            />
          </div>
        </div>
      )}
    </section>
  );
}
