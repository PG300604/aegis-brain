"use client";

import React, { useState } from "react";
import {
  Terminal,
  Copy,
  Check,
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
    label: "macOS & Linux (curl)",
    command: "curl -sSL https://raw.githubusercontent.com/PG300604/aegis-brain/main/install.sh | bash",
    comment: "# One-line bootstrap: installs daemon, systemd/launchd 24/7 service, and CLI shim",
    osBadge: "macOS & Linux",
  },
  {
    id: "powershell",
    label: "Windows (PowerShell)",
    command: "irm https://raw.githubusercontent.com/PG300604/aegis-brain/main/install.ps1 | iex",
    comment: "# Registers Antigravity keepalive task, Telegram bot daemon, and global aegis CLI",
    osBadge: "Windows 10/11",
  },
  {
    id: "uv",
    label: "Python (uv)",
    command: "uv tool install git+https://github.com/PG300604/aegis-brain.git",
    comment: "# Isolated ultra-fast Python environment; zero dependency collisions",
    osBadge: "Universal",
  },
  {
    id: "pip",
    label: "Python (pip)",
    command: "pip install git+https://github.com/PG300604/aegis-brain.git",
    comment: "# Standard Python package manager installation directly from git",
    osBadge: "Python 3.10+",
  },
  {
    id: "docker",
    label: "Docker",
    command: "docker run -d -p 8765:8765 --name aegis-brain ghcr.io/pg300604/aegis-brain:latest",
    comment: "# Headless containerized daemon running neural memory and REST bridge",
    osBadge: "Container",
  },
];

export function TerminalInstall() {
  const [activeTab, setActiveTab] = useState<string>("curl");
  const [copied, setCopied] = useState<boolean>(false);

  const selected = TABS.find((t) => t.id === activeTab) || TABS[0];

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(selected.command);
      setCopied(true);

      // Celebratory confetti in Santioni Spirits colors
      confetti({
        particleCount: 40,
        spread: 60,
        origin: { y: 0.8 },
        colors: ["#B91C1C", "#D4AF37", "#10B981", "#FBF9F5"],
      });

      setTimeout(() => setCopied(false), 2500);
    } catch (err) {
      console.error("Clipboard copy failed:", err);
    }
  };

  return (
    <div className="relative p-6 sm:p-8 bg-[#101116] text-[#FBF9F5] border-2 border-black rounded-none">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-black/40">
        <div>
          <div className="font-nikkei text-xs uppercase tracking-[0.2em] text-[#B91C1C] font-extrabold flex items-center gap-2">
            <span className="w-2.5 h-2.5 bg-[#B91C1C] border border-black inline-block" />
            QUICKSTART &amp; INSTALLATION
          </div>
          <h3 className="text-2xl sm:text-3xl font-charles-rosie text-white uppercase tracking-tight mt-2">
            Install in Seconds
          </h3>
          <p className="text-xs sm:text-sm text-zinc-200 font-sans font-medium max-w-xl mt-1 leading-relaxed">
            Deploy the 24/7 background daemon and global CLI with a single command across macOS, Linux, or Windows.
          </p>
        </div>

        <div className="px-4 py-2 bg-black border-2 border-black rounded-none text-center shadow-[3px_3px_0px_#D4AF37]">
          <div className="font-nikkei text-xl sm:text-2xl font-extrabold text-[#D4AF37]">
            V2.4.0
          </div>
          <div className="text-[10px] font-mono uppercase text-zinc-400">Stable Release</div>
        </div>
      </div>

      {/* Sleek Brutalist Command Strip / Code Palette */}
      <div className="my-6 rounded-none overflow-hidden border-2 border-black shadow-[6px_6px_0px_#000000] bg-[#0D0E15]">
        {/* OS Tabs Bar */}
        <div className="flex items-center border-b-2 border-black bg-black px-2 sm:px-4 overflow-x-auto no-scrollbar">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              type="button"
              onClick={() => setActiveTab(tab.id)}
              className={`px-3.5 sm:px-5 py-3 font-nikkei text-xs uppercase tracking-wider whitespace-nowrap transition-all border-b-2 font-extrabold cursor-pointer ${
                activeTab === tab.id
                  ? "border-[#B91C1C] text-white bg-[#101116] shadow-[inset_0_-2px_0px_#B91C1C]"
                  : "border-transparent text-zinc-400 hover:text-white"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Command Body */}
        <div className="p-5 sm:p-7 font-mono text-sm relative">
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4 bg-black/90 p-4 rounded-none border-2 border-black shadow-[inset_2px_2px_4px_rgba(0,0,0,0.6)]">
            <div className="flex items-center gap-3 overflow-x-auto py-1">
              <span className="text-[#D4AF37] select-none font-bold text-sm">$</span>
              <code className="text-[#FBF9F5] font-medium text-xs sm:text-sm whitespace-nowrap">
                {selected.command}
              </code>
            </div>

            <button
              type="button"
              onClick={handleCopy}
              className={`px-4 py-2.5 rounded-none font-nikkei text-xs uppercase tracking-wider flex items-center justify-center gap-2 transition-all shrink-0 cursor-pointer border-2 border-black ${
                copied
                  ? "bg-emerald-600 text-white shadow-[2px_2px_0px_#000000]"
                  : "bg-[#B91C1C] hover:bg-red-800 text-white shadow-[3px_3px_0px_#000000] active:translate-x-0.5 active:translate-y-0.5"
              }`}
            >
              {copied ? (
                <>
                  <Check className="w-3.5 h-3.5" />
                  <span>COPIED!</span>
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5" />
                  <span>COPY COMMAND</span>
                </>
              )}
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
