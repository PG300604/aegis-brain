"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Terminal, Search, AlertTriangle, CheckCircle2 } from "lucide-react";
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

export function AntigravityCliSimulator() {
  const [activePreset, setActivePreset] = useState<string>("whisper");
  const [mode, setMode] = useState<"aegis" | "traditional">("aegis");
  const [isSimulating, setIsSimulating] = useState<boolean>(false);
  const [cliStep, setCliStep] = useState<number>(3); // 0 to 4

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
    <div className="relative w-full rounded-xl overflow-hidden border-2 border-black bg-[#0B0C10] shadow-[8px_8px_0px_#000000] text-[#FBF9F5]">
      {/* 
        ========================================================================
        WINDOWS TERMINAL TOP BAR (Authentic Priyanshu-PC: Vault replica)
        ========================================================================
      */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-[#14151C] border-b-2 border-black select-none">
        {/* Left: Tab Pill */}
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-2 px-3 py-1 bg-black rounded-t border-t-2 border-x-2 border-black font-mono text-xs text-white shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]">
            <span className="w-2.5 h-2.5 rounded-sm bg-[#B91C1C] flex items-center justify-center text-[8px] font-bold">
              &gt;
            </span>
            <span className="font-semibold text-zinc-200">PRIYANSHU-PC: Vault</span>
            <span className="text-zinc-500 hover:text-white cursor-pointer ml-1 text-xs">✕</span>
          </div>
          <span className="text-zinc-600 font-mono text-sm px-1">+</span>
        </div>

        {/* Right: Window Controls */}
        <div className="flex items-center gap-3 text-zinc-400 font-mono text-xs">
          <span className="hover:text-white cursor-pointer">—</span>
          <span className="hover:text-white cursor-pointer">□</span>
          <span className="hover:text-red-400 cursor-pointer">✕</span>
        </div>
      </div>

      {/* 
        ========================================================================
        SEARCH NEURAL MEMORY BAR & PRESETS (From User Screenshot)
        ========================================================================
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
        ========================================================================
        LIVE CLI TERMINAL DISPLAY (Antigravity Interactive Mimic)
        ========================================================================
      */}
      <div className="p-4 sm:p-6 font-mono text-xs sm:text-[13px] leading-relaxed bg-[#08090D] min-h-[220px] select-text">
        {/* Antigravity Prompt Header */}
        <div className="flex items-center gap-2 text-zinc-400 mb-3 border-b border-white/10 pb-2">
          <span className="text-cyan-400 font-bold">1 (</span>
          <span className="text-zinc-300">
            &gt; Continue developing the feature where we left off yesterday.
          </span>
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
                  Process frozen for 60 seconds. High token overhead burned your monthly API limit.
                  Agent has amnesia: &ldquo;I apologize, what were we building?&rdquo;
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
                <span>o Thought for 21ms (AegisBrain neural memory bus instant symbol recall)</span>
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
                  <span>[200 OK] INSTANT MEMORY RESTORED</span>
                </div>
                <div className="text-zinc-300 text-[11px]">
                  All architecture rules, past bug fixes, and exact invariants recalled in 21ms.
                  Zero tokens wasted. Coding continues seamlessly.
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* 
        ========================================================================
        SIDE-BY-SIDE BENCHMARK CARDS (Matching Screenshot Exactly)
        ========================================================================
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
      </div>
    </div>
  );
}
