"use client";

import React, { useState } from "react";
import {
  Terminal,
  Copy,
  Check,
  Download,
  ShieldCheck,
  CheckCircle2,
  FileCode,
  HardDrive,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import confetti from "canvas-confetti";

interface InstallTab {
  id: string;
  label: string;
  command: string;
  comment: string;
  osBadge: string;
}

const TABS: InstallTab[] = [
  {
    id: "curl",
    label: "curl (macOS/Linux)",
    command: "curl -sSL https://raw.githubusercontent.com/PG300604/aegis-brain/main/install.sh | bash",
    comment: "# One-line bootstrap: installs daemon, systemd/launchd 24/7 service, and CLI shim",
    osBadge: "macOS & Linux",
  },
  {
    id: "powershell",
    label: "PowerShell (Windows)",
    command: "irm https://raw.githubusercontent.com/PG300604/aegis-brain/main/install.ps1 | iex",
    comment: "# Registers Antigravity keepalive task, Telegram bot daemon, and global aegis CLI",
    osBadge: "Windows 10/11",
  },
  {
    id: "uv",
    label: "uv (Universal)",
    command: "uv tool install git+https://github.com/PG300604/aegis-brain.git",
    comment: "# Isolated ultra-fast Python environment; zero dependency collisions",
    osBadge: "Cross-Platform",
  },
  {
    id: "pip",
    label: "pip",
    command: "pip install git+https://github.com/PG300604/aegis-brain.git",
    comment: "# Standard Python package manager installation directly from git",
    osBadge: "Python 3.10+",
  },
  {
    id: "docker",
    label: "docker",
    command: "docker run -d -p 8765:8765 --name aegis-brain ghcr.io/pg300604/aegis-brain:latest",
    comment: "# Headless containerized daemon running neural memory and REST bridge",
    osBadge: "Container",
  },
];

interface AssetRow {
  name: string;
  type: string;
  size: string;
  sha256: string;
  url: string;
}

const ASSETS: AssetRow[] = [
  {
    name: "aegis_brain-0.4.0-py3-none-any.whl",
    type: "Python Wheel Package",
    size: "482 KB",
    sha256: "9f8e21a48c77b2f694e82b7c45819389271a3962d2ea781bc62b25597ccbb81d",
    url: "https://github.com/PG300604/aegis-brain/releases",
  },
  {
    name: "aegis-brain-0.4.0.tar.gz",
    type: "Source Archive",
    size: "620 KB",
    sha256: "a3b190f8982b683ef99cb36a7138374d82b4501a18c0678f28cb887900bfa512",
    url: "https://github.com/PG300604/aegis-brain/releases",
  },
  {
    name: "install.ps1",
    type: "Windows Native Bootstrap",
    size: "18.4 KB",
    sha256: "6e52c8b824ef78cbb819d92ef0e7413697f26c04f981448b11ea99342738a901",
    url: "https://raw.githubusercontent.com/PG300604/aegis-brain/main/install.ps1",
  },
  {
    name: "install.sh",
    type: "POSIX Shell Bootstrap",
    size: "14.2 KB",
    sha256: "df32890a21cf813a07ec9b5377f0d01ca209e51c88db9f18e906b32ec3975ef8",
    url: "https://raw.githubusercontent.com/PG300604/aegis-brain/main/install.sh",
  },
];

export function TerminalInstall() {
  const [activeTab, setActiveTab] = useState<string>("curl");
  const [copied, setCopied] = useState<boolean>(false);
  const [copiedHash, setCopiedHash] = useState<string | null>(null);
  const [showDryRun, setShowDryRun] = useState<boolean>(false);

  const selected = TABS.find((t) => t.id === activeTab) || TABS[0];

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(selected.command);
      setCopied(true);

      // Trigger celebratory confetti
      confetti({
        particleCount: 45,
        spread: 60,
        origin: { y: 0.8 },
        colors: ["#00F0FF", "#10B981", "#38BDF8", "#F8FAFC"],
      });

      setTimeout(() => setCopied(false), 2500);
    } catch (err) {
      console.error("Clipboard copy failed:", err);
    }
  };

  const handleCopyHash = async (hash: string) => {
    try {
      await navigator.clipboard.writeText(hash);
      setCopiedHash(hash);
      setTimeout(() => setCopiedHash(null), 2000);
    } catch (err) {
      console.error("Failed to copy hash:", err);
    }
  };

  return (
    <section id="install" className="relative py-20 px-4 sm:px-6 max-w-5xl mx-auto">
      {/* Decorative ambient aura */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[550px] h-[350px] bg-cyan-500/10 blur-[120px] rounded-full pointer-events-none" />

      {/* Section Header */}
      <div className="text-center mb-10 space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/60 border border-cyan-500/30 text-cyan-400 font-mono text-xs">
          <Terminal className="w-3.5 h-3.5" />
          <span>ZERO-CONFIG DEPLOYMENT</span>
        </div>
        <h2 className="text-3xl sm:text-4xl font-bold tracking-tight text-white font-mono">
          Install AegisBrain In <span className="text-cyan-400 text-glow-cyan">Seconds</span>
        </h2>
        <p className="text-sm sm:text-base text-zinc-400 max-w-2xl mx-auto">
          One script initializes the 24/7 background daemon, configures the sub-second SQLite FTS5 neural index,
          and connects the Telegram remote listener.
        </p>
      </div>

      {/* Main Terminal Window */}
      <div className="glass-panel-glow rounded-2xl overflow-hidden shadow-2xl border border-cyan-500/30">
        {/* Terminal Chrome Bar */}
        <div className="px-4 py-3 bg-[#0a0c14]/90 border-b border-white/10 flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-rose-500/80 border border-rose-600/40" />
            <div className="w-3 h-3 rounded-full bg-amber-500/80 border border-amber-600/40" />
            <div className="w-3 h-3 rounded-full bg-emerald-500/80 border border-emerald-600/40" />
            <span className="ml-3 font-mono text-xs text-zinc-400 flex items-center gap-1.5">
              <span>aegis-brain</span>
              <span className="text-zinc-600">/</span>
              <span className="text-cyan-400">install</span>
            </span>
          </div>

          <div className="flex items-center gap-2 font-mono text-[11px] text-zinc-400">
            <span className="px-2 py-0.5 rounded bg-zinc-800/80 text-zinc-300 border border-white/5">
              {selected.osBadge}
            </span>
          </div>
        </div>

        {/* Tab Selector */}
        <div className="flex items-center border-b border-white/5 bg-[#05060a]/60 px-2 sm:px-4 overflow-x-auto no-scrollbar">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-3 sm:px-4 py-2.5 font-mono text-xs whitespace-nowrap transition-all border-b-2 font-medium flex items-center gap-2 ${
                activeTab === tab.id
                  ? "border-cyan-400 text-cyan-400 bg-cyan-400/5 shadow-[0_2px_8px_rgba(0,240,255,0.15)]"
                  : "border-transparent text-zinc-400 hover:text-zinc-200 hover:border-zinc-700"
              }`}
            >
              <span>{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Command Body */}
        <div className="p-5 sm:p-7 bg-[#030408]/95 font-mono text-sm relative">
          <div className="text-zinc-500 text-xs mb-2 select-none">
            {selected.comment}
          </div>

          <div className="flex items-start justify-between gap-4 py-2">
            <div className="flex items-center gap-3 overflow-x-auto text-emerald-300 font-mono text-xs sm:text-sm py-1">
              <span className="text-cyan-500 select-none font-bold text-base">❯</span>
              <span className="break-all selection:bg-cyan-500 selection:text-black">
                {selected.command}
              </span>
            </div>

            <button
              onClick={handleCopy}
              className={`flex-shrink-0 flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg font-mono text-xs transition-all duration-200 border ${
                copied
                  ? "bg-emerald-500 text-black border-emerald-400 shadow-[0_0_15px_rgba(16,185,129,0.4)]"
                  : "bg-cyan-950/70 hover:bg-cyan-900/90 text-cyan-300 border-cyan-500/40 hover:border-cyan-400 shadow-[0_0_12px_rgba(0,240,255,0.2)]"
              }`}
            >
              {copied ? (
                <>
                  <Check className="w-3.5 h-3.5" />
                  <span className="font-semibold">Copied!</span>
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5" />
                  <span>Copy</span>
                </>
              )}
            </button>
          </div>

          {/* Quick verification callout */}
          <div className="mt-4 pt-4 border-t border-white/5 flex flex-wrap items-center justify-between text-[11px] text-zinc-400 gap-2">
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>Signed release binaries • PGP & SHA-256 verifiable</span>
            </div>
            <button
              onClick={() => setShowDryRun(!showDryRun)}
              className="text-cyan-400 hover:text-cyan-300 flex items-center gap-1 font-mono transition-colors"
            >
              <span>{showDryRun ? "Hide Dry-Run Output" : "View Dry-Run Preview"}</span>
              {showDryRun ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
            </button>
          </div>

          {/* Dry Run Simulation Dropdown */}
          {showDryRun && (
            <div className="mt-3 p-3.5 rounded-lg bg-black/60 border border-white/10 font-mono text-xs text-zinc-300 space-y-1">
              <div className="text-zinc-500"># AegisBrain v0.4.0 Self-Bootstrap Dry-Run:</div>
              <div className="text-emerald-400">[✓] SQLite FTS5 Neural Memory schema verified (~/.aegis/brain.db)</div>
              <div className="text-emerald-400">[✓] FastText embeddings index mapped (1.8ms query latency)</div>
              <div className="text-emerald-400">[✓] Telegram Bot listener hooked (@HHAACLIBot / polling active)</div>
              <div className="text-emerald-400">[✓] In-flight Antigravity injector hooked (/type /alt+m ready)</div>
              <div className="text-cyan-400">[✓] Daemon running 24/7 on http://127.0.0.1:8765</div>
              <div className="text-amber-400">✨ AegisBrain successfully installed. Type `aegis briefing` to start.</div>
            </div>
          )}
        </div>
      </div>

      {/* Direct Download Assets Matrix */}
      <div className="mt-10">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <HardDrive className="w-4 h-4 text-cyan-400" />
            <h3 className="text-sm font-bold tracking-wider uppercase text-zinc-300 font-mono">
              Direct Binary & Release Downloads
            </h3>
          </div>
          <span className="font-mono text-xs text-zinc-500">v0.4.0 Stable</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {ASSETS.map((asset) => (
            <div
              key={asset.name}
              className="glass-panel p-4 rounded-xl border border-white/5 hover:border-cyan-500/30 transition-all group"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-white/5 border border-white/10 group-hover:border-cyan-400/40 transition-colors">
                    <FileCode className="w-4 h-4 text-cyan-400" />
                  </div>
                  <div>
                    <h4 className="font-mono text-xs font-semibold text-white group-hover:text-cyan-300 transition-colors">
                      {asset.name}
                    </h4>
                    <p className="text-[11px] text-zinc-400">{asset.type} • {asset.size}</p>
                  </div>
                </div>

                <a
                  href={asset.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-1.5 rounded-lg bg-white/5 hover:bg-cyan-500 hover:text-black text-zinc-400 hover:border-cyan-400 border border-white/10 transition-all"
                  title="Download Asset"
                >
                  <Download className="w-4 h-4" />
                </a>
              </div>

              {/* SHA256 Hash Row */}
              <div className="mt-3 pt-2.5 border-t border-white/5 flex items-center justify-between text-[10px] font-mono">
                <div className="flex items-center gap-1.5 text-zinc-500 truncate mr-2">
                  <span className="text-zinc-600 font-semibold">SHA256:</span>
                  <span className="truncate">{asset.sha256}</span>
                </div>
                <button
                  onClick={() => handleCopyHash(asset.sha256)}
                  className="flex-shrink-0 text-cyan-400 hover:text-cyan-300 transition-colors flex items-center gap-1"
                  title="Copy SHA256 Hash"
                >
                  {copiedHash === asset.sha256 ? (
                    <span className="text-emerald-400 font-bold flex items-center gap-0.5">
                      <Check className="w-3 h-3" /> Copied
                    </span>
                  ) : (
                    <span>Copy Hash</span>
                  )}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default TerminalInstall;
