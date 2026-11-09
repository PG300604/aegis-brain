"use client";

import React, { useState, useEffect, useRef } from "react";
import {
  VolumeX,
  Copy,
  Check,
  ChevronDown,
  ArrowRight,
  FileCode,
  CheckCircle2,
  AlertTriangle,
  Star,
} from "lucide-react";
import { motion, useScroll, useTransform } from "motion/react";
import { ThoughtLine } from "@/components/react-bits/ThoughtLine";
import { CallChip } from "@/components/react-bits/CallChip";
import { TerminalInstall } from "@/components/hud/TerminalInstall";
import { ArbitrageCalculator } from "@/components/hud/ArbitrageCalculator";
import { QualityGateCards } from "@/components/hud/QualityGateCards";
import { TelegramSimulator } from "@/components/hud/TelegramSimulator";
import { InfographicsGallery } from "@/components/hud/InfographicsGallery";
import { Feature06StatsBadge } from "@/components/hud/Feature06StatsBadge";
import { Feature06PipelineFlow } from "@/components/hud/Feature06PipelineFlow";
import { Feature06BlueprintCards } from "@/components/hud/Feature06BlueprintCards";
import { ParallaxCard } from "@/components/motion/ParallaxCard";
import { LoadingScreen } from "@/components/motion/LoadingScreen";
import { CursorPhysicsProvider } from "@/components/motion/CursorPhysicsProvider";
import { CloudMistBank } from "@/components/motion/CloudMistBank";
import { FlowCloudCanvas } from "@/components/motion/FlowCloudCanvas";
import { InteractiveTierDiagram } from "@/components/hud/InteractiveTierDiagram";
import { LaptopCliFrame } from "@/components/hud/LaptopCliFrame";
import { SoundtrackController, triggerSoundEffect } from "@/components/audio/SoundtrackController";

