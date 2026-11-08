"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import {
  Search,
  AlertTriangle,
  CheckCircle2,
  Zap,
  Flame,
  Terminal,
  Sparkles,
} from "lucide-react";
import { triggerSoundEffect } from "@/components/audio/SoundtrackController";

interface SearchPreset {
  id: string;
  label: string;
  symbol: string;
  file: string;
}

const PRESETS: SearchPreset[] = [
  {
    id: "rag",
    label: "#RAG",
    symbol: "AST Match: MemoryIndexer.fts5_bm25_search() [Vector Bus]",
    file: "src/aegis/memory/fts5.py:42",
  },
  {
    id: "sqlite",
    label: "#SQLITE",
    symbol: "AST Match: SQLiteWALConnection.execute_pragma_wal() [Memory Core]",
    file: "src/aegis/memory/wal.py:18",
  },
  {
    id: "whisper",
    label: "#WHISPER",
    symbol: "AST Match: AudioChunker.slice_deterministic_25s() [Whisper Transcoder]",
    file: "src/aegis/audio/transcode_slicer.py:31",
  },
  {
    id: "security",
    label: "#SECURITY",
    symbol: "AST Match: ASTTaintChecker.block_shell_injection() [Red-Team Gate]",
    file: "src/aegis/gates/taint.py:59",
  },
];

