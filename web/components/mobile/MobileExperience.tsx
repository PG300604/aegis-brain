"use client";

import React, { useState, useCallback } from "react";
import {
  Terminal,
  Copy,
  Check,
  ChevronDown,
  Shield,
  Zap,
  ExternalLink,
  Sparkles,
  TrendingUp,
  CheckCircle2,
  Lock,
  Radio,
  BookOpen,
} from "lucide-react";

interface InstallSnippet {
  id: "curl" | "powershell" | "uv" | "pip";
  label: string;
  command: string;
  desc: string;
}

const INSTALL_OPTIONS: InstallSnippet[] = [
  {
    id: "curl",
    label: "curl (macOS/Linux)",
    command: "curl -fsSL https://aegisbrain.ai/install.sh | bash",
    desc: "One-line automated POSIX installation & background daemon setup",
  },
  {
    id: "powershell",
    label: "PowerShell (Win32)",
    command: "irm https://aegisbrain.ai/install.ps1 | iex",
    desc: "Configures Win32 daemon, scheduled task keepalive & Whisper engine",
  },
  {
    id: "uv",
    label: "uv (Fast Python)",
    command: "uv tool install aegisbrain",
    desc: "Isolated global binary installation via astral-sh/uv",
  },
  {
    id: "pip",
    label: "pip",
    command: "pip install aegisbrain",
    desc: "Standard Python package installation into active virtualenv",
  },
];

interface MetricBadge {
  value: string;
  label: string;
  subtext: string;
  glowClass: string;
  icon: React.ElementType;
}

const METRICS: MetricBadge[] = [
  {
    value: "24ms",
    label: "Sub-Second Recall",
    subtext: "FTS5 vector memory",
    glowClass: "text-[#00F0FF] border-[#00F0FF]/30 bg-[#00F0FF]/5",
    icon: Zap,
  },
  {
    value: "$1,840/mo",
    label: "Token Arbitrage",
    subtext: "Tier 3 worker offload",
    glowClass: "text-[#10B981] border-[#10B981]/30 bg-[#10B981]/5",
    icon: TrendingUp,
  },
  {
    value: "Win32",
    label: "Whisper Shield",
    subtext: "24/7 background daemon",
    glowClass: "text-[#A855F7] border-[#A855F7]/30 bg-[#A855F7]/5",
    icon: Shield,
  },
  {
    value: "4 Gates",
    label: "Quality Guard",
    subtext: "AST security & simplicity",
    glowClass: "text-[#F59E0B] border-[#F59E0B]/30 bg-[#F59E0B]/5",
    icon: CheckCircle2,
  },
];

interface ActItem {
  id: string;
  title: string;
  tag: string;
  summary: string;
  highlights: string[];
  icon: React.ElementType;
}

const ACTS: ActItem[] = [
  {
    id: "act-1",
    title: "Act I: Neural Monolith & Context Memory",
    tag: "Sub-Second FTS5",
    summary:
      "Instant neural retrieval across months of multi-agent development sessions. Bootstraps fresh reasoning contexts in ≤ 400 tokens with zero hallucinated state drift.",
    highlights: [
      "Sub-24ms SQLite WAL memory queries",
      "Dynamic session snapshot & restore points",
      "Zero crawler token waste on session logs",
    ],
    icon: Sparkles,
  },
  {
    id: "act-2",
    title: "Act II: 3-Tier Multi-Agent Token Arbitrage",
    tag: "Zero Token Waste",
    summary:
      "The Frontier Brain acts strictly as Senior Architect. Implementation boilerplate, large tests, and repetitive tasks are offloaded to free local Tier 3 workers.",
    highlights: [
      "Hermes / Ollama / Qwen execution workers",
      "Autonomous coaching loops with error feedback",
      "Saves up to $1,840/mo in frontier tokens",
    ],
    icon: Zap,
  },
  {
    id: "act-3",
    title: "Act III: Zero-Leak Red-Team Security Shield",
    tag: "Continuous Audit",
    summary:
      "Every generated line of candidate code passes through strict AST syntax security gates, blocking dangerous shell executions, credential leakage, and path traversals.",
    highlights: [
      "Blocks shell=True and raw os.system calls",
      "Dual-environment sandbox verification",
      "Integrated GitGuardian secret scanning",
    ],
    icon: Lock,
  },
  {
    id: "act-4",
    title: "Act IV: 24/7 Win32 Whisper Daemon & Telegram",
    tag: "Autonomous Ops",
    summary:
      "A permanent background server backed by Windows Task Scheduler. Receives voice memos, transcribes audio locally with Whisper, and accepts remote Telegram commands.",
    highlights: [
      "Win32 self-resurrecting Scheduled Task",
      "Local Whisper speech-to-code pipeline",
      "In-flight /type and /btw remote controls",
    ],
    icon: Radio,
  },
];

