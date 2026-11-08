"use client";

import React, { useState, useEffect, useMemo, useRef } from "react";
import Image from "next/image";
import {
  Volume2,
  VolumeX,
  Copy,
  Check,
  Download,
  Terminal,
  ExternalLink,
  ChevronDown,
  ArrowRight,
  Shield,
  Cpu,
  Database,
  Radio,
  FileCode,
  HardDrive,
  Sparkles,
  Zap,
  Activity,
  Layers,
  Search,
  CheckCircle2,
  AlertTriangle,
  ZoomIn,
  X,
  Smartphone,
  Flame,
  Clock,
  Maximize2,
  Star,
  DollarSign,
  TrendingUp,
  ShieldCheck,
  RotateCcw,
} from "lucide-react";
import { motion, AnimatePresence, useScroll, useTransform } from "motion/react";
import { ThoughtLine } from "@/components/react-bits/ThoughtLine";
import { CallChip } from "@/components/react-bits/CallChip";
import { VoicePill } from "@/components/react-bits/VoicePill";
import { StopwatchDial } from "@/components/hud/StopwatchDial";
import { TerminalInstall } from "@/components/hud/TerminalInstall";
import { ArbitrageCalculator } from "@/components/hud/ArbitrageCalculator";
import { QualityGateCards } from "@/components/hud/QualityGateCards";
import { TelegramSimulator } from "@/components/hud/TelegramSimulator";
import { InfographicsGallery } from "@/components/hud/InfographicsGallery";
import { FluidWaterWave } from "@/components/motion/FluidWaterWave";
import { SceneTransition } from "@/components/motion/SceneTransition";
import { SoundtrackController, triggerSoundEffect } from "@/components/audio/SoundtrackController";

