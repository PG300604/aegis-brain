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

      // Trigger celebratory confetti in Santioni Spirits colors
      confetti({
        particleCount: 45,
        spread: 60,
        origin: { y: 0.8 },
        colors: ["#B91C1C", "#D4AF37", "#10B981", "#FBF9F5"],
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
    <div className="relative p-6 sm:p-8 bg-[#101116] text-[#FBF9F5] border-2 border-black rounded-lg">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-black/40">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#B91C1C] text-white font-nikkei text-xs uppercase tracking-widest shadow-[2px_2px_0px_#000000]">
            <Terminal className="w-3.5 h-3.5" />
            <span>ZERO-CONFIG SOVEREIGN DEPLOYMENT</span>
          </div>
          <h3 className="text-2xl sm:text-3xl font-charles-rosie text-white uppercase tracking-tight mt-2">
            One-Line Installation Cockpit
          </h3>
          <p className="text-xs sm:text-sm text-zinc-400 font-gt-era max-w-xl mt-1">
            One script initializes the 24/7 background daemon, configures the sub-second SQLite FTS5 neural index,
            and connects the Telegram remote listener.
          </p>
        </div>

        <div className="px-4 py-2 bg-black border-2 border-black rounded text-center shadow-[3px_3px_0px_#D4AF37]">
          <div className="font-nikkei text-xl sm:text-2xl font-extrabold text-[#D4AF37]">
            V2.4.0
          </div>
          <div className="text-[10px] font-mono uppercase text-zinc-400">Stable Release</div>
        </div>
      </div>

      {/* Main Terminal Window */}
      <div className="my-6 rounded-lg overflow-hidden border-2 border-black shadow-[6px_6px_0px_#000000] bg-[#181822]">
        {/* Terminal Chrome Bar */}
        <div className="px-4 py-3 bg-black border-b-2 border-black flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-[#B91C1C] border border-black" />
            <div className="w-3 h-3 rounded-full bg-[#D4AF37] border border-black" />
            <div className="w-3 h-3 rounded-full bg-[#10B981] border border-black" />
            <span className="ml-3 font-mono text-xs text-zinc-300 flex items-center gap-1.5">
              <span>aegis-brain</span>
              <span className="text-zinc-600">/</span>
              <span className="text-[#D4AF37] font-bold">install</span>
            </span>
          </div>

          <div className="flex items-center gap-2 font-mono text-[11px] text-zinc-400">
            <span className="px-2 py-0.5 rounded bg-[#101116] text-[#D4AF37] border border-black shadow-[1px_1px_0px_#000000]">
              {selected.osBadge}
            </span>
          </div>
        </div>

        {/* Tab Selector */}
        <div className="flex items-center border-b border-black/40 bg-black/40 px-2 sm:px-4 overflow-x-auto no-scrollbar">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              type="button"
              onClick={() => setActiveTab(tab.id)}
              className={`px-3 sm:px-4 py-2.5 font-nikkei text-xs uppercase tracking-wider whitespace-nowrap transition-all border-b-2 font-extrabold flex items-center gap-2 cursor-pointer ${
                activeTab === tab.id
                  ? "border-[#B91C1C] text-white bg-black/60 shadow-[inset_0_-2px_0px_#B91C1C]"
                  : "border-transparent text-zinc-400 hover:text-white"
              }`}
            >
              <span>{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Command Body */}
        <div className="p-5 sm:p-7 bg-[#101116] font-mono text-sm relative">
          <div className="text-zinc-500 text-xs mb-3 font-mono select-none">
            {selected.comment}
          </div>

          <div className="flex items-center justify-between gap-4 bg-black p-4 rounded border-2 border-black shadow-[inset_2px_2px_4px_rgba(0,0,0,0.6)]">
            <div className="flex items-center gap-3 overflow-x-auto">
              <span className="text-[#B91C1C] select-none font-bold text-base">&gt;</span>
              <code className="text-[#FBF9F5] font-semibold text-xs sm:text-sm whitespace-nowrap">
                {selected.command}
              </code>
            </div>

            <button
              type="button"
              onClick={handleCopy}
              className={`p-2 rounded font-nikkei text-xs uppercase tracking-wider flex items-center gap-1.5 transition-all shrink-0 cursor-pointer border-2 border-black ${
                copied
                  ? "bg-emerald-600 text-white shadow-[2px_2px_0px_#000000]"
                  : "bg-[#B91C1C] hover:bg-red-800 text-white shadow-[3px_3px_0px_#000000]"
              }`}
            >
              {copied ? (
                <>
                  <Check className="w-3.5 h-3.5" />
                  <span className="hidden sm:inline">COPIED!</span>
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5" />
                  <span className="hidden sm:inline">COPY</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Release Artifacts & SHA-256 Checksums */}
      <div className="p-5 rounded-lg bg-[#FAF8F5] text-black border-2 border-black shadow-[4px_4px_0px_#000000] space-y-4">
        <div className="flex items-center justify-between border-b-2 border-black pb-2">
          <span className="font-nikkei text-xs uppercase tracking-wider font-extrabold text-black">
            Verified Release Artifacts &amp; SHA-256 Checksums
          </span>
          <span className="text-[10px] font-mono bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded font-bold">
            286 TESTS PASSING
          </span>
        </div>

        <div className="space-y-2 font-mono text-xs">
          {ASSETS.map((asset) => (
            <div
              key={asset.name}
              className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 p-2.5 bg-white border border-black shadow-[2px_2px_0px_#000000] rounded"
            >
              <div>
                <div className="font-bold text-black flex items-center gap-2">
                  <FileCode className="w-3.5 h-3.5 text-[#B91C1C]" />
                  <span>{asset.name}</span>
                  <span className="text-[10px] text-zinc-500 font-normal">({asset.size})</span>
                </div>
                <div className="text-[10px] text-zinc-600 mt-0.5 truncate max-w-md">
                  SHA-256: {asset.sha256}
                </div>
              </div>

              <div className="flex items-center gap-2 shrink-0">
                <button
                  type="button"
                  onClick={() => handleCopyHash(asset.sha256)}
                  className="px-2 py-1 bg-[#101116] hover:bg-black text-white text-[10px] font-nikkei uppercase rounded border border-black shadow-[1px_1px_0px_#000000] cursor-pointer"
                >
                  {copiedHash === asset.sha256 ? "COPIED" : "COPY HASH"}
                </button>
                <a
                  href={asset.url}
                  target="_blank"
                  rel="noreferrer"
                  className="px-2 py-1 bg-[#B91C1C] hover:bg-red-800 text-white text-[10px] font-nikkei uppercase rounded border border-black shadow-[1px_1px_0px_#000000] flex items-center gap-1"
                >
                  <Download className="w-3 h-3" />
                  <span>GET</span>
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