export default function MobileExperience() {
  const [activePlatform, setActivePlatform] = useState<InstallSnippet["id"]>("curl");
  const [copied, setCopied] = useState(false);
  const [openAct, setOpenAct] = useState<string>("act-1");

  const currentSnippet =
    INSTALL_OPTIONS.find((opt) => opt.id === activePlatform) || INSTALL_OPTIONS[0];

  const handleCopy = useCallback(() => {
    if (typeof navigator !== "undefined" && navigator.clipboard) {
      navigator.clipboard
        .writeText(currentSnippet.command)
        .then(() => {
          setCopied(true);
          setTimeout(() => setCopied(false), 2400);
        })
        .catch(() => {
          // Fallback
          setCopied(true);
          setTimeout(() => setCopied(false), 2400);
        });
    }
  }, [currentSnippet.command]);

  const scrollToInstall = () => {
    const el = document.getElementById("mobile-install-card");
    if (el) {
      el.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <div className="block md:hidden w-full min-h-screen bg-[#030305] text-[#E2E8F0] px-4 pt-6 pb-28 relative font-sans overflow-x-hidden selection:bg-[#00F0FF]/20 selection:text-[#00F0FF]">
      {/* Background Ambience & Grid Accent */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-80 h-80 bg-[#00F0FF]/10 blur-[90px] pointer-events-none rounded-full" />
      <div className="absolute top-96 right-0 w-64 h-64 bg-[#A855F7]/10 blur-[80px] pointer-events-none rounded-full" />

      {/* Header Badge */}
      <header className="relative z-10 flex flex-col items-center text-center mb-6">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[#00F0FF]/30 bg-[#00F0FF]/10 text-[#00F0FF] text-[11px] font-mono tracking-wider uppercase mb-3 shadow-[0_0_15px_rgba(0,240,255,0.25)]">
          <span className="w-1.5 h-1.5 rounded-full bg-[#00F0FF] animate-pulse" />
          AegisBrain v2.4 • Autonomous OS
        </div>
        <h1 className="text-3xl font-extrabold tracking-tight text-white mb-2">
          Autonomous Coding <br />
          <span className="bg-gradient-to-r from-[#00F0FF] via-[#A855F7] to-[#00E5FF] bg-clip-text text-transparent">
            Without Token Waste
          </span>
        </h1>
        <p className="text-xs text-[#94A3B8] max-w-xs leading-relaxed">
          The autonomous brain orchestrating subagents, 24/7 background daemons, and sub-second neural memory.
        </p>
      </header>

      {/* 2.5D CSS GPU-Accelerated Obsidian Monolith Crystal */}
      <section className="relative z-10 my-8 flex flex-col items-center justify-center">
        <div className="relative w-44 h-52 flex items-center justify-center perspective-[1000px]">
          {/* Cyan Backglow Aura */}
          <div className="absolute w-36 h-36 rounded-full bg-gradient-to-tr from-[#00F0FF]/35 to-[#A855F7]/35 blur-2xl animate-pulse" />

          {/* 3D Rotating Crystal Wrapper */}
          <div
            className="monolith-mobile-anim relative w-28 h-40 transform-style-preserve-3d"
            style={{ transformStyle: "preserve-3d" }}
          >
            {/* Front Obsidian Facet */}
            <div className="absolute inset-0 bg-gradient-to-b from-[#11131E] via-[#050508] to-[#020204] border border-[#00F0FF]/50 shadow-[0_0_25px_rgba(0,240,255,0.35)] clip-polygon-diamond backdrop-blur-md flex items-center justify-center">
              <div className="w-8 h-8 rounded-full bg-[#A855F7]/30 blur-sm animate-ping" />
              <div className="w-4 h-4 rounded-full bg-[#00F0FF] shadow-[0_0_15px_#00F0FF]" />
            </div>

            {/* Cyan Wireframe Neon Accent Lines */}
            <div
              className="absolute -inset-1 border border-[#00F0FF]/40 rounded-lg pointer-events-none"
              style={{ transform: "rotateZ(45deg) scale(0.85)" }}
            />
            <div
              className="absolute -inset-1 border border-[#A855F7]/30 rounded-lg pointer-events-none"
              style={{ transform: "rotateZ(-45deg) scale(0.85)" }}
            />
          </div>
        </div>

        <div className="mt-2 text-center">
          <span className="text-[10px] font-mono tracking-widest text-[#64748B] uppercase">
            [ Procedural Obsidian Core • 60 FPS Mobile GPU ]
          </span>
        </div>
      </section>

      {/* Mobile Metric Badges Grid */}
      <section className="relative z-10 grid grid-cols-2 gap-2.5 mb-8">
        {METRICS.map((metric) => {
          const Icon = metric.icon;
          return (
            <div
              key={metric.label}
              className={`p-3 rounded-xl border backdrop-blur-md flex flex-col justify-between transition-transform active:scale-[0.98] ${metric.glowClass}`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-base font-black tracking-tight">{metric.value}</span>
                <Icon className="w-4 h-4 opacity-80" />
              </div>
              <div>
                <p className="text-[11px] font-semibold text-white leading-tight">{metric.label}</p>
                <p className="text-[9px] text-[#94A3B8] leading-tight mt-0.5">{metric.subtext}</p>
              </div>
            </div>
          );
        })}
      </section>

      {/* Quick Install Card */}
      <section
        id="mobile-install-card"
        className="relative z-10 p-4 rounded-2xl bg-[#08090E]/90 border border-white/10 backdrop-blur-xl shadow-2xl mb-8"
      >
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Terminal className="w-4 h-4 text-[#00F0FF]" />
            <h2 className="text-xs font-bold uppercase tracking-wider text-white">
              Instant Installation
            </h2>
          </div>
          <span className="text-[10px] font-mono text-[#00F0FF] bg-[#00F0FF]/10 px-2 py-0.5 rounded-full border border-[#00F0FF]/20">
            Self-Configuring
          </span>
        </div>

        {/* Platform Selection Pills */}
        <div className="grid grid-cols-2 gap-1.5 mb-3">
          {INSTALL_OPTIONS.map((opt) => (
            <button
              key={opt.id}
              onClick={() => setActivePlatform(opt.id)}
              className={`py-1.5 px-2.5 rounded-lg text-[11px] font-mono font-medium transition-all text-left flex items-center justify-between ${
                activePlatform === opt.id
                  ? "bg-[#00F0FF]/15 text-[#00F0FF] border border-[#00F0FF]/50 shadow-[0_0_12px_rgba(0,240,255,0.2)]"
                  : "bg-white/5 text-[#94A3B8] border border-white/5 hover:bg-white/10"
              }`}
            >
              <span className="truncate">{opt.id}</span>
              {activePlatform === opt.id && <span className="w-1.5 h-1.5 rounded-full bg-[#00F0FF]" />}
            </button>
          ))}
        </div>

        {/* Command Box with 1-Tap Copy */}
        <div className="relative group rounded-xl bg-[#030305] border border-white/10 p-3 mb-2 font-mono text-[11px] text-[#A5F3FC] break-all leading-relaxed">
          <code>{currentSnippet.command}</code>
        </div>

        <p className="text-[10px] text-[#64748B] mb-3 leading-normal">
          {currentSnippet.desc}
        </p>

        {/* 1-Tap Copy Button */}
        <button
          onClick={handleCopy}
          className={`w-full py-2.5 px-4 rounded-xl text-xs font-bold flex items-center justify-center gap-2 transition-all active:scale-[0.98] ${
            copied
              ? "bg-[#10B981] text-black shadow-[0_0_20px_rgba(16,185,129,0.5)]"
              : "bg-[#00F0FF] text-black shadow-[0_0_20px_rgba(0,240,255,0.4)] hover:bg-[#38BDF8]"
          }`}
        >
          {copied ? (
            <>
              <Check className="w-4 h-4 stroke-[2.5]" />
              <span>Copied to Clipboard!</span>
            </>
          ) : (
            <>
              <Copy className="w-4 h-4 stroke-[2.5]" />
              <span>1-Tap Copy Command</span>
            </>
          )}
        </button>
      </section>

      {/* Touch-Optimized Collapsible Acts */}
      <section className="relative z-10 mb-8">
        <div className="flex items-center justify-between mb-3 px-1">
          <h2 className="text-xs font-bold uppercase tracking-wider text-[#94A3B8]">
            Core Architecture Acts
          </h2>
          <span className="text-[10px] font-mono text-[#A855F7]">Touch to expand</span>
        </div>

        <div className="space-y-2">
          {ACTS.map((act) => {
            const isOpen = openAct === act.id;
            const ActIcon = act.icon;

            return (
              <div
                key={act.id}
                className="rounded-xl border border-white/10 bg-[#08090E]/80 backdrop-blur-md overflow-hidden transition-all"
              >
                <button
                  onClick={() => setOpenAct(isOpen ? "" : act.id)}
                  className="w-full p-3.5 flex items-center justify-between text-left transition-colors active:bg-white/5"
                >
                  <div className="flex items-center gap-2.5 min-w-0 pr-2">
                    <div className="w-7 h-7 rounded-lg bg-[#00F0FF]/10 border border-[#00F0FF]/20 flex items-center justify-center text-[#00F0FF] shrink-0">
                      <ActIcon className="w-3.5 h-3.5" />
                    </div>
                    <div className="min-w-0">
                      <div className="flex items-center gap-1.5">
                        <span className="text-xs font-bold text-white truncate">{act.title}</span>
                      </div>
                      <span className="text-[10px] font-mono text-[#00F0FF]/80">{act.tag}</span>
                    </div>
                  </div>
                  <ChevronDown
                    className={`w-4 h-4 text-[#94A3B8] shrink-0 transition-transform duration-200 ${
                      isOpen ? "rotate-180 text-[#00F0FF]" : ""
                    }`}
                  />
                </button>

                {isOpen && (
                  <div className="px-3.5 pb-3.5 pt-1 text-xs border-t border-white/5 bg-[#030305]/60 animate-fadeIn">
                    <p className="text-[#CBD5E1] text-[11px] leading-relaxed mb-3">
                      {act.summary}
                    </p>
                    <ul className="space-y-1.5">
                      {act.highlights.map((item, idx) => (
                        <li key={idx} className="flex items-center gap-2 text-[10px] text-[#94A3B8]">
                          <span className="w-1 h-1 rounded-full bg-[#00F0FF] shrink-0" />
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </section>

      {/* Sticky Bottom Dock */}
      <nav
        aria-label="Mobile Quick Actions"
        className="fixed bottom-0 left-0 right-0 z-50 px-4 py-2.5 bg-[#08090E]/90 backdrop-blur-xl border-t border-white/10 shadow-[0_-10px_30px_rgba(0,0,0,0.8)] flex items-center justify-around"
      >
        <button
          onClick={scrollToInstall}
          className="flex flex-col items-center gap-1 text-[10px] font-mono font-medium text-[#00F0FF] hover:text-white transition-colors"
        >
          <Zap className="w-4 h-4" />
          <span>⚡ Install</span>
        </button>

        <a
          href="https://github.com/aegisbrain/aegis-brain"
          target="_blank"
          rel="noopener noreferrer"
          className="flex flex-col items-center gap-1 text-[10px] font-mono font-medium text-[#CBD5E1] hover:text-[#00F0FF] transition-colors"
        >
          <ExternalLink className="w-4 h-4" />
          <span>⭐ GitHub</span>
        </a>

        <a
          href="#docs"
          onClick={(e) => {
            e.preventDefault();
            setOpenAct("act-1");
            window.scrollTo({ top: 380, behavior: "smooth" });
          }}
          className="flex flex-col items-center gap-1 text-[10px] font-mono font-medium text-[#CBD5E1] hover:text-[#00F0FF] transition-colors"
        >
          <BookOpen className="w-4 h-4" />
          <span>📖 Docs</span>
        </a>
      </nav>
    </div>
  );
}