export function LaptopCliFrame() {
  const [activePreset, setActivePreset] = useState<string>("whisper");
  const [mode, setMode] = useState<"aegis" | "traditional">("aegis");
  const [isSimulating, setIsSimulating] = useState<boolean>(false);
  const [cliStep, setCliStep] = useState<number>(3);

  const preset = PRESETS.find((p) => p.id === activePreset) || PRESETS[2];

  const runSimulation = (selectedMode: "aegis" | "traditional") => {
    setMode(selectedMode);
    setIsSimulating(true);
    setCliStep(0);
    triggerSoundEffect("click");

    setTimeout(() => {
      setCliStep(1);
      triggerSoundEffect("tab");
    }, 600);

    setTimeout(() => {
      setCliStep(2);
      triggerSoundEffect("tab");
    }, 1300);

    setTimeout(() => {
      setCliStep(3);
      setIsSimulating(false);
      triggerSoundEffect(selectedMode === "aegis" ? "success" : "transition");
    }, selectedMode === "aegis" ? 1800 : 2500);
  };

  return (
    <div className="w-full flex flex-col items-center select-none">
      {/* 
        ========================================================================
        MACBOOK PRO / STUDIO MONITOR DISPLAY CHASSIS (Sleek Hardware Bezel)
        ========================================================================
      */}
      <div className="w-full max-w-[1240px] rounded-[24px] bg-[#16171D] p-3 sm:p-4 shadow-[0_25px_70px_rgba(0,0,0,0.85),0_0_0_2px_rgba(255,255,255,0.12)] border-2 border-black relative">
        {/* Top Center Camera Notch Dot */}
        <div className="absolute top-1.5 sm:top-2 left-1/2 -translate-x-1/2 flex items-center justify-center w-12 h-3.5 bg-[#0C0D12] rounded-b-md z-30 border-b border-white/10">
          <span className="w-2 h-2 rounded-full bg-[#1F2430] border border-white/20 flex items-center justify-center">
            <span className="w-0.5 h-0.5 rounded-full bg-emerald-400/80 animate-pulse" />
          </span>
        </div>

        {/* Display Glass Screen */}
        <div className="relative rounded-[16px] overflow-hidden bg-[#090A0F] border border-black/80 shadow-inner">
          {/* Subtle 45-degree Glass Sheen */}
          <div
            className="absolute inset-0 pointer-events-none z-20 opacity-20"
            style={{
              background:
                "linear-gradient(135deg, rgba(255,255,255,0.08) 0%, transparent 40%)",
            }}
          />

          {/* 
            ====================================================================
            CLAUDE CODE CLI TITLEBAR (macOS Terminal Aesthetic)
            ====================================================================
          */}
          <div className="flex items-center justify-between px-4 py-3 bg-[#111218] border-b border-black select-none z-10 relative">
            {/* macOS Window Controls */}
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-[#EF4444] border border-black/30 shadow-[0_1px_2px_rgba(0,0,0,0.4)]" />
              <span className="w-3 h-3 rounded-full bg-[#F59E0B] border border-black/30 shadow-[0_1px_2px_rgba(0,0,0,0.4)]" />
              <span className="w-3 h-3 rounded-full bg-[#10B981] border border-black/30 shadow-[0_1px_2px_rgba(0,0,0,0.4)]" />
            </div>

            {/* Title */}
            <div className="flex items-center gap-2 font-mono text-xs text-zinc-300">
              <span className="font-bold text-[#D4AF37]">claude</span>
              <span className="text-zinc-500">|</span>
              <span className="text-white/80">Claude Code CLI v1.0.24 — priyanshu: ~/vault (aegis-brain)</span>
            </div>

            {/* Status Pill */}
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-0.5 rounded text-[10px] font-mono font-bold bg-[#B91C1C] text-white shadow-[2px_2px_0px_#000000]">
                Aegis WAL Active
              </span>
            </div>
          </div>

          {/* 
            ====================================================================
            SEARCH NEURAL MEMORY BAR & PRESETS (From User Screenshot)
            ====================================================================
          */}
          <div className="p-4 sm:p-5 border-b border-white/10 bg-[#0E0F16]">
            <div className="flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-3">
              {/* Search Input Box */}
              <div className="flex-1 flex items-center gap-2.5 px-3.5 py-2 rounded bg-black/80 border border-white/20 font-mono text-xs">
                <Search className="w-4 h-4 text-[#D4AF37]" />
                <input
                  type="text"
                  readOnly
                  value={`Search memory: ${preset.id}`}
                  className="bg-transparent text-white outline-none w-full font-mono text-xs"
                />
              </div>

              {/* Preset Buttons */}
              <div className="flex items-center gap-2 overflow-x-auto no-scrollbar">
                <span className="text-[10px] font-mono text-zinc-400 uppercase select-none mr-1">
                  PRESETS:
                </span>
                {PRESETS.map((p) => {
                  const isSelected = activePreset === p.id;
                  return (
                    <button
                      key={p.id}
                      type="button"
                      onClick={() => {
                        setActivePreset(p.id);
                        triggerSoundEffect("click");
                      }}
                      className={`px-3 py-1 rounded text-xs font-mono uppercase font-bold transition-all border cursor-pointer ${
                        isSelected
                          ? "bg-[#B91C1C] text-white border-[#B91C1C] shadow-[2px_2px_0px_#000000]"
                          : "bg-black/60 text-zinc-300 hover:text-white border-white/20"
                      }`}
                    >
                      {p.label}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* AST Match Bar (From Screenshot) */}
            <div className="mt-3 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 px-3 py-2 rounded bg-black/90 border border-white/10 font-mono text-[11px]">
              <div className="flex items-center gap-2 text-zinc-300">
                <span className="w-2 h-2 rounded-full bg-[#D4AF37] animate-pulse" />
                <span className="text-[#D4AF37] font-semibold">{preset.symbol}</span>
              </div>
              <span className="text-zinc-500 text-[10px]">{preset.file}</span>
            </div>
          </div>

          {/* 
            ====================================================================
            CLAUDE CODE CLI TERMINAL BODY
            ====================================================================
          */}
          <div className="p-4 sm:p-6 font-mono text-xs sm:text-[13px] leading-relaxed bg-[#08090D] min-h-[220px] select-text">
            {/* Prompt Line */}
            <div className="flex items-center gap-2 text-zinc-300 mb-3 border-b border-white/10 pb-2">
              <span className="text-[#D4AF37] font-bold">claude&gt;</span>
              <span>Continue working on the authentication middleware we started yesterday.</span>
            </div>

            {/* Scenario A: Traditional Amnesia Agent */}
            {mode === "traditional" && (
              <div className="space-y-2 text-red-200">
                {cliStep >= 0 && (
                  <div className="text-zinc-400 flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-red-500 animate-ping" />
                    <span>o Searching disk for conversation history...</span>
                  </div>
                )}
                {cliStep >= 1 && (
                  <div className="text-zinc-400 pl-4 border-l border-red-500/30">
                    • Crawling unindexed transcript.jsonl files across storage (48.2 MB)...
                  </div>
                )}
                {cliStep >= 2 && (
                  <div className="text-[#B91C1C] pl-4 border-l border-red-500/30 font-bold">
                    • Injected 54,200 raw tokens into prompt context (Quota threshold: 50,000 max/min)
                  </div>
                )}
                {cliStep >= 3 && (
                  <div className="mt-3 p-3 bg-red-950/70 border-2 border-[#B91C1C] rounded text-white font-mono text-xs shadow-[3px_3px_0px_#000000]">
                    <div className="text-[#B91C1C] font-extrabold flex items-center gap-1.5 mb-1">
                      <AlertTriangle className="w-4 h-4" />
                      <span>[HTTP 429 CLIFF CRASH] PROVIDER TOKEN QUOTA EXCEEDED</span>
                    </div>
                    <div className="text-zinc-300 text-[11px]">
                      Session frozen for 60 seconds. High token overhead burned your monthly API limit.
                      Agent suffered amnesia: &ldquo;I apologize, what were we building again?&rdquo;
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Scenario B: AegisBrain Persistent Agent */}
            {mode === "aegis" && (
              <div className="space-y-2 text-emerald-200">
                {cliStep >= 0 && (
                  <div className="text-zinc-300 flex items-center gap-2 font-bold">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                    <span>o Thought for 21ms (AegisBrain neural memory bus instant recall)</span>
                  </div>
                )}
                {cliStep >= 1 && (
                  <div className="text-zinc-400 pl-4 border-l border-emerald-500/40">
                    • Explored 1 symbol via SQLite WAL FTS5 virtual table (brain.db: 21ms)
                  </div>
                )}
                {cliStep >= 2 && (
                  <div className="text-emerald-400 pl-4 border-l border-emerald-500/40 font-semibold">
                    • Injected 380 tokens into active context (-99.3% token footprint savings)
                  </div>
                )}
                {cliStep >= 3 && (
                  <div className="mt-3 p-3 bg-emerald-950/60 border-2 border-emerald-500 rounded text-white font-mono text-xs shadow-[3px_3px_0px_#000000]">
                    <div className="text-emerald-400 font-extrabold flex items-center gap-1.5 mb-1">
                      <CheckCircle2 className="w-4 h-4" />
                      <span>[200 OK] INSTANT CONTEXT RESTORED</span>
                    </div>
                    <div className="text-zinc-300 text-[11px]">
                      Claude Code: &ldquo;Restored context from snapshot #042 in 21ms. Continuing middleware verification: 286/286 pytest invariants pass. Ready to edit.&rdquo;
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* 
            ====================================================================
            SIDE-BY-SIDE BENCHMARK CARDS (Matching User Screenshot)
            ====================================================================
          */}
          <div className="p-4 sm:p-6 bg-[#0B0C10] border-t border-white/10">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Left Card: Traditional Multi-MB Crawl */}
              <div className="p-5 rounded-lg bg-black/80 border-2 border-[#B91C1C] shadow-[4px_4px_0px_#000000]">
                <div className="flex items-center justify-between mb-3">
                  <span className="px-2.5 py-0.5 rounded bg-[#B91C1C] text-white text-[10px] font-nikkei uppercase font-extrabold tracking-wider">
                    TRADITIONAL MULTI-MB CRAWL
                  </span>
                  <span className="text-[10px] font-mono text-zinc-500">Unindexed Grep</span>
                </div>

                <div className="flex items-baseline gap-1 my-2">
                  <span className="font-charles-rosie text-4xl sm:text-5xl font-extrabold text-[#B91C1C]">
                    13,100
                  </span>
                  <span className="font-mono text-sm text-[#B91C1C]">ms</span>
                </div>

                <p className="font-gt-era text-xs text-zinc-400 mb-4 leading-relaxed">
                  Crawling raw 50MB conversation logs into context, parsing AST from scratch, and thrashing host memory.
                </p>

                {/* Latency Bar */}
                <div className="space-y-1 mb-4">
                  <div className="flex justify-between text-[10px] font-mono">
                    <span className="text-zinc-500 uppercase">Latency Penalty</span>
                    <span className="text-red-400 font-bold">12.4s Lag</span>
                  </div>
                  <div className="w-full h-1.5 bg-zinc-900 rounded-full overflow-hidden">
                    <div className="h-full bg-[#B91C1C] w-full" />
                  </div>
                </div>

                <div className="space-y-2 font-mono text-xs border-t border-white/10 pt-3 text-zinc-400">
                  <div className="flex justify-between">
                    <span>Context Waste:</span>
                    <span className="text-red-400 font-bold">54,200 Raw Tokens</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Memory Consumption:</span>
                    <span className="text-red-400 font-bold">1.35 GB</span>
                  </div>
                  <div className="flex justify-between">
                    <span>API Gate:</span>
                    <span className="text-[#B91C1C] font-bold">429 RateLimit Triggered</span>
                  </div>
                </div>
              </div>

              {/* Right Card: AegisBrain Neural FTS5 */}
              <div className="p-5 rounded-lg bg-black/80 border-2 border-emerald-500 shadow-[4px_4px_0px_#000000]">
                <div className="flex items-center justify-between mb-3">
                  <span className="px-2.5 py-0.5 rounded bg-emerald-700 text-white text-[10px] font-nikkei uppercase font-extrabold tracking-wider">
                    AEGISBRAIN NEURAL FTS5
                  </span>
                  <span className="text-[10px] font-mono text-emerald-400">brain.db WAL</span>
                </div>

                <div className="flex items-baseline gap-1 my-2">
                  <span className="font-charles-rosie text-4xl sm:text-5xl font-extrabold text-emerald-400">
                    24
                  </span>
                  <span className="font-mono text-sm text-emerald-400">ms</span>
                </div>

                <p className="font-gt-era text-xs text-zinc-400 mb-4 leading-relaxed">
                  Instant symbol retrieval via SQLite FTS5 virtual table with BM25 ranking directly in WAL memory mode.
                </p>

                {/* Latency Bar */}
                <div className="space-y-1 mb-4">
                  <div className="flex justify-between text-[10px] font-mono">
                    <span className="text-zinc-500 uppercase">Sub-Second SLA</span>
                    <span className="text-emerald-400 font-bold">&lt; 25ms Target Met</span>
                  </div>
                  <div className="w-full h-1.5 bg-zinc-900 rounded-full overflow-hidden">
                    <div className="h-full bg-emerald-500 w-[8%]" />
                  </div>
                </div>

                <div className="space-y-2 font-mono text-xs border-t border-white/10 pt-3 text-zinc-400">
                  <div className="flex justify-between">
                    <span>Tokens Injected:</span>
                    <span className="text-emerald-400 font-bold">380 Tokens (-99.3%)</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Memory Consumption:</span>
                    <span className="text-emerald-400 font-bold">19.8 MB (-98.5%)</span>
                  </div>
                  <div className="flex justify-between">
                    <span>API Gate:</span>
                    <span className="text-emerald-400 font-bold">200 OK (Clean Response)</span>
                  </div>
                </div>
              </div>
            </div>

            {/* 
              ==================================================================
              SIMULATOR CONTROL BAR (Matching User Screenshot Exactly)
              ==================================================================
            */}
            <div className="mt-5 p-4 rounded-lg bg-black border border-white/10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div>
                <div className="font-nikkei text-xs uppercase tracking-wider text-white font-extrabold flex items-center gap-2">
                  <Flame className="w-4 h-4 text-[#B91C1C]" />
                  <span>LIVE QUOTA CLIFF SIMULATOR</span>
                </div>
                <p className="text-[11px] font-gt-era text-zinc-400 mt-0.5">
                  Experience the difference between an agent crashing into a token wall vs indexed neural recall.
                </p>
              </div>

              <div className="flex items-center gap-3">
                <button
                  type="button"
                  disabled={isSimulating}
                  onClick={() => runSimulation("traditional")}
                  className="px-4 py-2 bg-[#B91C1C] hover:bg-red-800 disabled:opacity-50 text-white font-nikkei uppercase text-xs rounded border border-black shadow-[2px_2px_0px_#000000] cursor-pointer transition-transform active:translate-y-0.5"
                >
                  TEST TRADITIONAL AGENT
                </button>
                <button
                  type="button"
                  disabled={isSimulating}
                  onClick={() => runSimulation("aegis")}
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-nikkei uppercase text-xs rounded border border-black shadow-[2px_2px_0px_#000000] cursor-pointer transition-transform active:translate-y-0.5"
                >
                  TEST AEGIS FTS5
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 
        ========================================================================
        LAPTOP BOTTOM CHASSIS LIP & HINGE (MacBook / Studio Display Base)
        ========================================================================
      */}
      <div className="w-full max-w-[1300px] flex flex-col items-center">
        {/* Hinge Notch */}
        <div className="w-36 h-3 bg-[#111218] rounded-b-md border-x-2 border-b-2 border-black shadow-md -mt-0.5" />
        {/* Front Lip */}
        <div className="w-full max-w-[1280px] h-3.5 bg-gradient-to-b from-[#1C1D24] to-[#121319] rounded-b-xl border-x-2 border-b-2 border-black shadow-[0_15px_35px_rgba(0,0,0,0.7)] flex justify-center items-center">
          <div className="w-20 h-1 bg-black/60 rounded-full" />
        </div>
      </div>
    </div>
  );
}
