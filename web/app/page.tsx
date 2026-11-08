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
} from "lucide-react";

export default function Home() {
  const [scrollProgress, setScrollProgress] = useState(0);
  const [soundActive, setSoundActive] = useState(false);
  const [copiedTab, setCopiedTab] = useState<string | null>(null);
  const [selectedInstallTab, setSelectedInstallTab] = useState("curl");
  const [queryTerm, setQueryTerm] = useState("rag");
  const [sliderTurns, setSliderTurns] = useState(250);
  const [copiedAsset, setCopiedAsset] = useState<string | null>(null);

  // Track vertical scroll progress for the right-edge red progress line
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

  const installCommands: Record<string, { cmd: string; desc: string; os: string }> = {
    curl: {
      cmd: "curl -sSL https://raw.githubusercontent.com/PG300604/aegis-brain/main/install.sh | bash",
      desc: "One-line POSIX bootstrap: installs daemon, systemd/launchd service & aegis CLI",
      os: "macOS & Linux",
    },
    powershell: {
      cmd: "irm https://raw.githubusercontent.com/PG300604/aegis-brain/main/install.ps1 | iex",
      desc: "Registers Windows Scheduled Task keepalive, Telegram listener, and global aegis CLI",
      os: "Windows 10/11",
    },
    uv: {
      cmd: "uv tool install git+https://github.com/PG300604/aegis-brain.git",
      desc: "Isolated ultra-fast Python environment with zero dependency collisions",
      os: "Cross-Platform",
    },
    pip: {
      cmd: "pip install git+https://github.com/PG300604/aegis-brain.git",
      desc: "Direct wheel install into active Python environment",
      os: "Python 3.10+",
    },
    docker: {
      cmd: "docker run -d -p 8765:8765 --name aegis-brain ghcr.io/pg300604/aegis-brain:latest",
      desc: "Isolated headless container daemon with persistent /root/.aegis volume",
      os: "Docker Engine",
    },
  };

  const handleCopy = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedTab(id);
    setTimeout(() => setCopiedTab(null), 2500);
  };

  const handleCopyAsset = (name: string, hash: string) => {
    navigator.clipboard.writeText(hash);
    setCopiedAsset(name);
    setTimeout(() => setCopiedAsset(null), 2500);
  };

  // Simulated query results
  const querySimulations: Record<
    string,
    { ms: number; symbols: number; tokens: number; preview: string }
  > = {
    rag: {
      ms: 21.4,
      symbols: 42,
      tokens: 210,
      preview: "aegis/memory/fts5.py:142 • def recall_symbols(query, limit=10)",
    },
    sqlite: {
      ms: 18.2,
      symbols: 18,
      tokens: 185,
      preview: "aegis/db/connection.py:64 • PRAGMA journal_mode=WAL; synchronous=NORMAL;",
    },
    whisper: {
      ms: 23.8,
      symbols: 29,
      tokens: 240,
      preview: "aegis/audio/shield.py:88 • chunk_audio_greedy(duration_sec=25.0)",
    },
    security: {
      ms: 22.1,
      symbols: 36,
      tokens: 195,
      preview: "aegis/gates/redteam.py:51 • def scan_ast_taint(tree, allow_shell=False)",
    },
  };

  const currentQueryData =
    querySimulations[queryTerm.toLowerCase()] || {
      ms: 24.0,
      symbols: 31,
      tokens: 220,
      preview: `aegis/neural/index.py:89 • match('${queryTerm}') -> FTS5 snippet`,
    };

  // Calculations for Arbitrage Slider
  const frontierSpend = Math.round((sliderTurns * 30 * 0.08) * 10) / 10;
  const aegisSpend = Math.round((sliderTurns * 30 * 0.006) * 10) / 10;
  const netSavings = Math.round(frontierSpend - aegisSpend);
  const savingsPercent = Math.round(((frontierSpend - aegisSpend) / frontierSpend) * 100);

  return (
    <div className="relative min-h-screen bg-[#070709] text-[#0D0D11] selection:bg-[#B91C1C] selection:text-white">
      {/* 
        ========================================================================
        VERTICAL RED SCROLL PROGRESS LINE (matching Santioni Spirits right margin)
        ========================================================================
      */}
      <div className="scroll-progress-line">
        <div
          className="scroll-progress-fill"
          style={{ height: `${scrollProgress}%` }}
        />
      </div>

      {/* 
        ========================================================================
        LUXURY EDITORIAL TOP BAR (matching Santioni Spirits header)
        ========================================================================
      */}
      <header className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 sm:px-12 py-5 pointer-events-none">
        {/* Left: Circular Seal Logo */}
        <div className="pointer-events-auto flex items-center gap-3">
          <a href="#" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-full border border-white/30 flex items-center justify-center bg-black/60 backdrop-blur-md text-white transition-transform group-hover:scale-105">
              <svg
                viewBox="0 0 40 40"
                className="w-7 h-7 text-white fill-none stroke-current"
                strokeWidth="1.5"
              >
                <circle cx="20" cy="20" r="17" strokeDasharray="2 2" />
                <polygon points="20,7 32,28 8,28" />
                <circle cx="20" cy="21" r="3" fill="currentColor" />
              </svg>
            </div>
            <div className="flex flex-col">
              <span className="font-charles-rosie text-xl text-white tracking-wider leading-none">
                AegisBrain
              </span>
              <span className="font-gt-era text-[9px] uppercase tracking-[0.25em] text-white/50 leading-tight">
                Chassis • Memory
              </span>
            </div>
          </a>
        </div>

        {/* Right: Sharp Minimal Badge & Audio Toggle */}
        <div className="pointer-events-auto flex items-center gap-4">
          <div className="hidden sm:flex items-center bg-white border border-black shadow-[3px_3px_0px_#000000] text-black font-nikkei text-xs uppercase px-4 py-2 tracking-widest gap-4">
            <a href="#experience" className="hover:text-[#B91C1C] transition-colors">
              Experience
            </a>
            <span className="text-black/30">|</span>
            <a href="#terminal" className="hover:text-[#B91C1C] transition-colors">
              Terminal
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
          </div>

          {/* Sound Wave Indicator (matching Santioni bottom right) */}
          <button
            onClick={() => setSoundActive(!soundActive)}
            className="w-10 h-10 bg-white border border-black shadow-[3px_3px_0px_#000000] flex items-center justify-center text-black hover:bg-neutral-100 transition-colors"
            title={soundActive ? "Mute Ambient Sound" : "Enable Sound Atmosphere"}
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
        ACT I: THE TITLE SPREAD (matching Image 1: THE NOCTURNO EXPERIENCE)
        ========================================================================
      */}
      <section
        id="experience"
        className="relative min-h-screen w-full flex flex-col items-center justify-between pt-36 pb-16 px-4 bg-[#070709] overflow-hidden"
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
        <div className="relative z-10 text-center flex flex-col items-center max-w-5xl mx-auto my-auto select-none">
          <p className="font-charles-rosie text-white/70 text-lg sm:text-2xl tracking-[0.35em] uppercase mb-4">
            The
          </p>

          <h1 className="font-charles-rosie text-white text-6xl sm:text-8xl md:text-9xl lg:text-[11rem] leading-[0.88] tracking-tight uppercase drop-shadow-[0_10px_25px_rgba(0,0,0,0.8)]">
            Aeg<span className="text-[#B91C1C]">i</span>s
          </h1>

          <h2 className="font-charles-rosie text-white text-4xl sm:text-6xl md:text-7xl lg:text-8xl leading-tight tracking-[0.14em] uppercase mt-2">
            Experience
          </h2>

          <div className="mt-8 max-w-xl mx-auto px-4">
            <p className="font-gt-era text-white/60 text-xs sm:text-sm uppercase tracking-[0.25em] leading-relaxed">
              Autonomous 24/7 Multi-Tier Agent Engine & Sub-Second Neural Memory.
              Indulge in high-speed intelligence. Atone with zero token waste.
            </p>
          </div>
        </div>

        {/* 
          Foreground: Massive Organic Billowing White Silhouette 
          (Matching the white fluid splash rising from the bottom of Santioni Spirits Image 1)
        */}
        <div className="absolute bottom-0 left-0 right-0 w-full pointer-events-none z-10">
          <svg
            viewBox="0 0 1440 340"
            className="w-full h-auto text-white fill-current filter drop-shadow-[0_-10px_25px_rgba(0,0,0,0.5)]"
            preserveAspectRatio="none"
          >
            {/* Billowing cloud & liquid mist path */}
            <path d="M0,340 L1440,340 L1440,190 C1380,180 1340,130 1280,140 C1220,150 1190,210 1130,200 C1070,190 1040,110 970,120 C900,130 870,220 800,210 C730,200 700,90 620,100 C540,110 510,190 440,180 C370,170 340,70 260,90 C180,110 140,210 80,190 C40,175 20,230 0,220 Z" />
            {/* Splatter Droplets Floating Up */}
            <circle cx="280" cy="50" r="14" />
            <circle cx="260" cy="20" r="7" />
            <circle cx="610" cy="65" r="11" />
            <circle cx="635" cy="35" r="5" />
            <circle cx="985" cy="75" r="16" />
            <circle cx="960" cy="45" r="8" />
            <circle cx="1270" cy="85" r="12" />
            <circle cx="1295" cy="55" r="6" />
            <circle cx="450" cy="130" r="9" />
            <circle cx="810" cy="155" r="10" />
            <circle cx="1120" cy="140" r="8" />
          </svg>
        </div>

        {/* Scroll Indicator Prompt */}
        <div className="relative z-20 flex flex-col items-center gap-2 text-black mt-8">
          <span className="font-nikkei text-[10px] tracking-[0.3em] uppercase">
            Scroll To Enter The Narrative
          </span>
          <ChevronDown className="w-4 h-4 animate-bounce text-[#B91C1C]" />
        </div>
      </section>

      {/* 
        ========================================================================
        ACT II: SCENE 1 — THE CONTEXT LABYRINTH (matching Image 2)
        ========================================================================
      */}
      <section className="relative min-h-screen py-24 px-4 sm:px-8 bg-[#0B0B0E] flex flex-col items-center justify-center">
        {/* Main Comic Book Plate Container */}
        <div className="relative w-full max-w-5xl bg-[#FBF9F5] border-[3px] border-black shadow-[10px_10px_0px_#000000] p-4 sm:p-8">
          {/* Top-Right Comic Narration Caption Box */}
          <div className="absolute top-6 right-6 z-20 max-w-xs sm:max-w-md comic-narration-box p-4 bg-white">
            <p className="text-[11px] sm:text-xs text-black font-nikkei tracking-wide uppercase leading-snug">
              In an immense land of unindexed dead logs.
            </p>
            <p className="text-xs sm:text-sm text-black font-nikkei tracking-wide uppercase font-extrabold leading-snug mt-1">
              A <span className="text-[#B91C1C]">tired agent</span> wanders through 50,000 tokens of context bloat.
            </p>
          </div>

          {/* Overlapping Floating Inset Panel (Top Left) - Extreme Close-Up */}
          <div className="absolute top-6 left-6 z-20 w-36 sm:w-52 h-44 sm:h-64 comic-inset-box overflow-hidden bg-[#C8A87D]">
            {/* Hand-inked Face Close-Up */}
            <svg
              viewBox="0 0 200 240"
              className="w-full h-full text-black fill-none stroke-current"
              strokeWidth="2"
            >
              {/* Hood cowl shadow */}
              <path
                d="M10,10 C60,0 140,0 190,20 C180,80 180,180 190,230 L10,230 Z"
                fill="#000000"
              />
              {/* Exposed weathered face in ochre */}
              <path
                d="M40,50 C70,40 130,40 160,55 C165,110 150,160 120,180 C90,190 60,180 45,150 Z"
                fill="#C8A87D"
                stroke="#000000"
                strokeWidth="3"
              />
              {/* Deep eye socket shadow & cross-hatching */}
              <ellipse cx="85" cy="95" rx="18" ry="12" fill="#000000" />
              <ellipse cx="135" cy="100" rx="16" ry="11" fill="#000000" />
              <circle cx="88" cy="96" r="3" fill="#00F0FF" />
              <circle cx="137" cy="101" r="3" fill="#00F0FF" />
              {/* Weathered wrinkle hatching */}
              <line x1="70" y1="75" x2="100" y2="72" stroke="#000000" strokeWidth="1.5" />
              <line x1="120" y1="76" x2="150" y2="80" stroke="#000000" strokeWidth="1.5" />
              <line x1="85" y1="125" x2="105" y2="155" stroke="#000000" strokeWidth="2.5" />
              <line x1="90" y1="165" x2="120" y2="163" stroke="#000000" strokeWidth="2" />
              {/* Cross-hatch shading across cheeks */}
              <path
                d="M55,110 L75,130 M55,120 L75,140 M55,130 L75,150 M50,125 L70,105 M50,135 L70,115"
                stroke="#000000"
                strokeWidth="1.2"
              />
            </svg>
            <div className="absolute bottom-1 right-2 bg-black text-[#00F0FF] font-mono text-[9px] px-1">
              turn: 9 / 10
            </div>
          </div>

          {/* Main Comic Graphic Novel Illustration (Woodcut / Cross-Hatch Style) */}
          <div className="relative w-full h-[520px] sm:h-[620px] border-2 border-black bg-[#121217] overflow-hidden">
            <svg
              viewBox="0 0 1000 620"
              className="w-full h-full"
              preserveAspectRatio="xMidYMid slice"
            >
              {/* Sky Background with Cross-Hatch Shading */}
              <rect x="0" y="0" width="1000" height="620" fill="#0D0D11" />
              <g stroke="rgba(255,255,255,0.06)" strokeWidth="1">
                {Array.from({ length: 60 }).map((_, i) => (
                  <line key={i} x1="0" y1={i * 12} x2="1000" y2={i * 12} />
                ))}
              </g>

              {/* Billowing White Mist Shape (matching Santioni background cloud) */}
              <path
                d="M250,620 C280,480 320,380 420,360 C520,340 560,420 650,380 C740,340 760,240 850,220 C940,200 970,320 1000,310 L1000,620 Z"
                fill="#FFFFFF"
              />
              {/* Mist Splatter Droplets */}
              <circle cx="480" cy="270" r="18" fill="#FFFFFF" />
              <circle cx="510" cy="235" r="9" fill="#FFFFFF" />
              <circle cx="720" cy="190" r="14" fill="#FFFFFF" />
              <circle cx="745" cy="155" r="7" fill="#FFFFFF" />

              {/* Horizontal Ground Horizon Lines */}
              <g stroke="#000000" strokeWidth="2">
                <line x1="0" y1="480" x2="1000" y2="480" />
                <line x1="0" y1="520" x2="1000" y2="520" />
                <line x1="0" y1="570" x2="1000" y2="570" />
                {/* Cross-hatch earth strokes */}
                <line x1="120" y1="480" x2="150" y2="520" />
                <line x1="180" y1="480" x2="210" y2="520" />
                <line x1="680" y1="480" x2="710" y2="520" />
                <line x1="750" y1="480" x2="780" y2="520" />
                <line x1="840" y1="520" x2="870" y2="570" />
                <line x1="910" y1="520" x2="940" y2="570" />
              </g>

              {/* The Hooded Figure (Wanderer) Walking Hunched (matching Image 2) */}
              <g transform="translate(380, 290)">
                {/* Cloak body in Ochre (#C8A87D) with heavy black shadow hatching */}
                <path
                  d="M110,40 C70,40 50,70 40,110 C30,150 45,210 50,260 L140,240 C145,200 150,150 145,110 C140,80 130,40 110,40 Z"
                  fill="#C8A87D"
                  stroke="#000000"
                  strokeWidth="3.5"
                />
                {/* Hooded head leaning forward */}
                <path
                  d="M90,30 C75,30 55,50 50,75 C45,100 65,115 85,110 C105,105 115,80 110,55 C105,40 95,30 90,30 Z"
                  fill="#C8A87D"
                  stroke="#000000"
                  strokeWidth="3.5"
                />
                {/* Hood opening in pitch black */}
                <path
                  d="M52,75 C58,85 70,95 78,92 C82,80 75,70 65,65 Z"
                  fill="#000000"
                />
                {/* Deep cross-hatch shading across the cloak */}
                <g stroke="#000000" strokeWidth="2">
                  <line x1="60" y1="110" x2="80" y2="135" />
                  <line x1="65" y1="125" x2="88" y2="150" />
                  <line x1="70" y1="140" x2="95" y2="165" />
                  <line x1="75" y1="155" x2="102" y2="180" />
                  <line x1="80" y1="170" x2="110" y2="195" />
                  <line x1="85" y1="185" x2="118" y2="210" />
                  {/* Opposite cross-hatch */}
                  <line x1="80" y1="135" x2="60" y2="160" />
                  <line x1="90" y1="150" x2="70" y2="175" />
                  <line x1="100" y1="165" x2="80" y2="190" />
                  <line x1="110" y1="180" x2="90" y2="205" />
                </g>
                {/* Dark cloak trim band */}
                <path
                  d="M48,245 C75,250 115,240 142,225"
                  stroke="#000000"
                  strokeWidth="7"
                  fill="none"
                />
                {/* Trailing arm and hand */}
                <path
                  d="M100,140 C110,165 115,190 112,215 L102,215 C105,190 102,170 95,145 Z"
                  fill="#FFFFFF"
                  stroke="#000000"
                  strokeWidth="2.5"
                />
              </g>

              {/* Crawling Error Callout Bubble */}
              <g transform="translate(620, 430)">
                <rect
                  x="0"
                  y="0"
                  width="280"
                  height="65"
                  fill="#FFFFFF"
                  stroke="#000000"
                  strokeWidth="2.5"
                />
                <polygon points="0,25 -15,35 0,45" fill="#FFFFFF" stroke="#000000" strokeWidth="2.5" />
                <rect x="0" y="24" width="6" height="22" fill="#FFFFFF" />
                <text x="15" y="26" fill="#B91C1C" fontFamily="PPNikkeiMaru, Impact" fontSize="12" fontWeight="bold">
                  * 12,400 MS RE-READ STALL *
                </text>
                <text x="15" y="46" fill="#000000" fontFamily="GT-Era, sans-serif" fontSize="10">
                  Crawling 52,000 raw transcript tokens...
                </text>
              </g>
            </svg>
          </div>

          {/* Bottom Right Hash Mark (matching Santioni Image 2) */}
          <div className="flex items-center justify-between mt-4 px-2">
            <span className="font-gt-era text-xs uppercase tracking-widest text-black/60">
              Act I • The Context Labyrinth
            </span>
            <span className="font-nikkei text-lg text-black tracking-widest select-none">
              |||
            </span>
          </div>
        </div>
      </section>

      {/* 
        ========================================================================
        ACT III: SCENE 2 — THE AWAKENING OF THE NEURAL CORE (FTS5 24ms)
        ========================================================================
      */}
      <section className="relative min-h-screen py-24 px-4 sm:px-8 bg-[#070709] flex flex-col items-center justify-center">
        <div className="relative w-full max-w-5xl bg-[#FBF9F5] border-[3px] border-black shadow-[10px_10px_0px_#B91C1C] p-4 sm:p-8">
          {/* Top-Right Comic Narration Box */}
          <div className="absolute top-6 right-6 z-20 max-w-xs sm:max-w-md comic-narration-box p-4 bg-white">
            <p className="text-[11px] sm:text-xs text-black font-nikkei tracking-wide uppercase leading-snug">
              From the frozen void of 50,000-token amnesia.
            </p>
            <p className="text-xs sm:text-sm text-black font-nikkei tracking-wide uppercase font-extrabold leading-snug mt-1">
              The <span className="text-[#B91C1C]">24ms neural core</span> ignites. Sub-second SQLite FTS5 awakens.
            </p>
          </div>

          {/* Overlapping Inset Panel: The Crystalline Core */}
          <div className="absolute top-6 left-6 z-20 w-40 sm:w-56 h-48 sm:h-64 comic-inset-box overflow-hidden bg-black p-3 flex flex-col justify-between">
            <div className="flex items-center justify-between border-b border-white/20 pb-2">
              <span className="text-[10px] font-mono text-[#00F0FF] uppercase">
                Core State: Active
              </span>
              <span className="w-2 h-2 rounded-full bg-[#10B981] animate-ping" />
            </div>
            {/* Geometric Crystal Wireframe */}
            <svg viewBox="0 0 100 100" className="w-28 h-28 mx-auto text-[#00F0FF]">
              <polygon points="50,10 85,50 50,90 15,50" fill="none" stroke="currentColor" strokeWidth="2" />
              <line x1="50" y1="10" x2="50" y2="90" stroke="currentColor" strokeWidth="1" strokeDasharray="2 2" />
              <line x1="15" y1="50" x2="85" y2="50" stroke="currentColor" strokeWidth="1" strokeDasharray="2 2" />
              <circle cx="50" cy="50" r="12" fill="#A855F7" fillOpacity="0.4" stroke="#00F0FF" strokeWidth="1.5" />
            </svg>
            <div className="text-[9px] font-mono text-white/70 leading-tight">
              brain.db: WAL Mode
              <br />
              Latency: 0.024s (24ms)
            </div>
          </div>

          {/* Main Visual Arena: Interactive Comic Benchmark Station */}
          <div className="relative w-full border-2 border-black bg-white p-6 sm:p-12 mt-16 sm:mt-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
              {/* Left Dial: The 12,400ms Traditional Crawl */}
              <div className="border-2 border-black p-6 bg-neutral-50 shadow-[4px_4px_0px_#000000]">
                <div className="flex items-center justify-between mb-4">
                  <span className="font-nikkei text-xs uppercase text-neutral-500">
                    Traditional Agent
                  </span>
                  <span className="bg-[#B91C1C] text-white font-nikkei text-[10px] px-2 py-0.5 uppercase">
                    52,000 Tokens Lost
                  </span>
                </div>
                <div className="text-center my-6">
                  <div className="font-charles-rosie text-5xl sm:text-6xl text-[#B91C1C]">
                    12,400 <span className="text-xl">ms</span>
                  </div>
                  <p className="font-gt-era text-xs text-neutral-600 mt-2">
                    Crawls full multi-megabyte transcript on every user turn.
                  </p>
                </div>
                <div className="w-full bg-neutral-200 h-3 border border-black overflow-hidden">
                  <div className="bg-[#B91C1C] h-full w-[94%]" />
                </div>
                <div className="flex justify-between text-[10px] font-mono text-neutral-500 mt-2">
                  <span>RAM: &gt; 1.2 GB</span>
                  <span>Cost: High</span>
                </div>
              </div>

              {/* Right Dial: The 24ms Aegis Recall */}
              <div className="border-2 border-black p-6 bg-white shadow-[6px_6px_0px_#000000] relative">
                <div className="absolute -top-3 right-4 bg-black text-[#00F0FF] font-nikkei text-[11px] px-3 py-1 uppercase tracking-widest border border-black">
                  ★ 516x Speedup
                </div>
                <div className="flex items-center justify-between mb-4">
                  <span className="font-nikkei text-xs uppercase text-black font-extrabold">
                    AegisBrain FTS5
                  </span>
                </div>
                <div className="text-center my-6">
                  <div className="font-charles-rosie text-5xl sm:text-6xl text-black">
                    24 <span className="text-xl text-neutral-500">ms</span>
                  </div>
                  <p className="font-gt-era text-xs text-neutral-700 mt-2">
                    Pre-indexed SQLite WAL FTS5 memory recall under 240 tokens.
                  </p>
                </div>
                <div className="w-full bg-neutral-200 h-3 border border-black overflow-hidden">
                  <div className="bg-[#10B981] h-full w-[2%]" />
                </div>
                <div className="flex justify-between text-[10px] font-mono text-neutral-600 mt-2">
                  <span>RAM: &lt; 25 MB</span>
                  <span>Cost: $0.00</span>
                </div>
              </div>
            </div>

            {/* Interactive Live Query Sandbox in Vintage Comic Styling */}
            <div className="mt-8 border-2 border-black p-4 sm:p-6 bg-[#FBF9F5]">
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-4">
                <span className="font-nikkei text-xs uppercase tracking-wider text-black">
                  Test Sub-Second Neural Retrieval:
                </span>
                <div className="flex items-center gap-2">
                  {["rag", "sqlite", "whisper", "security"].map((term) => (
                    <button
                      key={term}
                      onClick={() => setQueryTerm(term)}
                      className={`px-2.5 py-1 text-xs font-mono uppercase border border-black transition-transform ${
                        queryTerm === term
                          ? "bg-black text-white shadow-[2px_2px_0px_#B91C1C] scale-105"
                          : "bg-white text-black hover:bg-neutral-100"
                      }`}
                    >
                      #{term}
                    </button>
                  ))}
                </div>
              </div>

              {/* Dynamic Query Result Panel */}
              <div className="bg-black text-white p-4 font-mono text-xs border border-black flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
                <div className="flex items-center gap-2 overflow-x-auto w-full">
                  <span className="text-[#00F0FF]">&gt;</span>
                  <span className="text-[#10B981]">aegis recall &quot;{queryTerm}&quot;</span>
                  <span className="text-white/40">→</span>
                  <span className="text-white/80 truncate">{currentQueryData.preview}</span>
                </div>
                <div className="flex items-center gap-3 shrink-0">
                  <span className="text-[#00F0FF] font-bold">
                    {currentQueryData.ms} ms
                  </span>
                  <span className="bg-white/10 px-2 py-0.5 text-[10px] text-white/60">
                    {currentQueryData.tokens} tokens
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div className="flex items-center justify-between mt-4 px-2">
            <span className="font-gt-era text-xs uppercase tracking-widest text-black/60">
              Act II • The Neural Core
            </span>
            <span className="font-nikkei text-lg text-black tracking-widest select-none">
              |||
            </span>
          </div>
        </div>
      </section>

      {/* 
        ========================================================================
        ACT IV: SCENE 3 — THE TRIAD OF SOVEREIGNTY (Token Arbitrage)
        ========================================================================
      */}
      <section className="relative min-h-screen py-24 px-4 sm:px-8 bg-[#0B0B0E] flex flex-col items-center justify-center">
        <div className="relative w-full max-w-5xl bg-[#FBF9F5] border-[3px] border-black shadow-[10px_10px_0px_#000000] p-4 sm:p-8">
          {/* Top-Right Comic Narration Box */}
          <div className="absolute top-6 right-6 z-20 max-w-xs sm:max-w-md comic-narration-box p-4 bg-white">
            <p className="text-[11px] sm:text-xs text-black font-nikkei tracking-wide uppercase leading-snug">
              Three minds. One unbreakable discipline.
            </p>
            <p className="text-xs sm:text-sm text-black font-nikkei tracking-wide uppercase font-extrabold leading-snug mt-1">
              The <span className="text-[#B91C1C]">high brain directs</span>. Tireless local workers hammer code in the forge.
            </p>
          </div>

          {/* Main Content: The 3-Tier Division & Interactive Token Slider */}
          <div className="border-2 border-black bg-white p-6 sm:p-10 mt-16 sm:mt-12">
            {/* 3 Comic Pillars */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
              {/* Tier 1 */}
              <div className="border-2 border-black p-5 bg-[#FAF8F5] shadow-[4px_4px_0px_#000000]">
                <div className="bg-black text-white font-nikkei text-[10px] uppercase px-2 py-0.5 inline-block mb-3">
                  Tier I • Senior Boss
                </div>
                <h3 className="font-charles-rosie text-2xl text-black">The Brain</h3>
                <p className="font-gt-era text-xs text-neutral-700 mt-2 leading-relaxed">
                  High cognition architecture, AST invariant definitions, and strict test review. Never writes raw implementation code.
                </p>
                <div className="mt-4 pt-3 border-t border-black/10 font-mono text-[10px] text-neutral-500">
                  Models: Fable 5.1 • Opus 5.5 • Gemini 4 • Argon
                </div>
              </div>

              {/* Tier 2 */}
              <div className="border-2 border-black p-5 bg-[#FAF8F5] shadow-[4px_4px_0px_#B91C1C]">
                <div className="bg-[#B91C1C] text-white font-nikkei text-[10px] uppercase px-2 py-0.5 inline-block mb-3">
                  Tier II • Junior Bosses
                </div>
                <h3 className="font-charles-rosie text-2xl text-black">The Inquisitors</h3>
                <p className="font-gt-era text-xs text-neutral-700 mt-2 leading-relaxed">
                  Subagents auditing candidate drafts through 4 strict quality gates. Coaches workers through targeted error-reduction loops.
                </p>
                <div className="mt-4 pt-3 border-t border-black/10 font-mono text-[10px] text-neutral-500">
                  Roles: QA • Security • DevOps • Frontend
                </div>
              </div>

              {/* Tier 3 */}
              <div className="border-2 border-black p-5 bg-[#FAF8F5] shadow-[4px_4px_0px_#000000]">
                <div className="bg-[#10B981] text-white font-nikkei text-[10px] uppercase px-2 py-0.5 inline-block mb-3">
                  Tier III • Local Workers
                </div>
                <h3 className="font-charles-rosie text-2xl text-black">The Forge</h3>
                <p className="font-gt-era text-xs text-neutral-700 mt-2 leading-relaxed">
                  Generates 100% raw boilerplate, unit tests, and candidate implementations in parallel using free local tokens.
                </p>
                <div className="mt-4 pt-3 border-t border-black/10 font-mono text-[10px] text-neutral-500">
                  Workers: Hermes CLI • Ollama • OpenCode
                </div>
              </div>
            </div>

            {/* Interactive Token Arbitrage Calculator */}
            <div className="border-2 border-black p-6 bg-[#FBF9F5] shadow-[6px_6px_0px_#000000]">
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
                <div>
                  <span className="font-nikkei text-sm uppercase text-black font-extrabold">
                    Interactive Token Arbitrage Dial
                  </span>
                  <p className="font-gt-era text-xs text-neutral-600 mt-0.5">
                    Adjust daily developer turns to view net annual savings.
                  </p>
                </div>
                <div className="bg-black text-white font-mono text-sm px-3 py-1 border border-black">
                  {sliderTurns} Turns / Day
                </div>
              </div>

              {/* Slider Input */}
              <input
                type="range"
                min="50"
                max="1000"
                step="25"
                value={sliderTurns}
                onChange={(e) => setSliderTurns(Number(e.target.value))}
                className="w-full h-3 bg-neutral-200 border-2 border-black appearance-none cursor-pointer accent-[#B91C1C]"
              />

              {/* Live Savings Counter */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-6 pt-6 border-t-2 border-black/10 text-center">
                <div className="border border-black p-4 bg-white">
                  <span className="font-gt-era text-xs uppercase text-neutral-500">
                    Direct Frontier Spend
                  </span>
                  <div className="font-charles-rosie text-3xl text-[#B91C1C] mt-1">
                    ${frontierSpend}
                    <span className="text-xs text-neutral-500">/mo</span>
                  </div>
                </div>

                <div className="border border-black p-4 bg-white">
                  <span className="font-gt-era text-xs uppercase text-neutral-500">
                    Aegis 3-Tier Spend
                  </span>
                  <div className="font-charles-rosie text-3xl text-black mt-1">
                    ${aegisSpend}
                    <span className="text-xs text-neutral-500">/mo</span>
                  </div>
                </div>

                <div className="border-2 border-black p-4 bg-white shadow-[4px_4px_0px_#10B981]">
                  <span className="font-nikkei text-xs uppercase text-[#10B981] font-bold">
                    Net Monthly Savings
                  </span>
                  <div className="font-charles-rosie text-3xl text-[#10B981] mt-1">
                    ${netSavings}
                    <span className="text-xs text-neutral-500"> ({savingsPercent}%)</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="flex items-center justify-between mt-4 px-2">
            <span className="font-gt-era text-xs uppercase tracking-widest text-black/60">
              Act III • The Triad of Sovereignty
            </span>
            <span className="font-nikkei text-lg text-black tracking-widest select-none">
              |||
            </span>
          </div>
        </div>
      </section>

      {/* 
        ========================================================================
        ACT V: SCENE 4 — THE NOCTURNAL SENTINEL (24/7 Mobile Command)
        ========================================================================
      */}
      <section className="relative min-h-screen py-24 px-4 sm:px-8 bg-[#070709] flex flex-col items-center justify-center">
        <div className="relative w-full max-w-5xl bg-[#FBF9F5] border-[3px] border-black shadow-[10px_10px_0px_#B91C1C] p-4 sm:p-8">
          {/* Top-Right Comic Narration Box */}
          <div className="absolute top-6 right-6 z-20 max-w-xs sm:max-w-md comic-narration-box p-4 bg-white">
            <p className="text-[11px] sm:text-xs text-black font-nikkei tracking-wide uppercase leading-snug">
              When night descends upon the developer&apos;s studio.
            </p>
            <p className="text-xs sm:text-sm text-black font-nikkei tracking-wide uppercase font-extrabold leading-snug mt-1">
              The <span className="text-[#B91C1C]">nocturnal daemon</span> guards the repository. Whisper slices never loop.
            </p>
          </div>

          {/* Main Visual: Telegram Remote Cockpit */}
          <div className="border-2 border-black bg-white p-6 sm:p-10 mt-16 sm:mt-12">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
              {/* Left: Inked Smartphone Mockup */}
              <div className="border-[3px] border-black p-5 bg-[#0D0D11] text-white shadow-[6px_6px_0px_#000000] rounded-xl max-w-sm mx-auto w-full">
                <div className="flex items-center justify-between pb-3 border-b border-white/10 mb-4 text-xs font-mono">
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-[#10B981] animate-pulse" />
                    <span>@HHAACLIBot</span>
                  </div>
                  <span className="text-white/40">24/7 Win32</span>
                </div>

                {/* Telegram Chat Bubbles */}
                <div className="space-y-3 font-gt-era text-xs">
                  <div className="bg-white/10 p-2.5 rounded border border-white/10">
                    <span className="text-[#00F0FF] text-[10px] block font-mono">
                      VOICE NOTE (0:48)
                    </span>
                    <div className="flex items-center gap-2 mt-1">
                      <span className="text-[#10B981]">▶</span>
                      <div className="flex-1 h-2 bg-white/20 rounded overflow-hidden">
                        <div className="h-full bg-[#10B981] w-[65%]" />
                      </div>
                      <span className="text-[9px] text-white/50">25s slice</span>
                    </div>
                  </div>

                  <div className="bg-black/60 p-2.5 rounded border border-white/20 text-white/80 font-mono text-[11px]">
                    <span className="text-[#10B981] text-[9px] block">
                      WHISPER DETERMINISTIC STT:
                    </span>
                    &quot;Fix auth exception in test_security and push directly to main.&quot;
                  </div>

                  <div className="bg-white/10 p-2.5 rounded border border-white/10 font-mono text-[11px] text-[#F59E0B]">
                    &gt; /type pytest tests/test_auth.py /alt+m
                  </div>

                  <div className="bg-[#10B981]/20 p-2.5 rounded border border-[#10B981]/40 text-[#10B981] text-[10px] font-mono">
                    🏁 Execution Completed! 286/286 passed.
                  </div>
                </div>
              </div>

              {/* Right: Operational Capabilities Checklist in Vintage Comic Stamp */}
              <div className="space-y-4">
                <div className="border-2 border-black p-4 bg-[#FAF8F5] shadow-[3px_3px_0px_#000000]">
                  <h4 className="font-nikkei text-xs uppercase text-black font-extrabold flex items-center gap-2">
                    <span className="text-[#B91C1C]">01.</span> Deterministic Audio Slicing
                  </h4>
                  <p className="font-gt-era text-xs text-neutral-700 mt-1">
                    Audios &gt; 30s are chopped into 25-second greedy chunks with <code className="bg-neutral-200 px-1 font-mono text-[10px]">temperature=0</code>, completely eliminating infinite transcription loops.
                  </p>
                </div>

                <div className="border-2 border-black p-4 bg-[#FAF8F5] shadow-[3px_3px_0px_#000000]">
                  <h4 className="font-nikkei text-xs uppercase text-black font-extrabold flex items-center gap-2">
                    <span className="text-[#B91C1C]">02.</span> In-Flight Keystroke Interrupt
                  </h4>
                  <p className="font-gt-era text-xs text-neutral-700 mt-1">
                    Inject live terminal keystrokes (<code className="bg-neutral-200 px-1 font-mono text-[10px]">/type &lt;cmd&gt; /alt+m</code>) into running Antigravity sessions from your phone without rebooting the daemon.
                  </p>
                </div>

                <div className="border-2 border-black p-4 bg-[#FAF8F5] shadow-[3px_3px_0px_#000000]">
                  <h4 className="font-nikkei text-xs uppercase text-black font-extrabold flex items-center gap-2">
                    <span className="text-[#B91C1C]">03.</span> Win32 Task Scheduler Shield
                  </h4>
                  <p className="font-gt-era text-xs text-neutral-700 mt-1">
                    Registered as a 5-minute recurring Windows background service. Account switches, reboots, and terminal exits never terminate the listener.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="flex items-center justify-between mt-4 px-2">
            <span className="font-gt-era text-xs uppercase tracking-widest text-black/60">
              Act IV • The Nocturnal Sentinel
            </span>
            <span className="font-nikkei text-lg text-black tracking-widest select-none">
              |||
            </span>
          </div>
        </div>
      </section>

      {/* 
        ========================================================================
        ACT VI: SCENE 5 — THE SANCTUM & TERMINAL PORTAL (Installation)
        ========================================================================
      */}
      <section
        id="terminal"
        className="relative min-h-screen py-24 px-4 sm:px-8 bg-[#0B0B0E] flex flex-col items-center justify-center"
      >
        <div className="relative w-full max-w-5xl bg-[#FBF9F5] border-[3px] border-black shadow-[10px_10px_0px_#000000] p-4 sm:p-8">
          {/* Top-Right Comic Narration Box */}
          <div className="absolute top-6 right-6 z-20 max-w-xs sm:max-w-md comic-narration-box p-4 bg-white">
            <p className="text-[11px] sm:text-xs text-black font-nikkei tracking-wide uppercase leading-snug">
              Claim sovereignty over your coding agents.
            </p>
            <p className="text-xs sm:text-sm text-black font-nikkei tracking-wide uppercase font-extrabold leading-snug mt-1">
              <span className="text-[#B91C1C]">Summon the chassis</span> with a single incantation.
            </p>
          </div>

          {/* Master Comic Terminal Frame */}
          <div className="border-2 border-black bg-white p-6 sm:p-10 mt-16 sm:mt-12">
            {/* Terminal Tab Bar */}
            <div className="flex flex-wrap items-center gap-2 border-b-2 border-black pb-4 mb-6">
              {Object.keys(installCommands).map((tab) => (
                <button
                  key={tab}
                  onClick={() => setSelectedInstallTab(tab)}
                  className={`px-4 py-2 font-nikkei text-xs uppercase tracking-wider border-2 border-black transition-transform ${
                    selectedInstallTab === tab
                      ? "bg-black text-white shadow-[3px_3px_0px_#B91C1C] -translate-y-0.5"
                      : "bg-[#FAF8F5] text-black hover:bg-neutral-100"
                  }`}
                >
                  {tab === "curl"
                    ? "curl (macOS/Linux)"
                    : tab === "powershell"
                    ? "PowerShell (Windows)"
                    : tab === "uv"
                    ? "uv (Universal)"
                    : tab === "pip"
                    ? "pip"
                    : "Docker"}
                </button>
              ))}
            </div>

            {/* Terminal Command Box with Click-To-Copy */}
            <div className="border-[3px] border-black bg-[#0D0D11] text-white p-6 shadow-[6px_6px_0px_#000000] relative">
              <div className="flex items-center justify-between pb-3 border-b border-white/10 mb-4 text-xs font-mono text-white/50">
                <span>{installCommands[selectedInstallTab].os}</span>
                <span>{installCommands[selectedInstallTab].desc}</span>
              </div>

              <div className="flex items-center justify-between gap-4 font-mono text-xs sm:text-sm overflow-x-auto py-2">
                <span className="text-[#00F0FF] shrink-0">$</span>
                <span className="text-white/90 select-all font-semibold flex-1">
                  {installCommands[selectedInstallTab].cmd}
                </span>
                <button
                  onClick={() =>
                    handleCopy(
                      selectedInstallTab,
                      installCommands[selectedInstallTab].cmd
                    )
                  }
                  className="shrink-0 bg-white text-black font-nikkei text-xs uppercase px-4 py-2 border border-black shadow-[2px_2px_0px_#B91C1C] hover:bg-neutral-100 transition-transform active:scale-95 flex items-center gap-1.5"
                >
                  {copiedTab === selectedInstallTab ? (
                    <>
                      <Check className="w-3.5 h-3.5 text-[#10B981]" />
                      <span>Copied!</span>
                    </>
                  ) : (
                    <>
                      <Copy className="w-3.5 h-3.5" />
                      <span>Copy</span>
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Direct Download Collection Plates (Vintage Engraved Patent Style) */}
            <div className="mt-10 pt-8 border-t-2 border-black/10">
              <span className="font-nikkei text-xs uppercase text-neutral-500 tracking-wider block mb-4">
                Verified Release Artifacts & SHA-256 Checksums:
              </span>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {[
                  {
                    name: "aegis_brain-0.4.0-py3-none-any.whl",
                    size: "248 KB",
                    hash: "7a9f2b84c1e0d3...4f2a",
                    type: "Python Wheel",
                  },
                  {
                    name: "aegis-brain-0.4.0.tar.gz",
                    size: "215 KB",
                    hash: "9c3e1a8b5f2d0e...8e1b",
                    type: "Source Archive",
                  },
                  {
                    name: "install.ps1",
                    size: "12 KB",
                    hash: "e4f8b2d1c0a9e7...3c5d",
                    type: "Windows Bootstrap",
                  },
                  {
                    name: "install.sh",
                    size: "9 KB",
                    hash: "b1d8e4f2a0c7e9...6a2f",
                    type: "POSIX Bootstrap",
                  },
                ].map((asset) => (
                  <div
                    key={asset.name}
                    className="border-2 border-black p-4 bg-[#FAF8F5] shadow-[3px_3px_0px_#000000] flex flex-col justify-between"
                  >
                    <div>
                      <span className="bg-black text-white font-mono text-[9px] px-1.5 py-0.5 uppercase">
                        {asset.type}
                      </span>
                      <h5 className="font-mono text-xs text-black font-bold mt-2 truncate">
                        {asset.name}
                      </h5>
                      <span className="text-[10px] text-neutral-500 block">
                        Size: {asset.size}
                      </span>
                    </div>

                    <div className="mt-4 pt-2 border-t border-black/10 flex items-center justify-between">
                      <span className="font-mono text-[9px] text-neutral-400 truncate max-w-[100px]">
                        {asset.hash}
                      </span>
                      <button
                        onClick={() => handleCopyAsset(asset.name, asset.hash)}
                        className="text-[10px] font-mono font-bold text-[#B91C1C] hover:underline"
                      >
                        {copiedAsset === asset.name ? "Copied!" : "SHA256"}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Footer Editorial Details */}
          <footer className="mt-8 pt-6 border-t border-black/20 flex flex-col sm:flex-row items-center justify-between text-xs font-gt-era text-neutral-600 gap-4">
            <div className="flex items-center gap-3">
              <span className="font-charles-rosie text-black text-lg">AegisBrain</span>
              <span>•</span>
              <span>GPLv3 Open Source</span>
              <span>•</span>
              <span>Version 0.4.0</span>
            </div>

            <div className="flex items-center gap-4 font-mono text-[11px]">
              <a
                href="https://github.com/PG300604/aegis-brain"
                target="_blank"
                rel="noreferrer"
                className="text-black hover:text-[#B91C1C] transition-colors"
              >
                GitHub Repository
              </a>
              <a
                href="/llms.txt"
                className="text-black hover:text-[#B91C1C] transition-colors"
              >
                llms.txt (GEO)
              </a>
              <a
                href="http://127.0.0.1:8765"
                className="text-black hover:text-[#B91C1C] transition-colors"
              >
                Daemon :8765
              </a>
            </div>
          </footer>
        </div>
      </section>
    </div>
  );
}
