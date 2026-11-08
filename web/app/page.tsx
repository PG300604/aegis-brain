"use client";

import React, { useState, useEffect } from "react";
import Image from "next/image";
import dynamic from "next/dynamic";
import {
  Shield,
  Terminal,
  Cpu,
  Database,
  Zap,
  Sparkles,
  CheckCircle2,
  ChevronRight,
  Download,
  ExternalLink,
  Activity,
  ArrowUpRight,
  GitBranch,
  Layers,
  Radio,
  FileCode,
  HardDrive,
  Check,
  Copy,
} from "lucide-react";

import {
  TopNav,
  TerminalInstall,
  StopwatchDial,
  ArbitrageCalculator,
  TelegramSimulator,
  QualityGateCards,
} from "@/components/hud";

// Dynamically import client-heavy / WebGL components with ssr: false
const NeuralMonolithCanvas = dynamic(
  () => import("@/components/webgl/NeuralMonolithCanvas"),
  { ssr: false }
);

const MobileExperience = dynamic(
  () => import("@/components/mobile/MobileExperience"),
  { ssr: false }
);

export default function Home() {
  const [mounted, setMounted] = useState(false);
  const [copiedWhl, setCopiedWhl] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div className="relative min-h-screen bg-[#030305] text-[#E2E8F0] overflow-x-hidden">
      {/* 
        ====================================================================
        MOBILE EXPERIENCE (< 768px):
        Lightweight, 2.5D CSS GPU-accelerated rotating obsidian crystal,
        interactive touch controls, and zero WebGL crash risk on phones.
        ====================================================================
      */}
      <div className="block md:hidden">
        <MobileExperience />
      </div>

      {/* 
        ====================================================================
        DESKTOP EXPERIENCE (>= 768px):
        5 Cinematic Acts with WebGL Obsidian Monolith, Navier-Stokes Token
        Fluid Particle Advection, Glass HUD Panels, and Interactive Benchmarks.
        ====================================================================
      */}
      <div className="hidden md:block">
        {/* Navigation Bar */}
        <TopNav />

        {/* ================================================================ */}
        {/* ACT 1: THE MONOLITH AWAKENS (Hero & Installation)                 */}
        {/* ================================================================ */}
        <section
          id="hero"
          className="relative min-h-screen flex flex-col justify-center items-center pt-24 pb-16 px-6 overflow-hidden"
        >
          {/* Background WebGL Monolith Canvas */}
          <div className="absolute inset-0 z-0 pointer-events-auto">
            {mounted && <NeuralMonolithCanvas />}
          </div>

          {/* Foreground Hero HUD Overlay */}
          <div className="relative z-10 max-w-5xl mx-auto text-center space-y-6 pt-12">
            {/* Status Pills */}
            <div className="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full bg-cyan-950/40 border border-cyan-500/30 backdrop-blur-md text-xs font-mono">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
              </span>
              <span className="text-cyan-400 font-semibold tracking-wider">
                AEGISBRAIN v0.4.0
              </span>
              <span className="text-zinc-500">|</span>
              <span className="text-zinc-300">
                24/7 DAEMON :8765 ACTIVE
              </span>
              <span className="text-zinc-500">|</span>
              <span className="text-emerald-400 font-medium">
                WIN32 KEEPALIVE GUARD
              </span>
            </div>

            {/* Hero Main Headline */}
            <h1 className="text-4xl lg:text-6xl font-extrabold tracking-tight text-white leading-[1.1] max-w-4xl mx-auto">
              Autonomous 24/7 Multi-Tier Agent Engine &amp;{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 text-glow-cyan">
                Sub-Second Neural Memory
              </span>
            </h1>

            {/* Hero Subtitle */}
            <p className="text-base lg:text-lg text-zinc-300 max-w-3xl mx-auto leading-relaxed">
              Stop burning expensive frontier model tokens on repetitive boilerplate and crawling sluggish multi-megabyte session logs. AegisBrain delivers deterministic 3-tier local token arbitrage, 24ms SQLite FTS5 neural recall, and permanent Telegram CLI operations to your AI coding workflow.
            </p>

            {/* Key Metrics HUD Bar */}
            <div className="grid grid-cols-4 gap-4 max-w-3xl mx-auto pt-2">
              <div className="glass-panel rounded-xl p-3 border-cyan-500/20 text-center">
                <div className="text-2xl font-bold font-mono text-cyan-400">
                  24 ms
                </div>
                <div className="text-[11px] text-zinc-400 font-mono uppercase tracking-wider">
                  Neural Recall (FTS5)
                </div>
              </div>
              <div className="glass-panel rounded-xl p-3 border-emerald-500/20 text-center">
                <div className="text-2xl font-bold font-mono text-emerald-400">
                  95.8%
                </div>
                <div className="text-[11px] text-zinc-400 font-mono uppercase tracking-wider">
                  Token Arbitrage Savings
                </div>
              </div>
              <div className="glass-panel rounded-xl p-3 border-purple-500/20 text-center">
                <div className="text-2xl font-bold font-mono text-purple-400">
                  24/7
                </div>
                <div className="text-[11px] text-zinc-400 font-mono uppercase tracking-wider">
                  Win32 KeepAlive Shield
                </div>
              </div>
              <div className="glass-panel rounded-xl p-3 border-amber-500/20 text-center">
                <div className="text-2xl font-bold font-mono text-amber-400">
                  0%
                </div>
                <div className="text-[11px] text-zinc-400 font-mono uppercase tracking-wider">
                  Dropped Audio (25s Chunks)
                </div>
              </div>
            </div>

            {/* CLI Quick Terminal Installation */}
            <div id="install" className="pt-4 max-w-3xl mx-auto">
              <TerminalInstall />
            </div>
          </div>
        </section>

        {/* ================================================================ */}
        {/* ACT 2: SUB-SECOND NEURAL MEMORY CORE (Benchmarks & Architecture)  */}
        {/* ================================================================ */}
        <section
          id="benchmarks"
          className="relative py-28 px-6 max-w-7xl mx-auto border-t border-white/5"
        >
          {/* Ambient Glow */}
          <div className="absolute top-1/3 left-1/4 w-[500px] h-[300px] bg-cyan-500/10 blur-[130px] rounded-full pointer-events-none" />

          {/* Section Heading */}
          <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/60 border border-cyan-500/30 text-cyan-400 font-mono text-xs">
              <Database className="w-3.5 h-3.5" />
              <span>ACT II &bull; NEURAL PERSISTENCE CORE</span>
            </div>
            <h2 className="text-3xl lg:text-4xl font-bold tracking-tight text-white">
              Sub-Second FTS5 Neural Recall vs. Sluggish Raw Session Crawling
            </h2>
            <p className="text-sm lg:text-base text-zinc-400 leading-relaxed">
              Standard AI coding assistants crawl raw, multi-megabyte JSONL session files on every user promptâ€”burning 12,400ms+ of disk latency and inflating context windows. AegisBrain maintains an indexed SQLite FTS5 database (<code>brain.db</code>), returning pinpoint semantic memories in 24ms within a compact &le;400 token payload.
            </p>
          </div>

          {/* Stopwatch Dial Interactive Benchmark */}
          <div className="mb-20">
            <StopwatchDial />
          </div>

          {/* Unified Architecture Diagram Showcase */}
          <div id="architecture" className="mt-20 space-y-6">
            <div className="text-center space-y-2">
              <span className="font-mono text-xs uppercase tracking-widest text-zinc-400">
                System Blueprint
              </span>
              <h3 className="text-2xl font-bold text-white">
                Unified End-to-End System Architecture
              </h3>
              <p className="text-sm text-zinc-400 max-w-2xl mx-auto">
                Comprehensive data flow connecting local SQLite WAL memory, Tier 1 frontier orchestrators, Tier 3 execution workers, and the 24/7 background Windows daemon.
              </p>
            </div>

            <div className="glass-panel rounded-2xl p-4 sm:p-6 border-white/10 shadow-[0_20px_50px_rgba(0,0,0,0.8)] relative overflow-hidden group">
              <div className="relative w-full overflow-hidden rounded-xl bg-white/95 p-3 flex justify-center items-center">
                <Image
                  src="/assets/architecture-unified.svg"
                  alt="AegisBrain Unified Architecture Diagram"
                  width={1240}
                  height={575}
                  className="w-full h-auto object-contain transition-transform duration-500 group-hover:scale-[1.01]"
                  priority
                />
              </div>

              {/* Blueprint Legend */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-6 border-t border-white/10 text-xs text-zinc-400">
                <div className="flex items-start gap-2.5">
                  <div className="w-2 h-2 rounded-full bg-cyan-400 mt-1 shrink-0" />
                  <div>
                    <strong className="text-zinc-200">SQLite FTS5 Memory Engine:</strong> Stores conversation transcripts, restore point snapshots, and error confidence ledgers with BM25 sub-second indexing.
                  </div>
                </div>
                <div className="flex items-start gap-2.5">
                  <div className="w-2 h-2 rounded-full bg-emerald-400 mt-1 shrink-0" />
                  <div>
                    <strong className="text-zinc-200">3-Tier Multi-Agent Distillation:</strong> Senior Boss Manager coaches local workers via zero frontier token drafting and automated syntax audits.
                  </div>
                </div>
                <div className="flex items-start gap-2.5">
                  <div className="w-2 h-2 rounded-full bg-purple-400 mt-1 shrink-0" />
                  <div>
                    <strong className="text-zinc-200">24/7 Telegram &amp; Win32 Service:</strong> Continuous background daemon backed by Scheduled Task with 25s Whisper audio chunking shield.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ================================================================ */}
        {/* ACT 3: TOKEN ARBITRAGE & MULTI-AGENT HIERARCHY                    */}
        {/* ================================================================ */}
        <section
          id="arbitrage"
          className="relative py-28 px-6 max-w-7xl mx-auto border-t border-white/5"
        >
          {/* Ambient Glow */}
          <div className="absolute top-1/2 right-1/4 w-[500px] h-[350px] bg-emerald-500/10 blur-[140px] rounded-full pointer-events-none" />

          {/* Section Heading */}
          <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-950/60 border border-emerald-500/30 text-emerald-400 font-mono text-xs">
              <Zap className="w-3.5 h-3.5" />
              <span>ACT III &bull; DETERMINISTIC TOKEN ARBITRAGE</span>
            </div>
            <h2 className="text-3xl lg:text-4xl font-bold tracking-tight text-white">
              Hierarchical 3-Tier Multi-Agent Token Arbitrage
            </h2>
            <p className="text-sm lg:text-base text-zinc-400 leading-relaxed">
              Frontier models (Gemini 4, Claude Opus 5.5, Fable 5.1, Argon) should strictly function as the <span className="text-white font-medium">Senior Boss (Brain)</span>: system architecture, invariant definitions, and error auditing. AegisBrain enforces the <span className="text-cyan-400 font-mono">Zero-Direct-Code Invariant</span>, offloading candidate code drafting to local workers for zero token spend.
            </p>
          </div>

          {/* Interactive Arbitrage Calculator */}
          <div className="mb-20">
            <ArbitrageCalculator />
          </div>

          {/* Hierarchy Pyramid Infographic Showcase */}
          <div className="space-y-6">
            <div className="text-center space-y-2">
              <span className="font-mono text-xs uppercase tracking-widest text-zinc-400">
                Division of Labor
              </span>
              <h3 className="text-2xl font-bold text-white">
                The 3-Tier Agent Hierarchy Pyramid
              </h3>
              <p className="text-sm text-zinc-400 max-w-2xl mx-auto">
                Strict operational separation of powers: strategic cognitive planning on top, targeted subagent dispatch in the middle, and high-volume local worker CLI execution at the foundation.
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
              {/* Infographic SVG Image */}
              <div className="lg:col-span-7 glass-panel rounded-2xl p-4 sm:p-6 border-white/10 shadow-[0_20px_50px_rgba(0,0,0,0.8)] group">
                <div className="relative w-full overflow-hidden rounded-xl bg-white/95 p-3 flex justify-center items-center">
                  <Image
                    src="/assets/infographic-hierarchy-pyramid.svg"
                    alt="AegisBrain 3-Tier Multi-Agent Hierarchy Pyramid"
                    width={1040}
                    height={870}
                    className="w-full h-auto object-contain transition-transform duration-500 group-hover:scale-[1.01]"
                  />
                </div>
              </div>

              {/* Tier Breakdown Descriptions */}
              <div className="lg:col-span-5 space-y-4">
                {/* Tier 1 Card */}
                <div className="glass-panel rounded-xl p-5 border-cyan-500/20 hover:border-cyan-400/40 transition-colors space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xs text-cyan-400 font-bold">
                      TIER 1 &bull; SENIOR BOSS (BRAIN)
                    </span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-500/30">
                      High Cognition
                    </span>
                  </div>
                  <h4 className="text-base font-semibold text-white">
                    Frontier Managers (Fable 5.1, Opus 5.5, Gemini 4, Argon)
                  </h4>
                  <p className="text-xs text-zinc-400 leading-relaxed">
                    Evaluates task severity and system headroom. Defines invariants, verifies candidate code, notices bugs, and coaches lower tiers. <strong className="text-zinc-200">Strict Invariant:</strong> Never wastes tokens typing boilerplate directly.
                  </p>
                </div>

                {/* Tier 2 Card */}
                <div className="glass-panel rounded-xl p-5 border-purple-500/20 hover:border-purple-400/40 transition-colors space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xs text-purple-400 font-bold">
                      TIER 2 &bull; JUNIOR BOSSES (SUBAGENTS)
                    </span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-500/30">
                      Domain Leads
                    </span>
                  </div>
                  <h4 className="text-base font-semibold text-white">
                    Specialized Leads (Backend, Frontend, Security, QA)
                  </h4>
                  <p className="text-xs text-zinc-400 leading-relaxed">
                    Translates architectural specs into execution directives. Dispatches commands to local worker CLIs, inspects AST graphs, and runs error-reduction coaching loops.
                  </p>
                </div>

                {/* Tier 3 Card */}
                <div className="glass-panel rounded-xl p-5 border-emerald-500/20 hover:border-emerald-400/40 transition-colors space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xs text-emerald-400 font-bold">
                      TIER 3 &bull; EXECUTION WORKERS (MUSCLE)
                    </span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-500/30">
                      $0.00 / token
                    </span>
                  </div>
                  <h4 className="text-base font-semibold text-white">
                    Local Workers (Hermes CLI, Ollama, Qwen2.5-Coder)
                  </h4>
                  <p className="text-xs text-zinc-400 leading-relaxed">
                    Executes heavy lifting, drafts boilerplate, writes repetitive tests, and creates implementations locally with free CPU/GPU tokens.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ================================================================ */}
        {/* ACT 4: TELEGRAM 24/7 REMOTE OPERATIONS & WIN32 SHIELD             */}
        {/* ================================================================ */}
        <section
          id="mobile"
          className="relative py-28 px-6 max-w-7xl mx-auto border-t border-white/5"
        >
          {/* Ambient Glow */}
          <div className="absolute top-1/3 left-1/3 w-[500px] h-[350px] bg-purple-500/10 blur-[150px] rounded-full pointer-events-none" />

          {/* Section Heading */}
          <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-950/60 border border-purple-500/30 text-purple-400 font-mono text-xs">
              <Radio className="w-3.5 h-3.5" />
              <span>ACT IV &bull; REMOTE TELEGRAM CLI &amp; WIN32 SHIELD</span>
            </div>
            <h2 className="text-3xl lg:text-4xl font-bold tracking-tight text-white">
              24/7 Remote Telegram Operations &amp; Whisper Chunking Shield
            </h2>
            <p className="text-sm lg:text-base text-zinc-400 leading-relaxed">
              Control your AI coding fleet from anywhere via <code>@HHAACLIBot</code>. Send voice memos with automatic 25-second FFmpeg chunking to prevent Whisper GPU crashes, inject in-flight terminal keystrokes via <code>/type</code>, and query context with <code>/btw</code> without stalling your models.
            </p>
          </div>

          {/* Interactive Telegram Smartphone Simulator */}
          <div className="mb-20">
            <TelegramSimulator />
          </div>

          {/* Mobile Operations Pipeline Infographic */}
          <div className="space-y-6">
            <div className="text-center space-y-2">
              <span className="font-mono text-xs uppercase tracking-widest text-zinc-400">
                Audio &amp; Terminal Architecture
              </span>
              <h3 className="text-2xl font-bold text-white">
                Deterministic Mobile-to-CLI Pipeline
              </h3>
              <p className="text-sm text-zinc-400 max-w-2xl mx-auto">
                How voice memos and remote commands safely traverse the Telegram gateway, Whisper transcriber, and local Antigravity keystroke injector.
              </p>
            </div>

            <div className="glass-panel rounded-2xl p-4 sm:p-6 border-white/10 shadow-[0_20px_50px_rgba(0,0,0,0.8)] group">
              <div className="relative w-full overflow-hidden rounded-xl bg-white/95 p-3 flex justify-center items-center">
                <Image
                  src="/assets/infographic-mobile-pipeline.svg"
                  alt="AegisBrain Mobile Operations & Whisper Pipeline"
                  width={1120}
                  height={620}
                  className="w-full h-auto object-contain transition-transform duration-500 group-hover:scale-[1.01]"
                />
              </div>

              {/* Feature Highlights Grid */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 pt-6 border-t border-white/10 text-xs">
                <div className="space-y-1">
                  <div className="font-mono text-purple-400 font-semibold flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-purple-400" />
                    25s Audio Slicer
                  </div>
                  <p className="text-zinc-400 text-[11px] leading-relaxed">
                    Slices voice files &gt;30s into overlapping 25s segments, preventing Whisper VRAM spikes and loop stalls.
                  </p>
                </div>

                <div className="space-y-1">
                  <div className="font-mono text-cyan-400 font-semibold flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
                    Win32 KeepAlive
                  </div>
                  <p className="text-zinc-400 text-[11px] leading-relaxed">
                    Windows Task Scheduler ensures background daemon resurrects silently on reboots and account switches.
                  </p>
                </div>

                <div className="space-y-1">
                  <div className="font-mono text-emerald-400 font-semibold flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                    /type Remote Interrupt
                  </div>
                  <p className="text-zinc-400 text-[11px] leading-relaxed">
                    Injects text directly into active Antigravity CLI sessions with automatic <code>/alt+m</code> submit.
                  </p>
                </div>

                <div className="space-y-1">
                  <div className="font-mono text-amber-400 font-semibold flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-amber-400" />
                    /btw Query Channel
                  </div>
                  <p className="text-zinc-400 text-[11px] leading-relaxed">
                    Queries memory and active status out-of-band without disturbing running code generation tasks.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ================================================================ */}
        {/* ACT 5: 4-DECISION QUALITY GATES & DOWNLOAD PORTAL                */}
        {/* ================================================================ */}
        <section
          id="quality-gates"
          className="relative py-28 px-6 max-w-7xl mx-auto border-t border-white/5"
        >
          {/* Ambient Glow */}
          <div className="absolute top-1/3 left-1/2 -translate-x-1/2 w-[600px] h-[350px] bg-amber-500/10 blur-[160px] rounded-full pointer-events-none" />

          {/* Section Heading */}
          <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-950/60 border border-amber-500/30 text-amber-400 font-mono text-xs">
              <Shield className="w-3.5 h-3.5" />
              <span>ACT V &bull; 4-DECISION QUALITY ARCHITECTURE</span>
            </div>
            <h2 className="text-3xl lg:text-4xl font-bold tracking-tight text-white">
              Autonomous Verification &amp; Security Shield
            </h2>
            <p className="text-sm lg:text-base text-zinc-400 leading-relaxed">
              Every candidate code output generated by Tier 3 workers must pass all four quality gates before entering the codebase. Flawed code triggers an automated coaching loop until zero errors remain.
            </p>
          </div>

          {/* Quality Gate Holographic Cards */}
          <div className="mb-20">
            <QualityGateCards />
          </div>

          {/* Quality Architecture Infographic */}
          <div className="space-y-6 mb-20">
            <div className="text-center space-y-2">
              <span className="font-mono text-xs uppercase tracking-widest text-zinc-400">
                Gate Flow Diagram
              </span>
              <h3 className="text-2xl font-bold text-white">
                The 4-Decision Quality Architecture Matrix
              </h3>
              <p className="text-sm text-zinc-400 max-w-2xl mx-auto">
                Step-by-step verification pipeline enforcing Karpathy simplicity, unslop distillation, security auditing, and dual-environment sandbox checks.
              </p>
            </div>

            <div className="glass-panel rounded-2xl p-4 sm:p-6 border-white/10 shadow-[0_20px_50px_rgba(0,0,0,0.8)] group">
              <div className="relative w-full overflow-hidden rounded-xl bg-white/95 p-3 flex justify-center items-center">
                <Image
                  src="/assets/infographic-quality-gate.svg"
                  alt="AegisBrain 4-Decision Quality Gate Infographic"
                  width={1100}
                  height={650}
                  className="w-full h-auto object-contain transition-transform duration-500 group-hover:scale-[1.01]"
                />
              </div>
            </div>
          </div>

          {/* Direct Download Artifacts Matrix */}
          <div className="glass-panel-glow rounded-3xl p-8 max-w-4xl mx-auto space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-6">
              <div>
                <h3 className="text-2xl font-bold text-white font-mono flex items-center gap-2">
                  <Download className="w-5 h-5 text-cyan-400" />
                  Direct Release Artifacts (v0.4.0)
                </h3>
                <p className="text-xs text-zinc-400 mt-1">
                  Production-certified Python wheel, source distributions, and container images.
                </p>
              </div>

              <a
                href="https://github.com/PG300604/aegis-brain/releases"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 text-xs font-mono px-4 py-2 rounded-full bg-cyan-500 text-black font-semibold hover:bg-cyan-400 transition-colors shrink-0"
              >
                <span>View All Releases</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </a>
            </div>

            <div className="space-y-3 font-mono text-xs">
              {/* Row 1: Wheel */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between p-3.5 rounded-xl bg-white/5 border border-white/10 hover:border-cyan-500/30 transition-colors gap-3">
                <div className="flex items-center gap-3">
                  <HardDrive className="w-4 h-4 text-cyan-400 shrink-0" />
                  <div>
                    <div className="text-zinc-200 font-medium">aegis_brain-0.4.0-py3-none-any.whl</div>
                    <div className="text-[11px] text-zinc-500">Universal Python Wheel &bull; 62.4 KB</div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-[10px] text-zinc-400 bg-black/40 px-2 py-1 rounded border border-white/5">
                    SHA256: 4f98...e1a0
                  </span>
                  <a
                    href="https://github.com/PG300604/aegis-brain/releases/download/v0.4.0/aegis_brain-0.4.0-py3-none-any.whl"
                    className="p-1.5 rounded-lg bg-cyan-950/60 text-cyan-400 border border-cyan-500/30 hover:bg-cyan-900/60"
                    title="Download Wheel"
                  >
                    <Download className="w-3.5 h-3.5" />
                  </a>
                </div>
              </div>

              {/* Row 2: Tarball */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between p-3.5 rounded-xl bg-white/5 border border-white/10 hover:border-cyan-500/30 transition-colors gap-3">
                <div className="flex items-center gap-3">
                  <FileCode className="w-4 h-4 text-emerald-400 shrink-0" />
                  <div>
                    <div className="text-zinc-200 font-medium">aegis_brain-0.4.0.tar.gz</div>
                    <div className="text-[11px] text-zinc-500">Source Distribution &bull; 58.1 KB</div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-[10px] text-zinc-400 bg-black/40 px-2 py-1 rounded border border-white/5">
                    SHA256: 9b23...7c81
                  </span>
                  <a
                    href="https://github.com/PG300604/aegis-brain/releases/download/v0.4.0/aegis_brain-0.4.0.tar.gz"
                    className="p-1.5 rounded-lg bg-emerald-950/60 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-900/60"
                    title="Download Source Tarball"
                  >
                    <Download className="w-3.5 h-3.5" />
                  </a>
                </div>
              </div>

              {/* Row 3: Docker */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between p-3.5 rounded-xl bg-white/5 border border-white/10 hover:border-purple-500/30 transition-colors gap-3">
                <div className="flex items-center gap-3">
                  <Cpu className="w-4 h-4 text-purple-400 shrink-0" />
                  <div>
                    <div className="text-zinc-200 font-medium">ghcr.io/pg300604/aegis-brain:latest</div>
                    <div className="text-[11px] text-zinc-500">Container Image &bull; Multi-Arch (amd64, arm64)</div>
                  </div>
                </div>
                <button
                  onClick={() => {
                    navigator.clipboard.writeText("docker pull ghcr.io/pg300604/aegis-brain:latest");
                    setCopiedWhl(true);
                    setTimeout(() => setCopiedWhl(false), 2000);
                  }}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-purple-950/60 text-purple-400 border border-purple-500/30 hover:bg-purple-900/60 text-[11px]"
                >
                  {copiedWhl ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                  <span>{copiedWhl ? "Copied" : "Copy Pull Command"}</span>
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* ================================================================ */}
        {/* FOOTER & SYSTEM SIGN-OFF                                          */}
        {/* ================================================================ */}
        <footer className="relative py-16 px-6 border-t border-white/10 bg-[#020203]">
          <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-8">
            {/* Brand & Mission */}
            <div className="space-y-2 text-center md:text-left">
              <div className="flex items-center justify-center md:justify-start gap-2">
                <div className="w-7 h-7 rounded-lg bg-cyan-950/80 border border-cyan-500/40 flex items-center justify-center">
                  <Shield className="w-4 h-4 text-cyan-400" />
                </div>
                <span className="font-bold font-mono tracking-wider text-base text-white">
                  AEGIS<span className="text-cyan-400">BRAIN</span>
                </span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-400 border border-emerald-500/30">
                  DAEMON 24/7
                </span>
              </div>
              <p className="text-xs text-zinc-400 max-w-sm">
                Autonomous 24/7 multi-tier agent engine &amp; sub-second neural memory for AI coding assistants. Released under the MIT License.
              </p>
            </div>

            {/* Quick Links */}
            <div className="flex flex-wrap items-center justify-center gap-6 text-xs text-zinc-400 font-mono">
              <a href="#hero" className="hover:text-cyan-400 transition-colors">
                Top
              </a>
              <a href="#benchmarks" className="hover:text-cyan-400 transition-colors">
                Benchmarks
              </a>
              <a href="#arbitrage" className="hover:text-cyan-400 transition-colors">
                Token Arbitrage
              </a>
              <a href="#mobile" className="hover:text-cyan-400 transition-colors">
                Telegram Bot
              </a>
              <a href="#quality-gates" className="hover:text-cyan-400 transition-colors">
                Quality Gates
              </a>
              <a href="/llms.txt" className="hover:text-cyan-400 transition-colors text-zinc-300">
                llms.txt (GEO)
              </a>
              <a
                href="https://github.com/PG300604/aegis-brain"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-cyan-400 transition-colors flex items-center gap-1"
              >
                <span>GitHub</span>
                <ExternalLink className="w-3 h-3 text-zinc-500" />
              </a>
            </div>

            {/* Copyright & Author */}
            <div className="text-xs text-zinc-500 font-mono text-center md:text-right space-y-1">
              <div>&copy; 2026 Priyanshu &bull; Open Source</div>
              <div className="text-[11px] text-zinc-600">
                Santioni Spirits-inspired Luxury HUD Architecture
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}