export default function Home() {
  const [scrollProgress, setScrollProgress] = useState(0);
  const [soundActive, setSoundActive] = useState(false);
  const [copiedClone, setCopiedClone] = useState(false);

  // Hero section scroll animations
  const heroRef = useRef<HTMLElement>(null);
  const { scrollYProgress: heroScroll } = useScroll({
    target: heroRef,
    offset: ["start start", "end start"],
  });
  const cloudY = useTransform(heroScroll, [0, 1], ["0%", "-30%"]);
  const cloudScale = useTransform(heroScroll, [0, 1], [1, 1.06]);
  const heroOpacity = useTransform(heroScroll, [0, 0.7], [1, 0.15]);
  const heroScale = useTransform(heroScroll, [0, 0.9], [1, 0.94]);

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

  return (
    <CursorPhysicsProvider>
      <div className="relative min-h-screen bg-[#070709] text-[#0D0D11] selection:bg-[#B91C1C] selection:text-white">
      {/* Cinematic Sovereign Preloader with AegisBrain Logo Top-Left */}
      <LoadingScreen />

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
        className="relative min-h-screen w-full flex flex-col items-center justify-between pt-28 pb-0 sm:pt-32 px-4 bg-[#070709] overflow-hidden"
      >
        {/* Center: Monumental Headline with Staggered Entrance Animation & Scroll Dissolve */}
        <motion.div
          style={{ opacity: heroOpacity, scale: heroScale }}
          className="relative z-10 text-center flex flex-col items-center max-w-5xl mx-auto select-none pt-2 sm:pt-4"
        >
          <motion.p
            initial={{ opacity: 0, y: 15, letterSpacing: "0.2em" }}
            animate={{ opacity: 0.75, y: 0, letterSpacing: "0.35em" }}
            transition={{ duration: 0.9, ease: [0.16, 1, 0.3, 1] }}
            className="font-charles-rosie text-white text-base sm:text-xl uppercase mb-1"
          >
            The
          </motion.p>

          <motion.h1
            initial={{ opacity: 0, y: 35, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ duration: 1.0, delay: 0.12, ease: [0.16, 1, 0.3, 1] }}
            className="font-charles-rosie text-white text-5xl sm:text-7xl md:text-8xl lg:text-9xl leading-[0.88] tracking-tight uppercase drop-shadow-[0_12px_35px_rgba(0,0,0,0.95)]"
          >
            Aeg<span className="text-[#B91C1C]">i</span>s
          </motion.h1>

          <motion.h2
            initial={{ opacity: 0, y: 25 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1.0, delay: 0.25, ease: [0.16, 1, 0.3, 1] }}
            className="font-charles-rosie text-white text-2xl sm:text-4xl md:text-5xl lg:text-6xl leading-tight tracking-[0.16em] uppercase mt-1 drop-shadow-[0_8px_25px_rgba(0,0,0,0.95)]"
          >
            Experience
          </motion.h2>

          {/* Punchy, Non-Slop Directives */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.9, delay: 0.38, ease: [0.16, 1, 0.3, 1] }}
            className="mt-8 max-w-3xl mx-auto px-4"
          >
            <h3 className="font-nikkei text-[#D4AF37] text-base sm:text-xl md:text-2xl uppercase tracking-[0.2em] font-extrabold leading-tight">
              TAKE FULL CONTROL OF YOUR AGENTS
            </h3>
          </motion.div>
        </motion.div>

        {/* Billowing Cumulus Cloud Mist Bank from Google Flow (190 Frames Scroll-Scrubbed + 60fps Ambient Motion) */}
        <motion.div style={{ y: cloudY, scale: cloudScale }} className="relative w-full mt-auto z-20 origin-bottom">
          <FlowCloudCanvas fillColor="#FAF8F5" />
        </motion.div>

        {/* Minimal Editorial Scroll Indicator */}
        <div className="relative z-30 flex flex-col items-center gap-1 pb-4 -mt-8 pointer-events-none select-none">
          <ChevronDown className="w-4 h-4 text-white/50 animate-bounce" />
        </div>
      </section>

      {/* 
        ========================================================================
        FEATURE 01: PERMANENT AGENT MEMORY (Real Developer Experience)
        ========================================================================
      */}
      <ParallaxCard index={0} id="memory">
        <div className="comic-plate relative w-full p-6 sm:p-12">
          {/* Feature Header in Human Real-Life Terms */}
          <div className="mb-8 pt-2">
            <div className="font-nikkei text-xs uppercase text-[#B91C1C] font-extrabold tracking-widest mb-2">
              FEATURE 01 // PERMANENT AGENT MEMORY
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl lg:text-6xl text-black tracking-tight leading-tight uppercase">
              Never Suffer From Agent Amnesia Again
            </h2>
            <p className="font-gt-era text-black/85 text-base sm:text-lg max-w-4xl mt-3 leading-relaxed">
              Every time you close your terminal or start a new day, standard AI coding agents forget everything. They waste minutes re-reading your entire project logs from disk—crashing into API token rate limits and freezing right when you&apos;re in the flow.
            </p>
            <p className="font-gt-era text-black/75 text-sm sm:text-base max-w-4xl mt-2 leading-relaxed">
              AegisBrain gives your assistant a permanent photographic notebook. When you say &ldquo;continue where we left off yesterday&rdquo;, it instantly recalls your exact architectural rules, past bug fixes, and project decisions without burning your tokens.
            </p>
          </div>

          {/* Claude Code Terminal Inside Laptop Display Frame */}
          <div className="mb-8">
            <LaptopCliFrame />
          </div>

          {/* Real-Time Memory Retrieval Trace */}
          <div className="mb-4">
            <div className="text-xs font-nikkei text-black uppercase tracking-wider mb-2 flex items-center gap-2 font-bold">
              <span className="w-2 h-2 rounded-full bg-[#B91C1C]" />
              Real-Time Memory Retrieval Trace
            </div>
            <ThoughtLine
              summary="Neural Recall Trace: Retrieved 4 symbols & test invariants from brain.db in 21ms"
              totalTime="21 ms"
              defaultExpanded={false}
            />
          </div>
        </div>
      </ParallaxCard>


      {/* 
        ========================================================================
        FEATURE 02: DETERMINISTIC 3-TIER LOCAL TOKEN ARBITRAGE ENGINE
        ========================================================================
      */}
      <ParallaxCard index={1} id="arbitrage">
        <div className="comic-plate relative w-full p-6 sm:p-10">
          <div className="mb-8 pt-2">
            <div className="font-nikkei text-xs uppercase text-[#B91C1C] font-extrabold tracking-widest mb-2">
              FEATURE 02 // TOKEN ARBITRAGE
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl text-black tracking-tight leading-tight uppercase">
              Slash Your AI API Bill by 92%
            </h2>
            <p className="font-gt-era text-black/75 text-sm sm:text-base max-w-3xl mt-2 leading-relaxed">
              Why pay $20 per million tokens for expensive models to write repetitive boilerplate? Frontier models act as the strategic brain, while free local models running on your own computer do the grunt work for $0.00.
            </p>
          </div>

          {/* Bespoke-Styled React Bits <CallChip /> */}
          <div className="mb-8 p-4 bg-white border-2 border-black shadow-[4px_4px_0px_#000000] space-y-3">
            <div className="flex items-center justify-between border-b border-black/10 pb-2">
              <span className="font-nikkei text-xs uppercase tracking-wider text-black flex items-center gap-2 font-bold">
                <span className="w-2 h-2 rounded-full bg-[#B91C1C]" />
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

          {/* 3D Interactive Topology & Signal Flow Diagram (Framer / MotionSites Style) */}
          <div className="mb-8">
            <InteractiveTierDiagram />
          </div>

          {/* Arbitrage Engine: ArbitrageCalculator */}
          <div className="border-2 border-black rounded-lg overflow-hidden shadow-[6px_6px_0px_#000000] bg-[#101116]">
            <ArbitrageCalculator />
          </div>
        </div>
      </ParallaxCard>


      {/* 
        ========================================================================
        FEATURE 03: 24/7 WIN32 KEEPALIVE SHIELD & PROCESS RESURRECTION
        ========================================================================
      */}
      <ParallaxCard index={2} id="keepalive">
        <div className="comic-plate relative w-full p-6 sm:p-10">
          <div className="mb-8 pt-2">
            <div className="inline-block bg-black text-[#FBF9F5] font-nikkei text-xs uppercase px-3 py-1 tracking-widest mb-3 shadow-[2px_2px_0px_#B91C1C]">
              FEATURE 03 • IMMORTAL HOST DAEMON
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl text-black tracking-tight leading-tight uppercase">
              Runs All Night Without Crashing
            </h2>
            <p className="font-gt-era text-black/75 text-sm sm:text-base max-w-3xl mt-2 leading-relaxed">
              Leaving an AI agent to run overnight shouldn&apos;t end with a frozen terminal. A silent Windows Scheduled Task checks your agent every 5 minutes and automatically restarts it if your computer sleeps, reboots, or crashes.
            </p>
          </div>

          {/* Side-by-Side Comparison Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {/* Card 1: Traditional Vulnerability */}
            <div className="comic-card-red p-6 rounded-lg space-y-3">
              <div className="border-b border-black/10 pb-2">
                <span className="font-nikkei text-xs uppercase tracking-wider text-[#B91C1C] font-extrabold">
                  Traditional Agent Vulnerability
                </span>
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
              <div className="border-b border-black/10 pb-2">
                <span className="font-nikkei text-xs uppercase tracking-wider text-emerald-700 font-extrabold">
                  Aegis Immortal KeepAlive Shield
                </span>
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
                <Check className="w-6 h-6 stroke-[3]" />
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
        </div>
      </ParallaxCard>


      {/* 
        ========================================================================
        FEATURE 04: DETERMINISTIC MOBILE TELEGRAM TELEMETRY & WHISPER SHIELD
        ========================================================================
      */}
      <ParallaxCard index={3} id="mobile">
        <div className="comic-plate relative w-full p-6 sm:p-10">
          <div className="mb-8 pt-2">
            <div className="inline-block bg-black text-[#FBF9F5] font-nikkei text-xs uppercase px-3 py-1 tracking-widest mb-3 shadow-[2px_2px_0px_#B91C1C]">
              FEATURE 04 • MOBILE TELEGRAM TELEMETRY
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl text-black tracking-tight leading-tight uppercase">
              Control Your Agent From Your Phone
            </h2>
            <p className="font-gt-era text-black/75 text-sm sm:text-base max-w-3xl mt-2 leading-relaxed">
              Step away from your desk without losing control. Send voice notes, review code diffs, and get notified the second tests pass—directly through Telegram while your desktop does the heavy lifting.
            </p>
          </div>

          {/* Telegram Simulator: TelegramSimulator with authentic iPhone 16 Pro iOS */}
          <div className="border-2 border-black rounded-lg overflow-hidden shadow-[6px_6px_0px_#000000] bg-[#101116] p-4 sm:p-6">
            <TelegramSimulator />
          </div>
        </div>
      </ParallaxCard>

      {/* 
        ========================================================================
        FEATURE 05: 4-DECISION QUALITY ARCHITECTURE GATE & AUTONOMOUS LEARNING LOOP
        ========================================================================
      */}
      <ParallaxCard index={4} id="quality">
        <div className="comic-plate relative w-full p-6 sm:p-10">
          <div className="mb-8 pt-2">
            <div className="inline-block bg-black text-[#FBF9F5] font-nikkei text-xs uppercase px-3 py-1 tracking-widest mb-3 shadow-[2px_2px_0px_#B91C1C]">
              FEATURE 05 • PRODUCTION SAFETY GATE
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl text-black tracking-tight leading-tight uppercase">
              Catch Bad Code Before It Hits Git
            </h2>
            <p className="font-gt-era text-black/75 text-sm sm:text-base max-w-3xl mt-2 leading-relaxed">
              Local models are free, but they can make silly mistakes. Instead of throwing them away, our 4-stage filter strips AI apologies, blocks vulnerabilities, and tests every line in a sandbox until zero bugs remain.
            </p>
          </div>

          {/* Quality Gates: QualityGateCards */}
          <div className="border-2 border-black rounded-lg overflow-hidden shadow-[6px_6px_0px_#000000] bg-[#101116]">
            <QualityGateCards />
          </div>
        </div>
      </ParallaxCard>

      {/* 
        ========================================================================
        FEATURE 06: MASTER ARCHITECTURAL BLUEPRINTS GALLERY
        ========================================================================
      */}
      <ParallaxCard index={5} id="blueprints">
        <div className="comic-plate relative w-full p-6 sm:p-10">
          <div className="mb-8 pt-2">
            <div className="font-nikkei text-xs uppercase text-[#B91C1C] font-extrabold tracking-widest mb-2">
              FEATURE 06 // SYSTEM BLUEPRINTS
            </div>
            <h2 className="font-charles-rosie text-4xl sm:text-5xl text-black tracking-tight leading-tight uppercase">
              The 7 Core System Blueprints
            </h2>
            <p className="font-gt-era text-black/75 text-sm sm:text-base max-w-3xl mt-2 leading-relaxed">
              Explore step-by-step how AegisBrain connects your terminal, memory database, free local models, and mobile notifications into a single bulletproof system.
            </p>
          </div>

          {/* 7 Interactive Live Architectural Blueprints */}
          <Feature06BlueprintCards className="mb-8" />

          {/* System Diagrams: InfographicsGallery */}
          <div className="border-2 border-black rounded-lg overflow-hidden shadow-[6px_6px_0px_#000000] bg-[#101116]">
            <InfographicsGallery />
          </div>
        </div>
      </ParallaxCard>

      {/* 
        ========================================================================
        FEATURE 07: QUICKSTART & INSTALLATION: ONE-LINE SETUP
        ========================================================================
      */}
      <ParallaxCard index={6} id="install">
        <div className="comic-plate relative w-full p-6 sm:p-10">
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
        </div>
      </ParallaxCard>

      {/* 
        ========================================================================
        COMMUNITY & COMPARISON: OPEN SOURCE HUB + 7-VECTOR ARCHITECTURAL MATRIX
        ========================================================================
      */}
      <ParallaxCard index={7} id="community">
        <div className="comic-plate relative w-full p-8 sm:p-12 text-black">
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
                      <span className="w-2 h-2 rounded-full bg-emerald-600" />
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
          </div>
      </ParallaxCard>

      {/* Luxury Minimal Footer Bottom Bar */}
      <footer className="relative py-12 px-4 sm:px-8 bg-[#070709] border-t border-white/10 text-xs font-gt-era text-white/50 flex flex-col sm:flex-row items-center justify-between gap-4 max-w-5xl mx-auto">
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
      </footer>

      {/* Atmospheric Audio Soundtrack & Sfx Engine */}
      <SoundtrackController
        soundActive={soundActive}
        onToggleSound={setSoundActive}
      />
    </div>
    </CursorPhysicsProvider>
  );
}
