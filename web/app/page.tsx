"use client";

import React, { useState, useEffect, useMemo } from "react";
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
import { motion, AnimatePresence } from "motion/react";
import { PromptBar } from "@/components/react-bits/PromptBar";
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

export default function Home() {
  const [scrollProgress, setScrollProgress] = useState(0);
  const [soundActive, setSoundActive] = useState(false);
  const [copiedSha, setCopiedSha] = useState<string | null>(null);
  const [selectedInfographicModal, setSelectedInfographicModal] = useState<string | null>(null);

  // Chapter 1: 429 Quota Cliff interactive cockpit state
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

  // Web Audio atmospheric sound generation
  useEffect(() => {
    if (!soundActive) return;
    try {
      const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      const ctx = new AudioCtx();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = "sine";
      osc.frequency.setValueAtTime(144, ctx.currentTime); // Deep warm subtle harmonic drone
      gain.gain.setValueAtTime(0.015, ctx.currentTime);

      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();

      return () => {
        try {
          osc.stop();
          ctx.close();
        } catch {
          // Ignore
        }
      };
    } catch {
      // AudioContext not supported
    }
  }, [soundActive]);

  const handleCopySha = (sha: string) => {
    navigator.clipboard.writeText(sha);
    setCopiedSha(sha);
    setTimeout(() => setCopiedSha(null), 2500);
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
        {/* Left: Circular Seal Logo */}
        <div className="pointer-events-auto flex items-center gap-3">
          <a href="#" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-full border-2 border-black flex items-center justify-center bg-[#FBF9F5] shadow-[3px_3px_0px_#000000] text-black transition-transform group-hover:scale-105">
              <svg
                viewBox="0 0 40 40"
                className="w-6 h-6 text-black fill-none stroke-current"
                strokeWidth="1.8"
              >
                <circle cx="20" cy="20" r="17" strokeDasharray="2 2" />
                <polygon points="20,8 32,28 8,28" />
                <circle cx="20" cy="21" r="3" fill="#B91C1C" />
              </svg>
            </div>
            <div className="flex flex-col">
              <span className="font-charles-rosie text-xl text-white tracking-wider leading-none">
                AegisBrain
              </span>
              <span className="font-gt-era text-[9px] uppercase tracking-[0.25em] text-white/50 leading-tight">
                Chassis • Neural Memory
              </span>
            </div>
          </a>
        </div>

        {/* Right: Sharp Minimal Badge & Audio Toggle */}
        <div className="pointer-events-auto flex items-center gap-4">
          <nav className="hidden sm:flex items-center bg-[#FBF9F5] border-2 border-black shadow-[4px_4px_0px_#000000] text-black font-nikkei text-xs uppercase px-4 py-2 tracking-widest gap-4">
            <a href="#narrative" className="hover:text-[#B91C1C] transition-colors">
              The Story
            </a>
            <span className="text-black/30">|</span>
            <a href="#benchmarks" className="hover:text-[#B91C1C] transition-colors">
              Benchmarks
            </a>
            <span className="text-black/30">|</span>
            <a href="#hierarchy" className="hover:text-[#B91C1C] transition-colors">
              Token Arbitrage
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
            onClick={() => setSoundActive(!soundActive)}
            className="w-10 h-10 bg-[#FBF9F5] border-2 border-black shadow-[4px_4px_0px_#000000] flex items-center justify-center text-black hover:bg-neutral-100 transition-colors cursor-pointer"
            title={soundActive ? "Mute Ambient Sound" : "Enable Sound Atmosphere"}
            aria-label="Toggle sound atmosphere"
          >
            {soundActive ? (
              <div className="flex items-end gap-[2px] h-4">
                <span className="w-[3px] bg-black sound-bar-1" />
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
        ACT I: THE MONUMENTAL TITLE SPREAD (Santioni Spirits Hero)
        ========================================================================
      */}
      <section
        id="experience"
        className="relative min-h-screen w-full flex flex-col items-center justify-between pt-32 pb-0 px-4 bg-[#070709] overflow-hidden"
      >
        {/* Subtle Horizontal Dry-Brush Chalk Streaks */}
        <div
          className="absolute inset-0 pointer-events-none opacity-20"
          style={{
            backgroundImage: `repeating-linear-gradient(
              0deg,
              transparent,
              transparent 3px,
              rgba(255, 255, 255, 0.08) 3px,
              rgba(255, 255, 255, 0.08) 4px
            )`,
          }}
        />

        {/* Center: Monumental Headline (Charles Rosie Renaissance Typeface) */}
        <div className="relative z-10 text-center flex flex-col items-center max-w-5xl mx-auto my-auto select-none pt-8">
          <p className="font-charles-rosie text-white/70 text-lg sm:text-2xl tracking-[0.35em] uppercase mb-2">
            The
          </p>

          <h1 className="font-charles-rosie text-white text-6xl sm:text-8xl md:text-9xl lg:text-[10.5rem] leading-[0.88] tracking-tight uppercase drop-shadow-[0_10px_30px_rgba(0,0,0,0.9)]">
            Aeg<span className="text-[#B91C1C]">i</span>s
          </h1>

          <h2 className="font-charles-rosie text-white text-3xl sm:text-5xl md:text-6xl lg:text-7xl leading-tight tracking-[0.16em] uppercase mt-2">
            Experience
          </h2>

          <div className="mt-6 max-w-2xl mx-auto px-4">
            <p className="font-gt-era text-white/70 text-xs sm:text-sm uppercase tracking-[0.25em] leading-relaxed">
              Autonomous 24/7 Multi-Tier Agent Engine & Sub-Second Neural Memory.
              Indulge in sub-second recall. Atone with zero token waste.
            </p>
          </div>

          {/* 
            ====================================================================
            REACT BITS COMPONENT #1: <PromptBar /> in the Hero / Prologue!
            Styled with dark lacquer black #121217, crisp white/black borders, gold/red keylines.
            ====================================================================
          */}
          <div className="w-full mt-10 max-w-3xl px-2">
            <div className="text-[10px] font-nikkei text-[#B91C1C] uppercase tracking-[0.2em] mb-2 text-center bg-black/60 py-1 px-3 border border-white/10 rounded-full inline-block">
              Interactive AI Prompt Cockpit • Select Model & Run /recall or /briefing
            </div>
            <PromptBar />
          </div>
        </div>

        {/* 
          Foreground: Monumental Billowing Fluid Liquid Mist Wave 
          Flowing at the base of the Hero spread, seamlessly connecting to the comic world
        */}
        <div className="relative w-full mt-12 z-10">
          <FluidWaterWave fillColor="#FBF9F5" />
        </div>

        {/* Scroll Indicator Prompt */}
        <div className="absolute bottom-6 left-1/2 -translate-x-1/2 z-20 flex flex-col items-center gap-1.5 text-black pointer-events-none select-none">
          <span className="font-nikkei text-[10px] tracking-[0.25em] uppercase text-black font-extrabold bg-[#FBF9F5] px-3 py-1 border border-black shadow-[2px_2px_0px_#000000]">
            SCROLL TO READ THE STORY
          </span>
          <ChevronDown className="w-4 h-4 animate-bounce text-[#B91C1C]" />
        </div>
      </section>

      {/* 
        ========================================================================
        SCENE SEAM TRANSITION: PROLOGUE → CHAPTER I
        ========================================================================
      */}
      <div id="narrative">
        <SceneTransition
          fromAct="PROLOGUE"
          toAct="CHAPTER I"
          badge="THE CONTEXT EXHAUSTION DISASTER"
        />
      </div>

      {/* 
        ========================================================================
        CHAPTER I: THE BURDEN OF DEAD LOGS (Context Bloat & 429 Cliff)
        ========================================================================
      */}
      <section className="relative py-16 px-4 sm:px-8 bg-[#0B0B0E] flex flex-col items-center justify-center">
        <div className="comic-plate relative w-full max-w-5xl p-6 sm:p-10 my-8">
          {/* Top-Right Comic Narration Box */}
          <div className="absolute top-6 right-6 z-20 max-w-xs sm:max-w-md comic-narration-box p-4 bg-white">
            <p className="text-[11px] sm:text-xs text-black font-nikkei tracking-wide uppercase leading-snug">
              In an immense land of unindexed dead logs.
            </p>
            <p className="text-xs sm:text-sm text-black font-nikkei tracking-wide uppercase font-extrabold leading-snug mt-1">
              A <span className="text-[#B91C1C]">tired agent</span> wanders through 50,000 tokens of raw context bloat, before crashing head-first into the 429 quota cliff.
            </p>
          </div>

          {/* Chapter Stamp & Header */}
          <div className="mb-8 pt-2">
            <div className="inline-block bg-black text-[#FBF9F5] font-nikkei text-xs uppercase px-3 py-1 tracking-widest mb-3 shadow-[2px_2px_0px_#B91C1C]">
              CHAPTER I • CHRONIC INEFFICIENCY
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl text-black tracking-tight leading-tight">
              The Memory Quota Abyss
            </h2>
            <p className="font-gt-era text-black/70 text-sm sm:text-base max-w-2xl mt-2 leading-relaxed">
              Every turn, traditional AI coding agents read megabytes of raw JSONL session logs from disk. By turn 15, token limits choke, latency explodes to 12.4 seconds, and developers face catastrophic 429 rate limits.
            </p>
          </div>

          {/* Excalidraw Hand-Drawn Architectural Diagram: Speed Benchmarks */}
          <div className="relative w-full border-2 border-black bg-white shadow-[6px_6px_0px_#000000] p-4 sm:p-6 mb-8 overflow-hidden group">
            <div className="flex items-center justify-between mb-3 border-b border-black/10 pb-2">
              <span className="font-nikkei text-xs uppercase tracking-wider text-black flex items-center gap-2">
                <Clock className="w-4 h-4 text-[#B91C1C]" />
                EXCALIDRAW ARCHITECTURAL BLUEPRINT • 24MS FTS5 VS 12,400MS RAW CRAWL
              </span>
              <button
                onClick={() => setSelectedInfographicModal("/infographics/infographic-speed-benchmarks.svg")}
                className="flex items-center gap-1 font-mono text-[11px] text-[#B91C1C] hover:underline cursor-pointer"
              >
                <Maximize2 className="w-3.5 h-3.5" /> Fullscreen
              </button>
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
              <span>Source: P:\open-source\aegis-brain\package\aegis\memory\fts5.py</span>
              <span className="text-emerald-700 font-bold">516x Measured Speedup</span>
            </div>
          </div>

          {/* Interactive 429 Quota Cliff Cockpit */}
          <div className="comic-card-dark p-5 sm:p-6 rounded-lg space-y-4 text-white">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-white/10 pb-3">
              <div>
                <h3 className="font-nikkei text-sm uppercase tracking-wider text-white flex items-center gap-2">
                  <Flame className="w-4 h-4 text-[#B91C1C]" />
                  Live Quota Cliff Simulator
                </h3>
                <p className="text-xs text-zinc-400 font-gt-era">
                  Experience the mechanical difference between crawling raw logs vs indexed neural FTS5.
                </p>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={runTraditionalSimulation}
                  className="px-3.5 py-1.5 bg-[#B91C1C] hover:bg-red-800 text-white font-mono text-xs rounded border border-black shadow-[2px_2px_0px_#000000] cursor-pointer"
                >
                  Test Traditional Agent
                </button>
                <button
                  onClick={runAegisSimulation}
                  className="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white font-mono text-xs rounded border border-black shadow-[2px_2px_0px_#000000] cursor-pointer"
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
                    <span className="text-[#B91C1C] flex items-center gap-1">
                      <AlertTriangle className="w-4 h-4" /> 429 RATE LIMIT
                    </span>
                  ) : quotaSimMode === "aegis" ? (
                    <span className="text-emerald-400 flex items-center gap-1">
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
        </div>
      </section>

      {/* 
        ========================================================================
        SCENE SEAM TRANSITION: CHAPTER I → CHAPTER II
        ========================================================================
      */}
      <SceneTransition
        fromAct="CHAPTER I"
        toAct="CHAPTER II"
        badge="THE 24MS RESURRECTION"
      />

      {/* 
        ========================================================================
        CHAPTER II: THE 24MS RESURRECTION (Neural Persistence & Fleet Memory)
        ========================================================================
      */}
      <section className="relative py-16 px-4 sm:px-8 bg-[#070709] flex flex-col items-center justify-center">
        <div className="comic-plate relative w-full max-w-5xl p-6 sm:p-10 my-8">
          {/* Top-Right Comic Narration Box */}
          <div className="absolute top-6 right-6 z-20 max-w-xs sm:max-w-md comic-narration-box p-4 bg-white">
            <p className="text-[11px] sm:text-xs text-black font-nikkei tracking-wide uppercase leading-snug">
              Every session reboot was an executioner&apos;s axe.
            </p>
            <p className="text-xs sm:text-sm text-black font-nikkei tracking-wide uppercase font-extrabold leading-snug mt-1">
              Until Aegis forged <span className="text-[#B91C1C]">SQLite FTS5 neural indexes</span> into the agent chassis. 24 milliseconds to total recall.
            </p>
          </div>

          {/* Chapter Stamp & Header */}
          <div className="mb-8 pt-2">
            <div className="inline-block bg-black text-[#FBF9F5] font-nikkei text-xs uppercase px-3 py-1 tracking-widest mb-3 shadow-[2px_2px_0px_#B91C1C]">
              CHAPTER II • NEURAL PERSISTENCE
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl text-black tracking-tight leading-tight">
              Sub-Second Memory & Fleet Sovereignty
            </h2>
            <p className="font-gt-era text-black/70 text-sm sm:text-base max-w-2xl mt-2 leading-relaxed">
              When an agent forgets, developers suffer. Aegis embeds SQLite WAL persistence (<code className="font-mono bg-black/10 px-1 py-0.5 rounded">brain.db</code>) with full-text BM25 ranking across all codebases and CLI engines.
            </p>
          </div>

          {/* Excalidraw Hand-Drawn Architectural Diagram: Universal Fleet Compatibility */}
          <div className="relative w-full border-2 border-black bg-white shadow-[6px_6px_0px_#000000] p-4 sm:p-6 mb-8 overflow-hidden group">
            <div className="flex items-center justify-between mb-3 border-b border-black/10 pb-2">
              <span className="font-nikkei text-xs uppercase tracking-wider text-black flex items-center gap-2">
                <Layers className="w-4 h-4 text-[#B91C1C]" />
                EXCALIDRAW ARCHITECTURAL BLUEPRINT • UNIVERSAL FLEET COMPATIBILITY
              </span>
              <button
                onClick={() => setSelectedInfographicModal("/infographics/infographic-universal-agents.svg")}
                className="flex items-center gap-1 font-mono text-[11px] text-[#B91C1C] hover:underline cursor-pointer"
              >
                <Maximize2 className="w-3.5 h-3.5" /> Fullscreen
              </button>
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

          {/* 
            ====================================================================
            REACT BITS COMPONENT #2: <ThoughtLine /> in Chapter II!
            Showing agent recovering from amnesia via 24ms SQLite FTS5 recall.
            ====================================================================
          */}
          <div className="mb-8">
            <div className="text-xs font-nikkei text-black uppercase tracking-wider mb-2 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-[#B91C1C]" />
              React Bits ThoughtLine • Sub-Second Amnesia Recovery Trace
            </div>
            <ThoughtLine
              summary="Neural Recall Trace: Retrieved 4 symbols & test invariants from brain.db in 21ms"
              totalTime="21 ms"
              defaultExpanded={true}
            />
          </div>

          {/* AI Tool Cockpit: StopwatchDial */}
          <div className="border-2 border-black rounded-lg overflow-hidden shadow-[6px_6px_0px_#000000] bg-[#0E0F16]">
            <StopwatchDial />
          </div>
        </div>
      </section>

      {/* 
        ========================================================================
        SCENE SEAM TRANSITION: CHAPTER II → CHAPTER III
        ========================================================================
      */}
      <SceneTransition
        fromAct="CHAPTER II"
        toAct="CHAPTER III"
        badge="THE UNBREAKABLE GUARDIAN"
      />

      {/* 
        ========================================================================
        CHAPTER III: THE 24/7 KEEPALIVE SHIELD (Win32 Standby & Resilience)
        ========================================================================
      */}
      <section className="relative py-16 px-4 sm:px-8 bg-[#0B0B0E] flex flex-col items-center justify-center">
        <div className="comic-plate relative w-full max-w-5xl p-6 sm:p-10 my-8">
          {/* Top-Right Comic Narration Box */}
          <div className="absolute top-6 right-6 z-20 max-w-xs sm:max-w-md comic-narration-box p-4 bg-white">
            <p className="text-[11px] sm:text-xs text-black font-nikkei tracking-wide uppercase leading-snug">
              Windows tried to put the mind to sleep.
            </p>
            <p className="text-xs sm:text-sm text-black font-nikkei tracking-wide uppercase font-extrabold leading-snug mt-1">
              Win32 connected standby kills background processes silently. Aegis built an <span className="text-[#B91C1C]">immortal Scheduled Task & daemon keepalive</span>.
            </p>
          </div>

          {/* Chapter Stamp & Header */}
          <div className="mb-8 pt-2">
            <div className="inline-block bg-black text-[#FBF9F5] font-nikkei text-xs uppercase px-3 py-1 tracking-widest mb-3 shadow-[2px_2px_0px_#B91C1C]">
              CHAPTER III • IMMORTAL DAEMON
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl text-black tracking-tight leading-tight">
              The 24/7 KeepAlive Shield & Win32 Resilience
            </h2>
            <p className="font-gt-era text-black/70 text-sm sm:text-base max-w-2xl mt-2 leading-relaxed">
              Operating an AI assistant overnight requires absolute resilience. Win32 connected standby, sleep transitions, and terminal terminations can disrupt unshielded agents. Aegis introduces a multi-layered watchdog system.
            </p>
          </div>

          {/* Side-by-Side Comparison Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {/* Card 1: Traditional Vulnerability */}
            <div className="comic-card-red p-6 rounded-lg space-y-3">
              <div className="flex items-center justify-between border-b border-black/10 pb-2">
                <span className="font-nikkei text-xs uppercase tracking-wider text-[#B91C1C] font-bold">
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
                <span className="font-nikkei text-xs uppercase tracking-wider text-emerald-700 font-bold">
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
                  <span><strong>Zero Disruption:</strong> Seamless persistence across reboots, account switches, and command terminal terminations.</span>
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
                <div className="font-nikkei text-xs uppercase tracking-wider text-black">
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
        </div>
      </section>

      {/* 
        ========================================================================
        SCENE SEAM TRANSITION: CHAPTER III → CHAPTER IV
        ========================================================================
      */}
      <SceneTransition
        fromAct="CHAPTER III"
        toAct="CHAPTER IV"
        badge="ONE-LINE ENGINE BOOTSTRAP"
      />

      {/* 
        ========================================================================
        CHAPTER IV: THE SOVEREIGN ARSENAL (Instant Deployment Cockpit)
        ========================================================================
      */}
      <section id="install" className="relative py-16 px-4 sm:px-8 bg-[#070709] flex flex-col items-center justify-center">
        <div className="comic-plate relative w-full max-w-5xl p-6 sm:p-10 my-8">
          {/* Top-Right Comic Narration Box */}
          <div className="absolute top-6 right-6 z-20 max-w-xs sm:max-w-md comic-narration-box p-4 bg-white">
            <p className="text-[11px] sm:text-xs text-black font-nikkei tracking-wide uppercase leading-snug">
              No complex Docker swarms. No hostage dependencies.
            </p>
            <p className="text-xs sm:text-sm text-black font-nikkei tracking-wide uppercase font-extrabold leading-snug mt-1">
              One command installs the <span className="text-[#B91C1C]">daemon, the CLI, the Telegram bridge</span>, and the neural memory engine.
            </p>
          </div>

          {/* Chapter Stamp & Header */}
          <div className="mb-8 pt-2">
            <div className="inline-block bg-black text-[#FBF9F5] font-nikkei text-xs uppercase px-3 py-1 tracking-widest mb-3 shadow-[2px_2px_0px_#B91C1C]">
              CHAPTER IV • ONE-LINE INSTALLATION
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl text-black tracking-tight leading-tight">
              The Multi-OS Terminal Cockpit
            </h2>
            <p className="font-gt-era text-black/70 text-sm sm:text-base max-w-2xl mt-2 leading-relaxed">
              Zero complicated configurations. AegisBrain is delivered as a sovereign binary with native installer scripts across Linux, macOS, and Windows.
            </p>
          </div>

          {/* AI Tool Cockpit: TerminalInstall */}
          <div className="border-2 border-black rounded-lg overflow-hidden shadow-[6px_6px_0px_#000000] bg-[#0E0F16]">
            <TerminalInstall />
          </div>
        </div>
      </section>

      {/* 
        ========================================================================
        SCENE SEAM TRANSITION: CHAPTER IV → CHAPTER V
        ========================================================================
      */}
      <div id="hierarchy">
        <SceneTransition
          fromAct="CHAPTER IV"
          toAct="CHAPTER V"
          badge="TOKEN ARBITRAGE & THE 3-TIER FORGE"
        />
      </div>

      {/* 
        ========================================================================
        CHAPTER V: THE 3-TIER TOKEN FORGE (Brain vs Execution Muscle)
        ========================================================================
      */}
      <section className="relative py-16 px-4 sm:px-8 bg-[#0B0B0E] flex flex-col items-center justify-center">
        <div className="comic-plate relative w-full max-w-5xl p-6 sm:p-10 my-8">
          {/* Top-Right Comic Narration Box */}
          <div className="absolute top-6 right-6 z-20 max-w-xs sm:max-w-md comic-narration-box p-4 bg-white">
            <p className="text-[11px] sm:text-xs text-black font-nikkei tracking-wide uppercase leading-snug">
              Why burn $20/hr letting frontier models write boilerplate?
            </p>
            <p className="text-xs sm:text-sm text-black font-nikkei tracking-wide uppercase font-extrabold leading-snug mt-1">
              Tier 1 plans. Tier 2 audits. <span className="text-[#B91C1C]">Tier 3 local workers</span> hammer out the code for zero frontier tokens.
            </p>
          </div>

          {/* Chapter Stamp & Header */}
          <div className="mb-8 pt-2">
            <div className="inline-block bg-black text-[#FBF9F5] font-nikkei text-xs uppercase px-3 py-1 tracking-widest mb-3 shadow-[2px_2px_0px_#B91C1C]">
              CHAPTER V • FREE TOKEN ARBITRAGE
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl text-black tracking-tight leading-tight">
              The 3-Tier Multi-Agent Hierarchy
            </h2>
            <p className="font-gt-era text-black/70 text-sm sm:text-base max-w-2xl mt-2 leading-relaxed">
              Frontier models (Claude Opus, Gemini 4) are strategic brains, not construction grunts. AegisBrain enforces strict division of labor: high-cognition models architect and coach, while local CLI workers (Hermes, Ollama, Qwen) execute implementations for free.
            </p>
          </div>

          {/* Excalidraw Hand-Drawn Architectural Diagram: Hierarchy Pyramid */}
          <div className="relative w-full border-2 border-black bg-white shadow-[6px_6px_0px_#000000] p-4 sm:p-6 mb-8 overflow-hidden group">
            <div className="flex items-center justify-between mb-3 border-b border-black/10 pb-2">
              <span className="font-nikkei text-xs uppercase tracking-wider text-black flex items-center gap-2">
                <Cpu className="w-4 h-4 text-[#B91C1C]" />
                EXCALIDRAW ARCHITECTURAL BLUEPRINT • 3-TIER HIERARCHY PYRAMID
              </span>
              <button
                onClick={() => setSelectedInfographicModal("/infographics/infographic-hierarchy-pyramid.svg")}
                className="flex items-center gap-1 font-mono text-[11px] text-[#B91C1C] hover:underline cursor-pointer"
              >
                <Maximize2 className="w-3.5 h-3.5" /> Fullscreen
              </button>
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
              <span>Dynamic Workload Triage: Micro-tasks direct, Macro-tasks delegated</span>
              <span className="text-emerald-700 font-bold">$1,840/mo Measured Savings</span>
            </div>
          </div>

          {/* 
            ====================================================================
            REACT BITS COMPONENT #3: <CallChip /> in Chapter V!
            Showing live local worker tool invocations.
            ====================================================================
          */}
          <div className="mb-8 p-4 bg-white border-2 border-black shadow-[4px_4px_0px_#000000] space-y-3">
            <div className="flex items-center justify-between border-b border-black/10 pb-2">
              <span className="font-nikkei text-xs uppercase tracking-wider text-black flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-[#B91C1C]" />
                React Bits CallChip • Active Tier 3 Local Worker Invocations
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

          {/* AI Tool Cockpit: ArbitrageCalculator */}
          <div className="border-2 border-black rounded-lg overflow-hidden shadow-[6px_6px_0px_#000000] bg-[#0E0F16]">
            <ArbitrageCalculator />
          </div>
        </div>
      </section>

      {/* 
        ========================================================================
        SCENE SEAM TRANSITION: CHAPTER V → CHAPTER VI
        ========================================================================
      */}
      <SceneTransition
        fromAct="CHAPTER V"
        toAct="CHAPTER VI"
        badge="THE FOUR GATES OF STEEL"
      />

      {/* 
        ========================================================================
        CHAPTER VI: THE 4-STAGE QUALITY GATE (Adversarial Error-Free Gates)
        ========================================================================
      */}
      <section className="relative py-16 px-4 sm:px-8 bg-[#070709] flex flex-col items-center justify-center">
        <div className="comic-plate relative w-full max-w-5xl p-6 sm:p-10 my-8">
          {/* Top-Right Comic Narration Box */}
          <div className="absolute top-6 right-6 z-20 max-w-xs sm:max-w-md comic-narration-box p-4 bg-white">
            <p className="text-[11px] sm:text-xs text-black font-nikkei tracking-wide uppercase leading-snug">
              No unverified draft escapes to production.
            </p>
            <p className="text-xs sm:text-sm text-black font-nikkei tracking-wide uppercase font-extrabold leading-snug mt-1">
              Every candidate line passes 4 automated gates: <span className="text-[#B91C1C]">Karpathy Simplicity, Unslop sanitization, Red-Team security, and Dual-Environment verification</span>.
            </p>
          </div>

          {/* Chapter Stamp & Header */}
          <div className="mb-8 pt-2">
            <div className="inline-block bg-black text-[#FBF9F5] font-nikkei text-xs uppercase px-3 py-1 tracking-widest mb-3 shadow-[2px_2px_0px_#B91C1C]">
              CHAPTER VI • ZERO-DEFECT AUDIT
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl text-black tracking-tight leading-tight">
              The 4-Decision Quality Architecture Gate
            </h2>
            <p className="font-gt-era text-black/70 text-sm sm:text-base max-w-2xl mt-2 leading-relaxed">
              When lower-tier models generate code, errors occur. Rather than discarding local models, Aegis applies an adversarial compiler and static analysis gate that coach the worker until zero defects remain.
            </p>
          </div>

          {/* Excalidraw Hand-Drawn Architectural Diagrams Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {/* Diagram 1: Quality Gate */}
            <div className="border-2 border-black bg-white shadow-[6px_6px_0px_#000000] p-4 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="font-nikkei text-xs uppercase text-black font-bold">
                    1. The 4-Decision Pipeline
                  </span>
                  <button
                    onClick={() => setSelectedInfographicModal("/infographics/infographic-quality-gate.svg")}
                    className="font-mono text-[10px] text-[#B91C1C] hover:underline cursor-pointer"
                  >
                    Zoom
                  </button>
                </div>
                <div className="relative w-full h-[220px] bg-[#FAF8F5] border border-black/10 flex items-center justify-center">
                  <Image
                    src="/infographics/infographic-quality-gate.svg"
                    alt="4-Decision Quality Architecture Gate"
                    fill
                    className="object-contain p-2"
                  />
                </div>
              </div>
              <div className="text-[10px] font-mono text-black/60 mt-2">
                Simplicity → Unslop → Red-Team AST → Dual-Env
              </div>
            </div>

            {/* Diagram 2: Learning Curve */}
            <div className="border-2 border-black bg-white shadow-[6px_6px_0px_#000000] p-4 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="font-nikkei text-xs uppercase text-black font-bold">
                    2. Worker Confidence Curve
                  </span>
                  <button
                    onClick={() => setSelectedInfographicModal("/infographics/infographic-learning-curve.svg")}
                    className="font-mono text-[10px] text-[#B91C1C] hover:underline cursor-pointer"
                  >
                    Zoom
                  </button>
                </div>
                <div className="relative w-full h-[220px] bg-[#FAF8F5] border border-black/10 flex items-center justify-center">
                  <Image
                    src="/infographics/infographic-learning-curve.svg"
                    alt="Worker Confidence and Error Reduction Curve"
                    fill
                    className="object-contain p-2"
                  />
                </div>
              </div>
              <div className="text-[10px] font-mono text-black/60 mt-2">
                Autonomous error coaching converges to &gt;8.0/10 confidence
              </div>
            </div>
          </div>

          {/* AI Tool Cockpit: QualityGateCards */}
          <div className="border-2 border-black rounded-lg overflow-hidden shadow-[6px_6px_0px_#000000] bg-[#0E0F16]">
            <QualityGateCards />
          </div>
        </div>
      </section>

      {/* 
        ========================================================================
        SCENE SEAM TRANSITION: CHAPTER VI → CHAPTER VII
        ========================================================================
      */}
      <SceneTransition
        fromAct="CHAPTER VI"
        toAct="CHAPTER VII"
        badge="24/7 MOBILE TELEGRAM SOVEREIGNTY"
      />

      {/* 
        ========================================================================
        CHAPTER VII: TOTAL REMOTE FREEDOM (In-Flight Mobile Telegram Companion)
        ========================================================================
      */}
      <section className="relative py-16 px-4 sm:px-8 bg-[#0B0B0E] flex flex-col items-center justify-center">
        <div className="comic-plate relative w-full max-w-5xl p-6 sm:p-10 my-8">
          {/* Top-Right Comic Narration Box */}
          <div className="absolute top-6 right-6 z-20 max-w-xs sm:max-w-md comic-narration-box p-4 bg-white">
            <p className="text-[11px] sm:text-xs text-black font-nikkei tracking-wide uppercase leading-snug">
              Controlling your agents from the train, gym, or airport.
            </p>
            <p className="text-xs sm:text-sm text-black font-nikkei tracking-wide uppercase font-extrabold leading-snug mt-1">
              Speak a 45-second voice note. <span className="text-[#B91C1C]">Deterministic 25s FFmpeg chunking</span> shields Whisper STT from hallucinations. Keystroke injection via <code className="font-mono">/type</code>.
            </p>
          </div>

          {/* Chapter Stamp & Header */}
          <div className="mb-8 pt-2">
            <div className="inline-block bg-black text-[#FBF9F5] font-nikkei text-xs uppercase px-3 py-1 tracking-widest mb-3 shadow-[2px_2px_0px_#B91C1C]">
              CHAPTER VII • REMOTE TELEGRAM BRIDGE
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl text-black tracking-tight leading-tight">
              Real-Time Mobile Command Center
            </h2>
            <p className="font-gt-era text-black/70 text-sm sm:text-base max-w-2xl mt-2 leading-relaxed">
              True developer autonomy means never being chained to a desk. AegisBrain runs a 24/7 Telegram companion (<code className="font-mono bg-black/10 px-1">@HHAACLIBot</code>) with audio transcription shielding and in-flight terminal control.
            </p>
          </div>

          {/* Excalidraw Hand-Drawn Architectural Diagram: Mobile Pipeline */}
          <div className="relative w-full border-2 border-black bg-white shadow-[6px_6px_0px_#000000] p-4 sm:p-6 mb-8 overflow-hidden group">
            <div className="flex items-center justify-between mb-3 border-b border-black/10 pb-2">
              <span className="font-nikkei text-xs uppercase tracking-wider text-black flex items-center gap-2">
                <Smartphone className="w-4 h-4 text-[#B91C1C]" />
                EXCALIDRAW ARCHITECTURAL BLUEPRINT • 24/7 MOBILE TELEGRAM PIPELINE
              </span>
              <button
                onClick={() => setSelectedInfographicModal("/infographics/infographic-mobile-pipeline.svg")}
                className="flex items-center gap-1 font-mono text-[11px] text-[#B91C1C] hover:underline cursor-pointer"
              >
                <Maximize2 className="w-3.5 h-3.5" /> Fullscreen
              </button>
            </div>

            <div className="relative w-full h-[280px] sm:h-[420px] bg-[#FAF8F5] flex items-center justify-center overflow-hidden border border-black/10">
              <Image
                src="/infographics/infographic-mobile-pipeline.svg"
                alt="24/7 Mobile Telegram Ingestion Pipeline: Phone mic to FFmpeg chunking to Whisper STT to Antigravity /type injection"
                fill
                className="object-contain p-2 hover:scale-[1.02] transition-transform duration-300"
              />
            </div>
            <div className="mt-3 flex items-center justify-between text-[11px] font-mono text-black/60">
              <span>Deterministic 25-Second Chunking Shield: 0 Hallucinations</span>
              <span className="text-emerald-700 font-bold">In-Flight /type /alt+m Interrupt</span>
            </div>
          </div>

          {/* 
            ====================================================================
            AI TOOL COCKPIT: TelegramSimulator with integrated REACT BITS <VoicePill />!
            ====================================================================
          */}
          <div className="border-2 border-black rounded-lg overflow-hidden shadow-[6px_6px_0px_#000000] bg-[#0E0F16] p-4 sm:p-6">
            <TelegramSimulator />
          </div>
        </div>
      </section>

      {/* 
        ========================================================================
        SCENE SEAM TRANSITION: CHAPTER VII → CHAPTER VIII
        ========================================================================
      */}
      <div id="blueprints">
        <SceneTransition
          fromAct="CHAPTER VII"
          toAct="CHAPTER VIII"
          badge="THE UNIFIED BLUEPRINT"
        />
      </div>

      {/* 
        ========================================================================
        CHAPTER VIII: THE UNIFIED SYSTEM BLUEPRINT (Blueprint & Gallery)
        ========================================================================
      */}
      <section className="relative py-16 px-4 sm:px-8 bg-[#070709] flex flex-col items-center justify-center">
        <div className="comic-plate relative w-full max-w-5xl p-6 sm:p-10 my-8">
          {/* Top-Right Comic Narration Box */}
          <div className="absolute top-6 right-6 z-20 max-w-xs sm:max-w-md comic-narration-box p-4 bg-white">
            <p className="text-[11px] sm:text-xs text-black font-nikkei tracking-wide uppercase leading-snug">
              The complete blueprint of autonomous persistence.
            </p>
            <p className="text-xs sm:text-sm text-black font-nikkei tracking-wide uppercase font-extrabold leading-snug mt-1">
              Inspect every diagram hand-crafted with Data Professor clarity: <span className="text-[#B91C1C]">architecture, memory, hierarchy, and pipelines</span>.
            </p>
          </div>

          {/* Chapter Stamp & Header */}
          <div className="mb-8 pt-2">
            <div className="inline-block bg-black text-[#FBF9F5] font-nikkei text-xs uppercase px-3 py-1 tracking-widest mb-3 shadow-[2px_2px_0px_#B91C1C]">
              CHAPTER VIII • ARCHITECTURAL BLUEPRINTS
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl text-black tracking-tight leading-tight">
              The Interactive Infographics Gallery
            </h2>
            <p className="font-gt-era text-black/70 text-sm sm:text-base max-w-2xl mt-2 leading-relaxed">
              Explore the entire technical system diagram suite. Switch between architecture topologies, speed benchmarks, quality gates, and mobile pipelines with full zoom and inspection.
            </p>
          </div>

          {/* AI Tool Cockpit: InfographicsGallery */}
          <div className="border-2 border-black rounded-lg overflow-hidden shadow-[6px_6px_0px_#000000] bg-[#0E0F16]">
            <InfographicsGallery />
          </div>
        </div>
      </section>

      {/* 
        ========================================================================
        SCENE SEAM TRANSITION: CHAPTER VIII → EPILOGUE
        ========================================================================
      */}
      <SceneTransition
        fromAct="CHAPTER VIII"
        toAct="EPILOGUE"
        badge="SOVEREIGN DELIVERANCE & ARCHIVE"
      />

      {/* 
        ========================================================================
        EPILOGUE: THE ATONEMENT & DOWNLOAD ARCHIVE
        ========================================================================
      */}
      <footer className="relative py-20 px-4 sm:px-8 bg-[#070709] border-t-4 border-black text-white">
        <div className="max-w-5xl mx-auto space-y-12">
          {/* Main Download Plate */}
          <div className="comic-plate p-8 sm:p-12 text-black">
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 border-b-2 border-black pb-8">
              <div>
                <div className="inline-block bg-[#B91C1C] text-white font-nikkei text-xs uppercase px-3 py-1 tracking-widest mb-2 shadow-[2px_2px_0px_#000000]">
                  OFFICIAL SOVEREIGN RELEASE • V2.4.0
                </div>
                <h3 className="font-charles-rosie text-3xl sm:text-4xl text-black tracking-tight">
                  AegisBrain Engine Archive
                </h3>
                <p className="font-gt-era text-black/70 text-sm mt-1 max-w-lg">
                  Free and open source under the Apache-2.0 License. Verified against 286 backend unit tests.
                </p>
              </div>

              <div className="flex flex-wrap items-center gap-3">
                <a
                  href="https://github.com/PG300604/aegis-brain/releases"
                  target="_blank"
                  rel="noreferrer"
                  className="px-5 py-2.5 bg-black hover:bg-neutral-800 text-white font-nikkei text-xs uppercase tracking-wider rounded border border-black shadow-[4px_4px_0px_#B91C1C] flex items-center gap-2 cursor-pointer"
                >
                  <Download className="w-4 h-4 text-[#B91C1C]" />
                  Download Tarball
                </a>
                <a
                  href="https://github.com/PG300604/aegis-brain"
                  target="_blank"
                  rel="noreferrer"
                  className="px-5 py-2.5 bg-[#FBF9F5] hover:bg-neutral-100 text-black font-nikkei text-xs uppercase tracking-wider rounded border-2 border-black shadow-[4px_4px_0px_#000000] flex items-center gap-2 cursor-pointer"
                >
                  <Star className="w-4 h-4 text-[#B91C1C] fill-[#B91C1C]" />
                  Star on GitHub
                </a>
              </div>
            </div>

            {/* SHA Hashes and Integrity Badges */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-6 font-mono text-xs">
              <div className="p-3 bg-white border border-black shadow-[2px_2px_0px_#000000] flex items-center justify-between">
                <div>
                  <div className="text-[10px] text-zinc-500 uppercase">Git Commit SHA</div>
                  <div className="font-bold text-black mt-0.5">690b8cd96671994ab1709628</div>
                </div>
                <button
                  onClick={() => handleCopySha("690b8cd96671994ab170962811d20508a46c2a9a")}
                  className="p-1.5 hover:bg-zinc-100 rounded border border-black text-black cursor-pointer"
                  title="Copy Commit SHA"
                >
                  {copiedSha === "690b8cd96671994ab170962811d20508a46c2a9a" ? (
                    <Check className="w-3.5 h-3.5 text-emerald-600" />
                  ) : (
                    <Copy className="w-3.5 h-3.5" />
                  )}
                </button>
              </div>

              <div className="p-3 bg-white border border-black shadow-[2px_2px_0px_#000000] flex items-center justify-between">
                <div>
                  <div className="text-[10px] text-zinc-500 uppercase">GPG Signer Key</div>
                  <div className="font-bold text-black mt-0.5">0x7F41E8D2 (Priyanshu Ghosh)</div>
                </div>
                <span className="text-[10px] bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded font-bold">
                  VERIFIED
                </span>
              </div>
            </div>

            {/* 7-Vector Comparison Matrix */}
            <div className="mt-8 pt-6 border-t border-black/10">
              <h4 className="font-nikkei text-xs uppercase tracking-wider text-black mb-3">
                7-Vector Architectural Comparison Matrix
              </h4>
              <div className="overflow-x-auto">
                <table className="w-full text-left font-mono text-[11px] border-collapse border border-black">
                  <thead>
                    <tr className="bg-black text-white">
                      <th className="p-2.5 border border-black">Vector</th>
                      <th className="p-2.5 border border-black text-[#00F0FF]">AegisBrain</th>
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
              className="relative w-full max-w-6xl max-h-[90vh] bg-[#FAF8F5] border-4 border-black shadow-[12px_12px_0px_#B91C1C] rounded-lg p-6 flex flex-col"
            >
              <div className="flex items-center justify-between border-b-2 border-black pb-3 mb-4">
                <span className="font-nikkei text-sm uppercase text-black font-extrabold flex items-center gap-2">
                  <Maximize2 className="w-4 h-4 text-[#B91C1C]" />
                  AegisBrain Hand-Drawn Architectural Blueprint • High-Resolution View
                </span>
                <button
                  onClick={() => setSelectedInfographicModal(null)}
                  className="p-1.5 bg-black text-white hover:bg-[#B91C1C] rounded border border-black cursor-pointer transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="relative w-full flex-1 min-h-[400px] sm:min-h-[600px] bg-white border border-black/20 flex items-center justify-center overflow-auto p-4">
                <Image
                  src={selectedInfographicModal}
                  alt="AegisBrain Blueprint Fullscreen View"
                  fill
                  className="object-contain"
                />
              </div>

              <div className="mt-4 flex items-center justify-between text-xs font-mono text-black/70">
                <span>Hand-crafted Data Professor style SVG diagram</span>
                <a
                  href={selectedInfographicModal}
                  download
                  className="text-[#B91C1C] font-bold hover:underline flex items-center gap-1"
                >
                  <Download className="w-3.5 h-3.5" /> Download SVG
                </a>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