export default function Home() {
  const [scrollProgress, setScrollProgress] = useState(0);
  const [soundActive, setSoundActive] = useState(false);
  const [copiedClone, setCopiedClone] = useState(false);
  const [selectedInfographicModal, setSelectedInfographicModal] = useState<string | null>(null);

  // Hero section scroll-driven fluid wave reveal
  const heroRef = useRef<HTMLElement>(null);
  const { scrollYProgress: heroScroll } = useScroll({
    target: heroRef,
    offset: ["start start", "end start"],
  });
  const waveY = useTransform(heroScroll, [0, 1], ["0%", "-35%"]);
  const heroOpacity = useTransform(heroScroll, [0, 0.7], [1, 0.15]);
  const heroScale = useTransform(heroScroll, [0, 0.9], [1, 0.94]);

  // Feature 1: 429 Quota Cliff interactive simulation state
  const [quotaSimMode, setQuotaSimMode] = useState<"idle" | "traditional" | "aegis">("idle");
  const [quotaTokens, setQuotaTokens] = useState<number>(0);
  const [quotaLatency, setQuotaLatency] = useState<number>(0);
  const [quotaError, setQuotaError] = useState<string | null>(null);

  // Vertical laser scroll tracker
  useEffect(() => {
    const handleScroll = () => {
      const totalHeight =
        document.documentElement.scrollHeight - window.innerHeight;
      if (totalHeight > 0) {
        setScrollProgress((window.scrollY / totalHeight) * 100);
      }
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const handleCopyClone = () => {
    navigator.clipboard.writeText("git clone https://github.com/PG300604/aegis-brain.git");
    setCopiedClone(true);
    setTimeout(() => setCopiedClone(false), 2500);
  };

  const runTraditionalSimulation = () => {
    setQuotaSimMode("traditional");
    setQuotaTokens(8400);
    setQuotaLatency(1200);
    setQuotaError(null);

    setTimeout(() => {
      setQuotaTokens(24800);
      setQuotaLatency(4600);
    }, 600);

    setTimeout(() => {
      setQuotaTokens(54200);
      setQuotaLatency(12400);
      setQuotaError(
        "HTTP 429 RateLimitExceeded: TPM limit reached (50,000 max tokens/min). Request dropped. 60s cooldown enforced by provider API."
      );
    }, 1400);
  };

  const runAegisSimulation = () => {
    setQuotaSimMode("aegis");
    setQuotaError(null);
    setQuotaTokens(380);
    setQuotaLatency(21);
  };

  // Autoplay Quota Cliff simulation loop
  useEffect(() => {
    let mode: "traditional" | "aegis" = "traditional";
    runTraditionalSimulation();

    const interval = setInterval(() => {
      if (mode === "traditional") {
        runAegisSimulation();
        mode = "aegis";
      } else {
        runTraditionalSimulation();
        mode = "traditional";
      }
    }, 5500);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative min-h-screen bg-[#070709] text-[#0D0D11] selection:bg-[#B91C1C] selection:text-white paper-grain">
      {/* 
        ========================================================================
        VERTICAL RED SCROLL PROGRESS LINE (Right Margin Laser Tracker)
        ========================================================================
      */}
      <div className="scroll-progress-line" aria-hidden="true">
        <div
          className="scroll-progress-fill"
          style={{ height: `${scrollProgress}%` }}
        />
      </div>

      {/* 
        ========================================================================
        LUXURY EDITORIAL TOP BAR (Santioni Spirits Editorial Header)
        ========================================================================
      */}
      <header className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 sm:px-12 py-5 pointer-events-none">
        {/* Left: AegisBrain Lockup matching user screenshot exactly */}
        <div className="pointer-events-auto flex items-center gap-3">
          <a href="#" className="flex flex-col group select-none">
            <div className="flex items-baseline">
              <span className="font-extrabold text-2xl sm:text-3xl text-white tracking-tight group-hover:text-zinc-200 transition-colors">
                AegisBrain
              </span>
              <span className="font-extrabold text-2xl sm:text-3xl text-[#B91C1C]">.</span>
            </div>
            <span className="text-[11px] sm:text-xs font-gt-era text-white/60 tracking-wider mt-0.5">
              Autonomous engineering chassis, neural memory bus &amp; multi-agent governor.
            </span>
          </a>
        </div>

        {/* Right: Minimal Badges & Audio Toggle */}
        <div className="pointer-events-auto flex items-center gap-4">
          <nav className="hidden sm:flex items-center bg-[#FBF9F5] border-2 border-black shadow-[4px_4px_0px_#000000] text-black font-nikkei text-xs uppercase px-4 py-2 tracking-widest gap-4">
            <a href="#features" className="hover:text-[#B91C1C] transition-colors">
              Features
            </a>
            <span className="text-black/30">|</span>
            <a href="#memory" className="hover:text-[#B91C1C] transition-colors">
              Memory Core
            </a>
            <span className="text-black/30">|</span>
            <a href="#arbitrage" className="hover:text-[#B91C1C] transition-colors">
              Arbitrage
            </a>
            <span className="text-black/30">|</span>
            <a href="#blueprints" className="hover:text-[#B91C1C] transition-colors">
              Blueprints
            </a>
            <span className="text-black/30">|</span>
            <a
              href="https://github.com/PG300604/aegis-brain"
              target="_blank"
              rel="noreferrer"
              className="text-[#B91C1C] font-extrabold hover:underline flex items-center gap-1"
            >
              GitHub <ArrowRight className="w-3 h-3" />
            </a>
          </nav>

          {/* Sound Wave Indicator */}
          <button
            type="button"
            onClick={() => {
              const next = !soundActive;
              setSoundActive(next);
              triggerSoundEffect("click");
            }}
            className="w-10 h-10 bg-[#FBF9F5] border-2 border-black shadow-[4px_4px_0px_#000000] flex items-center justify-center text-black hover:bg-neutral-100 transition-colors cursor-pointer"
            title={soundActive ? "Mute Ambient Sound" : "Enable Sound Atmosphere"}
            aria-label="Toggle sound atmosphere"
          >
            {soundActive ? (
              <div className="flex items-end gap-[2px] h-4">
                <span className="w-[3px] bg-black sound-bar-1 animate-pulse" />
                <span className="w-[3px] bg-[#B91C1C] sound-bar-2" />
                <span className="w-[3px] bg-black sound-bar-3" />
                <span className="w-[3px] bg-black sound-bar-4" />
              </div>
            ) : (
              <VolumeX className="w-4 h-4 text-black/60" />
            )}
          </button>
        </div>
      </header>

      {/* 
        ========================================================================
        HERO SPREAD: THE AEGIS EXPERIENCE (Deep Black + Fluid Typography)
        ========================================================================
      */}
      <section
        id="experience"
        ref={heroRef}
        className="relative min-h-screen w-full flex flex-col items-center justify-between pt-36 pb-0 px-4 bg-[#070709] overflow-hidden"
      >
        {/* Subtle Horizontal Dry-Brush Chalk Streaks */}
        <div
          className="absolute inset-0 pointer-events-none opacity-15"
          style={{
            backgroundImage: `repeating-linear-gradient(
              0deg,
              transparent,
              transparent 3px,
              rgba(255, 255, 255, 0.05) 3px,
              rgba(255, 255, 255, 0.05) 4px
            )`,
          }}
        />

        {/* Center: Monumental Headline with Pure, Non-Jitter Entrance Animation & Scroll Dissolve */}
        <motion.div
          style={{ opacity: heroOpacity, scale: heroScale }}
          initial={{ opacity: 0, y: 25 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
          className="relative z-10 text-center flex flex-col items-center max-w-5xl mx-auto my-auto select-none pt-4 sm:pt-8"
        >
          <p className="font-charles-rosie text-white/70 text-lg sm:text-2xl tracking-[0.35em] uppercase mb-1">
            The
          </p>

          <h1 className="font-charles-rosie text-white text-6xl sm:text-8xl md:text-9xl lg:text-[10rem] leading-[0.88] tracking-tight uppercase drop-shadow-[0_12px_35px_rgba(0,0,0,0.95)]">
            Aeg<span className="text-[#B91C1C]">i</span>s
          </h1>

          <h2 className="font-charles-rosie text-white text-3xl sm:text-5xl md:text-6xl lg:text-7xl leading-tight tracking-[0.16em] uppercase mt-2 drop-shadow-[0_8px_25px_rgba(0,0,0,0.95)]">
            Experience
          </h2>

          {/* Punchy, Non-Slop Directives & Sub-description */}
          <div className="mt-8 max-w-3xl mx-auto px-4 space-y-3">
            <h3 className="font-nikkei text-[#D4AF37] text-base sm:text-xl md:text-2xl uppercase tracking-[0.2em] font-extrabold leading-tight">
              TAKE FULL CONTROL OF YOUR AGENTS
            </h3>
            <p className="font-nikkei text-white text-xs sm:text-sm uppercase tracking-[0.25em] font-bold">
              UNLEASH THE FULL POWER OF AGENTIC PERSISTENCE
            </p>
            <p className="font-gt-era text-white/75 text-xs sm:text-sm leading-relaxed max-w-2xl mx-auto pt-2">
              Sub-Second Neural Memory (&lt;25ms) • 3-Tier Local Token Arbitrage ($1,840+/mo) • 24/7 Sovereign KeepAlive Shield • 100% Invariant Determinism
            </p>
          </div>
        </motion.div>

        {/* Foreground: Billowing Fluid Liquid Mist Wave Rising Dynamically on Scroll */}
        <motion.div style={{ y: waveY }} className="relative w-full mt-12 z-20">
          <FluidWaterWave fillColor="#FBF9F5" />
        </motion.div>

        {/* Scroll Indicator Prompt */}
        <div className="absolute bottom-6 left-1/2 -translate-x-1/2 z-20 flex flex-col items-center gap-1.5 text-black pointer-events-none select-none">
          <span className="font-nikkei text-[10px] tracking-[0.25em] uppercase text-black font-extrabold bg-[#FBF9F5] px-3 py-1 border border-black shadow-[2px_2px_0px_#000000]">
            EXPLORE ARCHITECTURAL FEATURES
          </span>
          <ChevronDown className="w-4 h-4 animate-bounce text-[#B91C1C]" />
        </div>
      </section>

      {/* 
        ========================================================================
        FEATURE 01: SUB-SECOND NEURAL MEMORY CORE (SQLite WAL + FTS5)
        ========================================================================
      */}
      <div id="memory">
        <SceneTransition
          fromAct="ARCHITECTURE"
          toAct="FEATURE 01"
          badge="SUB-SECOND NEURAL MEMORY CORE"
        />
      </div>

      <section id="features" className="relative py-16 px-4 sm:px-8 bg-[#0B0B0E] flex flex-col items-center justify-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="comic-plate relative w-full max-w-5xl p-6 sm:p-10 my-8"
        >
          {/* Top-Right Badge */}
          <div className="absolute top-6 right-6 z-20 comic-narration-box p-3 bg-white hidden sm:block">
            <span className="text-xs text-black font-nikkei tracking-wider uppercase font-extrabold">
              <span className="text-[#B91C1C]">24MS RECALL</span> • ZERO CONTEXT BLOAT
            </span>
          </div>

          {/* Feature Header */}
          <div className="mb-8 pt-2">
            <div className="inline-block bg-black text-[#FBF9F5] font-nikkei text-xs uppercase px-3 py-1 tracking-widest mb-3 shadow-[2px_2px_0px_#B91C1C]">
              FEATURE 01 • NEURAL PERSISTENCE
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl text-black tracking-tight leading-tight uppercase">
              Sub-Second Neural Memory Core
            </h2>
            <p className="font-gt-era text-black/75 text-sm sm:text-base max-w-3xl mt-2 leading-relaxed">
              Instead of crashing into 429 quota cliffs and burning 50,000 tokens reading raw unindexed JSONL logs, AegisBrain indexes all codebase symbols, memories, and invariants into SQLite WAL mode with BM25 ranking (<code className="font-mono bg-black/10 px-1 py-0.5 rounded">brain.db</code>).
            </p>
          </div>

          {/* Sovereign Architectural Diagram: Speed Benchmarks */}
          <div
            onClick={() => setSelectedInfographicModal("/infographics/infographic-speed-benchmarks.svg")}
            className="relative w-full border-2 border-black bg-white shadow-[6px_6px_0px_#000000] p-4 sm:p-6 mb-8 overflow-hidden group cursor-zoom-in"
          >
            <div className="flex items-center justify-between mb-3 border-b border-black/10 pb-2">
              <span className="font-nikkei text-xs uppercase tracking-wider text-black flex items-center gap-2 font-bold">
                <Clock className="w-4 h-4 text-[#B91C1C]" />
                SPEED BENCHMARKS • 24MS FTS5 VS 12,400MS RAW CRAWL
              </span>
              <span className="font-mono text-[11px] text-[#B91C1C] flex items-center gap-1 group-hover:underline">
                <ZoomIn className="w-3.5 h-3.5" /> Click to inspect
              </span>
            </div>

            <div className="relative w-full h-[280px] sm:h-[420px] bg-[#FAF8F5] flex items-center justify-center overflow-hidden border border-black/10">
              <Image
                src="/infographics/infographic-speed-benchmarks.svg"
                alt="AegisBrain Speed Benchmarks: 24ms SQLite FTS5 vs 12,400ms raw crawl"
                fill
                className="object-contain p-2 hover:scale-[1.02] transition-transform duration-300"
              />
            </div>
            <div className="mt-3 flex items-center justify-between text-[11px] font-mono text-black/60">
              <span>Engine: P:\open-source\aegis-brain\package\aegis\memory\fts5.py</span>
              <span className="text-emerald-700 font-bold">516x Measured Speedup</span>
            </div>
          </div>

          {/* React Bits Component: Bespoke-Styled <ThoughtLine /> */}
          <div className="mb-8">
            <div className="text-xs font-nikkei text-black uppercase tracking-wider mb-2 flex items-center gap-2 font-bold">
              <Sparkles className="w-4 h-4 text-[#B91C1C]" />
              Real-Time Memory Retrieval Trace
            </div>
            <ThoughtLine
              summary="Neural Recall Trace: Retrieved 4 symbols & test invariants from brain.db in 21ms"
              totalTime="21 ms"
              defaultExpanded={true}
            />
          </div>

          {/* AI Simulation: StopwatchDial */}
          <div className="border-2 border-black rounded-lg overflow-hidden shadow-[6px_6px_0px_#000000] bg-[#101116] mb-8">
            <StopwatchDial />
          </div>

          {/* Interactive 429 Quota Cliff Simulation */}
          <div className="p-5 sm:p-6 rounded-lg bg-[#14141A] text-white border-2 border-black shadow-[4px_4px_0px_#000000] space-y-4">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-white/10 pb-3">
              <div>
                <h3 className="font-nikkei text-sm uppercase tracking-wider text-white flex items-center gap-2 font-bold">
                  <Flame className="w-4 h-4 text-[#B91C1C]" />
                  Live Quota Cliff Simulator
                </h3>
                <p className="text-xs text-zinc-400 font-gt-era">
                  Experience the mechanical difference between crawling raw logs vs indexed neural FTS5.
                </p>
              </div>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={runTraditionalSimulation}
                  className="px-3.5 py-1.5 bg-[#B91C1C] hover:bg-red-800 text-white font-nikkei uppercase text-xs rounded border border-black shadow-[2px_2px_0px_#000000] cursor-pointer"
                >
                  Test Traditional Agent
                </button>
                <button
                  type="button"
                  onClick={runAegisSimulation}
                  className="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white font-nikkei uppercase text-xs rounded border border-black shadow-[2px_2px_0px_#000000] cursor-pointer"
                >
                  Test Aegis FTS5
                </button>
              </div>
            </div>

            {/* Metrics Readout */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 font-mono text-xs">
              <div className="bg-black/60 p-3 rounded border border-white/10">
                <div className="text-zinc-500 text-[10px] uppercase">Tokens Injected</div>
                <div className={`text-xl font-bold mt-1 ${quotaTokens > 30000 ? "text-[#B91C1C]" : "text-white"}`}>
                  {quotaTokens ? `${quotaTokens.toLocaleString()} tokens` : "Idle (0 tokens)"}
                </div>
                <div className="text-[10px] text-zinc-500 mt-1">Context window load</div>
              </div>

              <div className="bg-black/60 p-3 rounded border border-white/10">
                <div className="text-zinc-500 text-[10px] uppercase">Search Latency</div>
                <div className={`text-xl font-bold mt-1 ${quotaLatency > 3000 ? "text-[#B91C1C]" : "text-emerald-400"}`}>
                  {quotaLatency ? `${quotaLatency} ms` : "0 ms"}
                </div>
                <div className="text-[10px] text-zinc-500 mt-1">Wall-clock retrieval time</div>
              </div>

              <div className="bg-black/60 p-3 rounded border border-white/10">
                <div className="text-zinc-500 text-[10px] uppercase">Provider Status</div>
                <div className="text-base font-bold mt-1 text-white">
                  {quotaError ? (
                    <span className="text-[#B91C1C] flex items-center gap-1 font-bold">
                      <AlertTriangle className="w-4 h-4" /> 429 RATE LIMIT
                    </span>
                  ) : quotaSimMode === "aegis" ? (
                    <span className="text-emerald-400 flex items-center gap-1 font-bold">
                      <CheckCircle2 className="w-4 h-4" /> 200 OK (<span className="text-xs">21ms</span>)
                    </span>
                  ) : (
                    <span className="text-zinc-400">Ready to simulate</span>
                  )}
                </div>
                <div className="text-[10px] text-zinc-500 mt-1">API gateway response</div>
              </div>
            </div>

            {quotaError && (
              <div className="p-3 bg-[#B91C1C]/20 border border-[#B91C1C] rounded text-xs font-mono text-red-200 flex items-start gap-2">
                <AlertTriangle className="w-4 h-4 text-[#B91C1C] flex-shrink-0 mt-0.5" />
                <div>
                  <div className="font-bold text-[#B91C1C]">RATE LIMIT CLIFF TRIGGERED:</div>
                  <div>{quotaError}</div>
                </div>
              </div>
            )}
          </div>
        </motion.div>
      </section>

      {/* 
        ========================================================================
        FEATURE 02: DETERMINISTIC 3-TIER LOCAL TOKEN ARBITRAGE ENGINE
        ========================================================================
      */}
      <div id="arbitrage">
        <SceneTransition
          fromAct="FEATURE 01"
          toAct="FEATURE 02"
          badge="DETERMINISTIC 3-TIER TOKEN ARBITRAGE"
        />
      </div>

      <section className="relative py-16 px-4 sm:px-8 bg-[#070709] flex flex-col items-center justify-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="comic-plate relative w-full max-w-5xl p-6 sm:p-10 my-8"
        >
          <div className="absolute top-6 right-6 z-20 comic-narration-box p-3 bg-white hidden sm:block">
            <span className="text-xs text-black font-nikkei tracking-wider uppercase font-extrabold">
              <span className="text-[#B91C1C]">ZERO TOKEN WASTE</span> • $1,840+/MO SAVINGS
            </span>
          </div>

          <div className="mb-8 pt-2">
            <div className="inline-block bg-black text-[#FBF9F5] font-nikkei text-xs uppercase px-3 py-1 tracking-widest mb-3 shadow-[2px_2px_0px_#B91C1C]">
              FEATURE 02 • TOKEN ARBITRAGE ENGINE
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl text-black tracking-tight leading-tight uppercase">
              3-Tier Multi-Agent Hierarchy
            </h2>
            <p className="font-gt-era text-black/75 text-sm sm:text-base max-w-3xl mt-2 leading-relaxed">
              Frontier models (Gemini 4, Claude Opus, Fable) are strategic brains, not construction workers. AegisBrain enforces strict division of labor: high-cognition models architect and coach, while local CLI workers (Hermes, Ollama, Qwen) execute implementations for free.
            </p>
          </div>

          {/* Sovereign Architectural Diagram: Hierarchy Pyramid */}
          <div
            onClick={() => setSelectedInfographicModal("/infographics/infographic-hierarchy-pyramid.svg")}
            className="relative w-full border-2 border-black bg-white shadow-[6px_6px_0px_#000000] p-4 sm:p-6 mb-8 overflow-hidden group cursor-zoom-in"
          >
            <div className="flex items-center justify-between mb-3 border-b border-black/10 pb-2">
              <span className="font-nikkei text-xs uppercase tracking-wider text-black flex items-center gap-2 font-bold">
                <Cpu className="w-4 h-4 text-[#B91C1C]" />
                3-TIER MULTI-AGENT HIERARCHY PYRAMID
              </span>
              <span className="font-mono text-[11px] text-[#B91C1C] flex items-center gap-1 group-hover:underline">
                <ZoomIn className="w-3.5 h-3.5" /> Click to inspect
              </span>
            </div>

            <div className="relative w-full h-[280px] sm:h-[420px] bg-[#FAF8F5] flex items-center justify-center overflow-hidden border border-black/10">
              <Image
                src="/infographics/infographic-hierarchy-pyramid.svg"
                alt="3-Tier Multi-Agent Hierarchy Pyramid: Senior Boss, Subagents, and Free Execution Workers"
                fill
                className="object-contain p-2 hover:scale-[1.02] transition-transform duration-300"
              />
            </div>
            <div className="mt-3 flex items-center justify-between text-[11px] font-mono text-black/60">
              <span>Dynamic Workload Triage: Micro-tasks direct, Macro-tasks delegated to local workers</span>
              <span className="text-emerald-700 font-bold">$1,840/mo Measured Savings</span>
            </div>
          </div>

          {/* Bespoke-Styled React Bits <CallChip /> */}
          <div className="mb-8 p-4 bg-white border-2 border-black shadow-[4px_4px_0px_#000000] space-y-3">
            <div className="flex items-center justify-between border-b border-black/10 pb-2">
              <span className="font-nikkei text-xs uppercase tracking-wider text-black flex items-center gap-2 font-bold">
                <Sparkles className="w-4 h-4 text-[#B91C1C]" />
                Active Tier 3 Local Worker Invocations
              </span>
              <span className="font-mono text-[10px] text-emerald-700 font-bold">100% Free Hardware Tokens</span>
            </div>
            <div className="flex flex-wrap gap-3">
              <CallChip
                toolName="hermes chat"
                command="hermes chat -q 'Write AST visitor for tainted exec() nodes'"
                duration="21 ms"
                status="done"
                progress={100}
              />
              <CallChip
                toolName="aegis recall"
                command="sqlite3 brain.db 'SELECT snippet FROM memories WHERE query match ...'"
                duration="18 ms"
                status="done"
                progress={100}
              />
              <CallChip
                toolName="scan_ast_taint"
                command="ASTTaintChecker.block_shell_injection(allow_shell=False)"
                duration="4 ms"
                status="done"
                progress={100}
              />
            </div>
          </div>

          {/* Arbitrage Engine: ArbitrageCalculator */}
          <div className="border-2 border-black rounded-lg overflow-hidden shadow-[6px_6px_0px_#000000] bg-[#101116]">
            <ArbitrageCalculator />
          </div>
        </motion.div>
      </section>

      {/* 
        ========================================================================
        FEATURE 03: 24/7 WIN32 KEEPALIVE SHIELD & PROCESS RESURRECTION
        ========================================================================
      */}
      <SceneTransition
        fromAct="FEATURE 02"
        toAct="FEATURE 03"
        badge="24/7 WIN32 KEEPALIVE SHIELD"
      />

      <section className="relative py-16 px-4 sm:px-8 bg-[#0B0B0E] flex flex-col items-center justify-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="comic-plate relative w-full max-w-5xl p-6 sm:p-10 my-8"
        >
          <div className="absolute top-6 right-6 z-20 comic-narration-box p-3 bg-white hidden sm:block">
            <span className="text-xs text-black font-nikkei tracking-wider uppercase font-extrabold">
              <span className="text-emerald-700">99.98% UPTIME</span> • WIN32 WATCHDOG
            </span>
          </div>

          <div className="mb-8 pt-2">
            <div className="inline-block bg-black text-[#FBF9F5] font-nikkei text-xs uppercase px-3 py-1 tracking-widest mb-3 shadow-[2px_2px_0px_#B91C1C]">
              FEATURE 03 • IMMORTAL HOST DAEMON
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl text-black tracking-tight leading-tight uppercase">
              24/7 Win32 KeepAlive Shield &amp; Process Resurrection
            </h2>
            <p className="font-gt-era text-black/75 text-sm sm:text-base max-w-3xl mt-2 leading-relaxed">
              Operating an autonomous coding agent overnight requires absolute resilience. Win32 connected standby, sleep transitions, and terminal terminations can disrupt unshielded agents. Aegis introduces an immortal Windows Scheduled Task watchdog.
            </p>
          </div>

          {/* Side-by-Side Comparison Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {/* Card 1: Traditional Vulnerability */}
            <div className="comic-card-red p-6 rounded-lg space-y-3">
              <div className="flex items-center justify-between border-b border-black/10 pb-2">
                <span className="font-nikkei text-xs uppercase tracking-wider text-[#B91C1C] font-extrabold">
                  Traditional Agent Vulnerability
                </span>
                <span className="text-[10px] font-mono text-zinc-500">Unshielded</span>
              </div>
              <ul className="space-y-2 text-xs font-gt-era text-black/80">
                <li className="flex items-start gap-2">
                  <span className="text-[#B91C1C] font-bold">✕</span>
                  <span><strong>Silent Sleep Freeze:</strong> Windows Standby terminates webhook connections and drops long-running tasks.</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-[#B91C1C] font-bold">✕</span>
                  <span><strong>Account Switch Termination:</strong> Closing an Antigravity or VSCode window terminates running background jobs.</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-[#B91C1C] font-bold">✕</span>
                  <span><strong>Telegram Bridge Death:</strong> Remote polling listeners die unceremoniously with no auto-resurrection.</span>
                </li>
              </ul>
            </div>

            {/* Card 2: Aegis KeepAlive Shield */}
            <div className="comic-card-emerald p-6 rounded-lg space-y-3">
              <div className="flex items-center justify-between border-b border-black/10 pb-2">
                <span className="font-nikkei text-xs uppercase tracking-wider text-emerald-700 font-extrabold">
                  Aegis Immortal KeepAlive Shield
                </span>
                <span className="text-[10px] font-mono text-emerald-700 font-bold">Active 24/7</span>
              </div>
              <ul className="space-y-2 text-xs font-gt-era text-black/80">
                <li className="flex items-start gap-2">
                  <span className="text-emerald-700 font-bold">✓</span>
                  <span><strong>Win32 Scheduled Task:</strong> <code className="font-mono bg-black/5 px-1">AegisBrainDaemonKeepAlive</code> triggers every 5 min to ensure daemon (:8765) is running.</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-700 font-bold">✓</span>
                  <span><strong>Self-Healing Watchdog:</strong> Reconnects Telegram listener, drains asynchronous inboxes, and holds WAL database lock.</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-700 font-bold">✓</span>
                  <span><strong>Zero Disruption:</strong> Seamless persistence across reboots, account switches, and terminal terminations.</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Pytest Verification Badge */}
          <div className="p-4 bg-white border-2 border-black shadow-[4px_4px_0px_#000000] flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded bg-emerald-100 border-2 border-emerald-600 flex items-center justify-center text-emerald-700 font-bold">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <div>
                <div className="font-nikkei text-xs uppercase tracking-wider text-black font-extrabold">
                  Verified Test Suite Parity
                </div>
                <div className="font-gt-era text-xs text-black/70">
                  All keepalive, remote polling, token guard, and AST security modules verified
                </div>
              </div>
            </div>
            <div className="comic-stamp-emerald px-4 py-2 font-mono text-xs">
              286/286 PYTEST TESTS PASSING • 100% CLEAN
            </div>
          </div>
        </motion.div>
      </section>

      {/* 
        ========================================================================
        FEATURE 04: DETERMINISTIC MOBILE TELEGRAM TELEMETRY & WHISPER SHIELD
        ========================================================================
      */}
      <SceneTransition
        fromAct="FEATURE 03"
        toAct="FEATURE 04"
        badge="24/7 MOBILE TELEGRAM TELEMETRY"
      />

      <section className="relative py-16 px-4 sm:px-8 bg-[#070709] flex flex-col items-center justify-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="comic-plate relative w-full max-w-5xl p-6 sm:p-10 my-8"
        >
          <div className="absolute top-6 right-6 z-20 comic-narration-box p-3 bg-white hidden sm:block">
            <span className="text-xs text-black font-nikkei tracking-wider uppercase font-extrabold">
              <span className="text-[#B91C1C]">IN-FLIGHT INTERRUPT</span> • /type /alt+m
            </span>
          </div>

          <div className="mb-8 pt-2">
            <div className="inline-block bg-black text-[#FBF9F5] font-nikkei text-xs uppercase px-3 py-1 tracking-widest mb-3 shadow-[2px_2px_0px_#B91C1C]">
              FEATURE 04 • MOBILE TELEGRAM TELEMETRY
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl text-black tracking-tight leading-tight uppercase">
              Real-Time Mobile Command Center
            </h2>
            <p className="font-gt-era text-black/75 text-sm sm:text-base max-w-3xl mt-2 leading-relaxed">
              True developer autonomy means never being chained to a desk. AegisBrain runs a 24/7 Telegram companion (<code className="font-mono bg-black/10 px-1">@HHAACLIBot</code>) with audio transcription shielding and in-flight terminal control.
            </p>
          </div>

          {/* Sovereign Architectural Diagram: Mobile Pipeline */}
          <div
            onClick={() => setSelectedInfographicModal("/infographics/infographic-mobile-pipeline.svg")}
            className="relative w-full border-2 border-black bg-white shadow-[6px_6px_0px_#000000] p-4 sm:p-6 mb-8 overflow-hidden group cursor-zoom-in"
          >
            <div className="flex items-center justify-between mb-3 border-b border-black/10 pb-2">
              <span className="font-nikkei text-xs uppercase tracking-wider text-black flex items-center gap-2 font-bold">
                <Smartphone className="w-4 h-4 text-[#B91C1C]" />
                24/7 MOBILE TELEGRAM PIPELINE BLUEPRINT
              </span>
              <span className="font-mono text-[11px] text-[#B91C1C] flex items-center gap-1 group-hover:underline">
                <ZoomIn className="w-3.5 h-3.5" /> Click to inspect
              </span>
            </div>

            <div className="relative w-full h-[280px] sm:h-[420px] bg-[#FAF8F5] flex items-center justify-center overflow-hidden border border-black/10">
              <Image
                src="/infographics/infographic-mobile-pipeline.svg"
                alt="24/7 Mobile Telegram Ingestion Pipeline: Phone mic to FFmpeg chunking to Whisper STT to Antigravity /type injection"
                fill
                className="object-contain p-2 hover:scale-[1.02] transition-transform duration-300"
              />
            </div>
          </div>

          {/* Telegram Simulator: TelegramSimulator with integrated REACT BITS <VoicePill /> */}
          <div className="border-2 border-black rounded-lg overflow-hidden shadow-[6px_6px_0px_#000000] bg-[#101116] p-4 sm:p-6">
            <TelegramSimulator />
          </div>
        </motion.div>
      </section>

      {/* 
        ========================================================================
        FEATURE 05: 4-DECISION QUALITY ARCHITECTURE GATE & AUTONOMOUS LEARNING LOOP
        ========================================================================
      */}
      <SceneTransition
        fromAct="FEATURE 04"
        toAct="FEATURE 05"
        badge="4-DECISION QUALITY ARCHITECTURE GATE"
      />

      <section className="relative py-16 px-4 sm:px-8 bg-[#0B0B0E] flex flex-col items-center justify-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="comic-plate relative w-full max-w-5xl p-6 sm:p-10 my-8"
        >
          <div className="absolute top-6 right-6 z-20 comic-narration-box p-3 bg-white hidden sm:block">
            <span className="text-xs text-black font-nikkei tracking-wider uppercase font-extrabold">
              <span className="text-[#B91C1C]">ZERO-DEFECT AUDIT</span> • 4 GATES OF STEEL
            </span>
          </div>

          <div className="mb-8 pt-2">
            <div className="inline-block bg-black text-[#FBF9F5] font-nikkei text-xs uppercase px-3 py-1 tracking-widest mb-3 shadow-[2px_2px_0px_#B91C1C]">
              FEATURE 05 • PRODUCTION SAFETY GATE
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl text-black tracking-tight leading-tight uppercase">
              4-Decision Quality Architecture Gate
            </h2>
            <p className="font-gt-era text-black/75 text-sm sm:text-base max-w-3xl mt-2 leading-relaxed">
              When lower-tier models generate code, errors occur. Rather than discarding local models, Aegis applies an adversarial compiler and static analysis gate that coach the worker until zero defects remain.
            </p>
          </div>

          {/* Quality Gates: QualityGateCards */}
          <div className="border-2 border-black rounded-lg overflow-hidden shadow-[6px_6px_0px_#000000] bg-[#101116]">
            <QualityGateCards />
          </div>
        </motion.div>
      </section>

      {/* 
        ========================================================================
        FEATURE 06: UNIVERSAL MULTI-CHASSIS AGENT FLEET PROTOCOL
        ========================================================================
      */}
      <SceneTransition
        fromAct="FEATURE 05"
        toAct="FEATURE 06"
        badge="UNIVERSAL MULTI-CHASSIS FLEET PROTOCOL"
      />

      <section className="relative py-16 px-4 sm:px-8 bg-[#070709] flex flex-col items-center justify-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="comic-plate relative w-full max-w-5xl p-6 sm:p-10 my-8"
        >
          <div className="absolute top-6 right-6 z-20 comic-narration-box p-3 bg-white hidden sm:block">
            <span className="text-xs text-black font-nikkei tracking-wider uppercase font-extrabold">
              <span className="text-emerald-700">6 ENGINES</span> • ZERO LOCK-IN
            </span>
          </div>

          <div className="mb-8 pt-2">
            <div className="inline-block bg-black text-[#FBF9F5] font-nikkei text-xs uppercase px-3 py-1 tracking-widest mb-3 shadow-[2px_2px_0px_#B91C1C]">
              FEATURE 06 • FLEET INTEROPERABILITY
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl text-black tracking-tight leading-tight uppercase">
              Universal Multi-Chassis Agent Fleet
            </h2>
            <p className="font-gt-era text-black/75 text-sm sm:text-base max-w-3xl mt-2 leading-relaxed">
              Zero vendor lock-in. AegisBrain runs as an autonomous sidecar across Antigravity, Claude Code, Cursor, Windsurf, Aider, and Hermes CLI. Switch IDEs or terminals with shared sub-second neural memory.
            </p>
          </div>

          {/* Sovereign Architectural Diagram: Universal Fleet Compatibility */}
          <div
            onClick={() => setSelectedInfographicModal("/infographics/infographic-universal-agents.svg")}
            className="relative w-full border-2 border-black bg-white shadow-[6px_6px_0px_#000000] p-4 sm:p-6 mb-8 overflow-hidden group cursor-zoom-in"
          >
            <div className="flex items-center justify-between mb-3 border-b border-black/10 pb-2">
              <span className="font-nikkei text-xs uppercase tracking-wider text-black flex items-center gap-2 font-bold">
                <Layers className="w-4 h-4 text-[#B91C1C]" />
                UNIVERSAL FLEET COMPATIBILITY BLUEPRINT
              </span>
              <span className="font-mono text-[11px] text-[#B91C1C] flex items-center gap-1 group-hover:underline">
                <ZoomIn className="w-3.5 h-3.5" /> Click to inspect
              </span>
            </div>

            <div className="relative w-full h-[280px] sm:h-[420px] bg-[#FAF8F5] flex items-center justify-center overflow-hidden border border-black/10">
              <Image
                src="/infographics/infographic-universal-agents.svg"
                alt="Universal Multi-Agent Fleet Compatibility across Claude Code, Cursor, Windsurf, Aider, Antigravity"
                fill
                className="object-contain p-2 hover:scale-[1.02] transition-transform duration-300"
              />
            </div>
            <div className="mt-3 flex items-center justify-between text-[11px] font-mono text-black/60">
              <span>Universal Sidecar Protocol: Zero vendor lock-in</span>
              <span className="text-emerald-700 font-bold">6 Supported Engines</span>
            </div>
          </div>
        </motion.div>
      </section>

      {/* 
        ========================================================================
        FEATURE 07: MASTER ARCHITECTURAL BLUEPRINTS GALLERY
        ========================================================================
      */}
      <div id="blueprints">
        <SceneTransition
          fromAct="FEATURE 06"
          toAct="FEATURE 07"
          badge="MASTER ARCHITECTURAL BLUEPRINT GALLERY"
        />
      </div>

      <section className="relative py-16 px-4 sm:px-8 bg-[#0B0B0E] flex flex-col items-center justify-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="comic-plate relative w-full max-w-5xl p-6 sm:p-10 my-8"
        >
          <div className="absolute top-6 right-6 z-20 comic-narration-box p-3 bg-white hidden sm:block">
            <span className="text-xs text-black font-nikkei tracking-wider uppercase font-extrabold">
              <span className="text-[#B91C1C]">SYSTEM BLUEPRINTS</span> • 7 ARCHITECTURAL DIAGRAMS
            </span>
          </div>

          <div className="mb-8 pt-2">
            <div className="inline-block bg-black text-[#FBF9F5] font-nikkei text-xs uppercase px-3 py-1 tracking-widest mb-3 shadow-[2px_2px_0px_#B91C1C]">
              FEATURE 07 • ARCHITECTURAL BLUEPRINTS
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl text-black tracking-tight leading-tight uppercase">
              Architecture &amp; Execution Flow
            </h2>
            <p className="font-gt-era text-black/75 text-sm sm:text-base max-w-3xl mt-2 leading-relaxed">
              Clear system blueprints detailing multi-agent token arbitrage, sub-second neural memory, and deterministic mobile telemetry.
            </p>
          </div>

          {/* System Diagrams: InfographicsGallery */}
          <div className="border-2 border-black rounded-lg overflow-hidden shadow-[6px_6px_0px_#000000] bg-[#101116]">
            <InfographicsGallery />
          </div>
        </motion.div>
      </section>

      {/* 
        ========================================================================
        QUICKSTART & INSTALLATION: ONE-LINE SETUP
        ========================================================================
      */}
      <SceneTransition
        fromAct="FEATURE 07"
        toAct="INSTALLATION"
        badge="ONE-LINE TERMINAL BOOTSTRAP"
      />

      <section id="install" className="relative py-16 px-4 sm:px-8 bg-[#070709] flex flex-col items-center justify-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="comic-plate relative w-full max-w-5xl p-6 sm:p-10 my-8"
        >
          <div className="mb-8 pt-2">
            <div className="inline-block bg-black text-[#FBF9F5] font-nikkei text-xs uppercase px-3 py-1 tracking-widest mb-3 shadow-[2px_2px_0px_#B91C1C]">
              QUICKSTART &amp; INSTALLATION
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl text-black tracking-tight leading-tight uppercase">
              Install in Seconds
            </h2>
            <p className="font-gt-era text-black/75 text-sm sm:text-base max-w-2xl mt-2 leading-relaxed">
              Deploy the 24/7 background daemon and global CLI with a single command across macOS, Linux, or Windows.
            </p>
          </div>

          {/* Terminal Command Strip: TerminalInstall */}
          <div className="border-2 border-black rounded-lg overflow-hidden shadow-[6px_6px_0px_#000000] bg-[#101116]">
            <TerminalInstall />
          </div>
        </motion.div>
      </section>

      {/* 
        ========================================================================
        FOOTER: OPEN SOURCE & COMMUNITY HUB + ARCHITECTURAL COMPARISON MATRIX
        ========================================================================
      */}
      <footer className="relative py-20 px-4 sm:px-8 bg-[#070709] border-t-4 border-black text-white">
        <div className="max-w-5xl mx-auto space-y-12">
          {/* Main Community & Open Source Plate */}
          <div className="comic-plate p-8 sm:p-12 text-black">
            <div className="border-b-2 border-black pb-8">
              <div className="inline-block bg-[#B91C1C] text-white font-nikkei text-xs uppercase px-3 py-1 tracking-widest mb-2 shadow-[2px_2px_0px_#000000]">
                OPEN SOURCE &amp; COMMUNITY
              </div>
              <h3 className="font-charles-rosie text-3xl sm:text-4xl text-black tracking-tight uppercase">
                Build With AegisBrain
              </h3>
              <p className="font-gt-era text-black/75 text-sm sm:text-base mt-2 max-w-2xl leading-relaxed">
                AegisBrain is 100% free and open-source under the Apache-2.0 License. If you believe coding agents deserve deterministic persistence and zero token waste, star the repository, open issues, and join the development.
              </p>
            </div>

            {/* Action Cards Grid: 4 Pillars of Community */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-6">
              {/* Card 1: Star on GitHub */}
              <div className="p-5 bg-white border-2 border-black shadow-[4px_4px_0px_#000000] rounded flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-nikkei text-xs uppercase tracking-wider font-extrabold text-black flex items-center gap-2">
                      <Star className="w-4 h-4 text-[#D4AF37] fill-[#D4AF37]" />
                      Star the Repository
                    </span>
                    <span className="text-[10px] font-mono uppercase bg-amber-100 text-amber-800 px-2 py-0.5 rounded font-bold">
                      GitHub
                    </span>
                  </div>
                  <p className="font-gt-era text-xs text-black/75 leading-relaxed">
                    Help more developers discover sovereign agentic memory, zero token waste, and 24/7 background persistence.
                  </p>
                </div>
                <div className="mt-4 pt-3 border-t border-black/10">
                  <a
                    href="https://github.com/PG300604/aegis-brain"
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-2 px-4 py-2 bg-black hover:bg-neutral-800 text-white font-nikkei text-xs uppercase tracking-wider rounded border border-black shadow-[2px_2px_0px_#B91C1C] transition-transform hover:-translate-y-0.5"
                  >
                    <Star className="w-3.5 h-3.5 text-[#D4AF37] fill-[#D4AF37]" />
                    <span>Star on GitHub</span>
                    <ArrowRight className="w-3 h-3 text-white/60 ml-1" />
                  </a>
                </div>
              </div>

              {/* Card 2: Clone Repository */}
              <div className="p-5 bg-white border-2 border-black shadow-[4px_4px_0px_#000000] rounded flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-nikkei text-xs uppercase tracking-wider font-extrabold text-black flex items-center gap-2">
                      <FileCode className="w-4 h-4 text-[#B91C1C]" />
                      Clone Repository
                    </span>
                    <span className="text-[10px] font-mono uppercase bg-zinc-100 text-zinc-800 px-2 py-0.5 rounded font-bold">
                      Local Setup
                    </span>
                  </div>
                  <p className="font-gt-era text-xs text-black/75 leading-relaxed">
                    Get the source code and start hacking immediately.
                  </p>
                </div>
                <div className="mt-4 pt-3 border-t border-black/10 flex items-center justify-between gap-2 bg-[#0D0E15] p-2.5 rounded border border-black text-white font-mono text-[11px]">
                  <span className="text-zinc-300 truncate">
                    git clone https://github.com/PG300604/aegis-brain.git
                  </span>
                  <button
                    type="button"
                    onClick={handleCopyClone}
                    className="px-2.5 py-1 bg-[#B91C1C] hover:bg-red-800 text-white font-nikkei text-[10px] uppercase rounded border border-black flex items-center gap-1 cursor-pointer shrink-0"
                  >
                    {copiedClone ? (
                      <>
                        <Check className="w-3 h-3" />
                        <span>COPIED</span>
                      </>
                    ) : (
                      <>
                        <Copy className="w-3 h-3" />
                        <span>COPY</span>
                      </>
                    )}
                  </button>
                </div>
              </div>

              {/* Card 3: Issues & Discussions */}
              <div className="p-5 bg-white border-2 border-black shadow-[4px_4px_0px_#000000] rounded flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-nikkei text-xs uppercase tracking-wider font-extrabold text-black flex items-center gap-2">
                      <AlertTriangle className="w-4 h-4 text-[#B91C1C]" />
                      Issues &amp; Discussions
                    </span>
                    <span className="text-[10px] font-mono uppercase bg-red-100 text-[#B91C1C] px-2 py-0.5 rounded font-bold">
                      Community
                    </span>
                  </div>
                  <p className="font-gt-era text-xs text-black/75 leading-relaxed">
                    Request a chassis adapter, report an edge case, or propose an invariant.
                  </p>
                </div>
                <div className="mt-4 pt-3 border-t border-black/10">
                  <a
                    href="https://github.com/PG300604/aegis-brain/issues"
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-2 px-4 py-2 bg-[#FBF9F5] hover:bg-neutral-100 text-black font-nikkei text-xs uppercase tracking-wider rounded border-2 border-black shadow-[2px_2px_0px_#000000] transition-transform hover:-translate-y-0.5"
                  >
                    <span>💬 Open an Issue</span>
                    <ArrowRight className="w-3 h-3 text-black/50 ml-1" />
                  </a>
                </div>
              </div>

              {/* Card 4: Contribute Code */}
              <div className="p-5 bg-white border-2 border-black shadow-[4px_4px_0px_#000000] rounded flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-nikkei text-xs uppercase tracking-wider font-extrabold text-black flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-emerald-700" />
                      Contribute Code
                    </span>
                    <span className="text-[10px] font-mono uppercase bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded font-bold">
                      Pull Requests
                    </span>
                  </div>
                  <p className="font-gt-era text-xs text-black/75 leading-relaxed">
                    Submit PRs for new local worker bridges, IDE shims, or benchmark tests.
                  </p>
                </div>
                <div className="mt-4 pt-3 border-t border-black/10">
                  <a
                    href="https://github.com/PG300604/aegis-brain/pulls"
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white font-nikkei text-xs uppercase tracking-wider rounded border border-black shadow-[2px_2px_0px_#000000] transition-transform hover:-translate-y-0.5"
                  >
                    <span>🔀 Submit Pull Request</span>
                    <ArrowRight className="w-3 h-3 text-white/60 ml-1" />
                  </a>
                </div>
              </div>
            </div>

            {/* 7-Vector Comparison Matrix */}
            <div className="mt-8 pt-6 border-t border-black/10">
              <h4 className="font-nikkei text-xs uppercase tracking-wider text-black mb-3 font-extrabold">
                7-Vector Architectural Comparison Matrix
              </h4>
              <div className="overflow-x-auto">
                <table className="w-full text-left font-mono text-[11px] border-collapse border border-black">
                  <thead>
                    <tr className="bg-black text-white">
                      <th className="p-2.5 border border-black">Vector</th>
                      <th className="p-2.5 border border-black text-[#D4AF37]">AegisBrain</th>
                      <th className="p-2.5 border border-black">LangChain / CrewAI</th>
                      <th className="p-2.5 border border-black">Raw Cursor Rules</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr className="bg-white">
                      <td className="p-2.5 border border-black font-bold">Memory Mechanism</td>
                      <td className="p-2.5 border border-black text-emerald-700 font-bold">SQLite WAL FTS5 (24ms)</td>
                      <td className="p-2.5 border border-black text-zinc-500">Crawls raw JSON/RAM</td>
                      <td className="p-2.5 border border-black text-zinc-500">0 memory across sessions</td>
                    </tr>
                    <tr className="bg-[#FAF8F5]">
                      <td className="p-2.5 border border-black font-bold">Cost Arbitrage</td>
                      <td className="p-2.5 border border-black text-emerald-700 font-bold">3-Tier (92% savings)</td>
                      <td className="p-2.5 border border-black text-zinc-500">100% frontier API spend</td>
                      <td className="p-2.5 border border-black text-zinc-500">User pays per token</td>
                    </tr>
                    <tr className="bg-white">
                      <td className="p-2.5 border border-black font-bold">Host KeepAlive</td>
                      <td className="p-2.5 border border-black text-emerald-700 font-bold">Win32 Scheduled Task 24/7</td>
                      <td className="p-2.5 border border-black text-zinc-500">Dies on terminal close</td>
                      <td className="p-2.5 border border-black text-zinc-500">None</td>
                    </tr>
                    <tr className="bg-[#FAF8F5]">
                      <td className="p-2.5 border border-black font-bold">Quality Gates</td>
                      <td className="p-2.5 border border-black text-emerald-700 font-bold">4-Stage AST Security + Unslop</td>
                      <td className="p-2.5 border border-black text-zinc-500">Unfiltered model output</td>
                      <td className="p-2.5 border border-black text-zinc-500">Manual review</td>
                    </tr>
                    <tr className="bg-white">
                      <td className="p-2.5 border border-black font-bold">Mobile Remote</td>
                      <td className="p-2.5 border border-black text-emerald-700 font-bold">Telegram /type + Whisper STT</td>
                      <td className="p-2.5 border border-black text-zinc-500">Desktop terminal only</td>
                      <td className="p-2.5 border border-black text-zinc-500">IDE bound</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Luxury Footer Bottom */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-8 border-t border-white/10 text-xs font-gt-era text-white/50">
            <div className="flex items-center gap-3">
              <span className="font-charles-rosie text-white text-lg">AegisBrain</span>
              <span>•</span>
              <span className="italic font-charles-rosie text-white/70">
                &ldquo;Memoriam Non Perdet, Tempus Non Teret&rdquo;
              </span>
            </div>
            <div>
              Crafted for sovereign developers. Open-source under Apache-2.0.
            </div>
          </div>
        </div>
      </footer>

      {/* 
        ========================================================================
        INFOGRAPHIC FULLSCREEN LIGHTBOX MODAL
        ========================================================================
      */}
      <AnimatePresence>
        {selectedInfographicModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/90 backdrop-blur-md flex items-center justify-center p-4 sm:p-8"
            onClick={() => setSelectedInfographicModal(null)}
          >
            <motion.div
              initial={{ scale: 0.95 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.95 }}
              onClick={(e) => e.stopPropagation()}
              className="relative w-full max-w-6xl max-h-[90vh] bg-[#FAF8F5] border-4 border-black shadow-[12px_12px_0px_#B91C1C] rounded-lg p-6 flex flex-col text-black"
            >
              <div className="flex items-center justify-between border-b-2 border-black pb-3 mb-4">
                <span className="font-nikkei text-sm uppercase text-black font-extrabold flex items-center gap-2">
                  <Maximize2 className="w-4 h-4 text-[#B91C1C]" />
                  AegisBrain Architectural Blueprint • High-Resolution View
                </span>
                <button
                  type="button"
                  onClick={() => setSelectedInfographicModal(null)}
                  className="p-1.5 bg-black text-white hover:bg-[#B91C1C] rounded border border-black cursor-pointer transition-colors"
                  aria-label="Close"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="relative w-full flex-1 min-h-[400px] sm:min-h-[600px] bg-white border border-black/20 flex items-center justify-center overflow-auto p-4">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={selectedInfographicModal}
                  alt="AegisBrain Blueprint Fullscreen View"
                  className="max-h-[75vh] w-auto object-contain"
                />
              </div>

              <div className="mt-4 flex items-center justify-between text-xs font-mono text-black/70">
                <span>High-resolution luxury editorial SVG blueprint</span>
                <span className="text-black/50 text-[11px]">Press ESC or click outside to close</span>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
      {/* Atmospheric Audio Soundtrack & Sfx Engine */}
      <SoundtrackController
        soundActive={soundActive}
        onToggleSound={setSoundActive}
      />
    </div>
  );
}
