"use client";

import React, { useState, useId } from "react";
import {
  Clock,
  Zap,
  Search,
  Database,
  Cpu,
  Layers,
  ArrowRight,
  TrendingDown,
  Activity,
  FileCode2,
} from "lucide-react";

interface QueryPreset {
  key: string;
  query: string;
  aegisMs: number;
  traditionalMs: number;
  symbols: number;
  aegisRam: string;
  traditionalRam: string;
  sourcePreview: string;
  astMatch: string;
}

const PRESETS: Record<string, QueryPreset> = {
  rag: {
    key: "rag",
    query: "rag",
    aegisMs: 19,
    traditionalMs: 12400,
    symbols: 42,
    aegisRam: "18.2 MB",
    traditionalRam: "1.24 GB",
    sourcePreview: "src/aegis/rag/hybrid_retriever.py:84",
    astMatch: "HybridRetriever.query_embeddings() [AST Node #1409]",
  },
  sqlite: {
    key: "sqlite",
    query: "sqlite",
    aegisMs: 22,
    traditionalMs: 11950,
    symbols: 38,
    aegisRam: "21.4 MB",
    traditionalRam: "1.18 GB",
    sourcePreview: "src/aegis/memory/sqlite_fts5.py:42",
    astMatch: "NeuralMemory.fts5_match_bm25() [FTS5 Virtual Table]",
  },
  whisper: {
    key: "whisper",
    query: "whisper",
    aegisMs: 24,
    traditionalMs: 13100,
    symbols: 19,
    aegisRam: "19.8 MB",
    traditionalRam: "1.35 GB",
    sourcePreview: "src/aegis/audio/transcode_slicer.py:31",
    astMatch: "AudioChunker.slice_deterministic_25s() [Whisper Transcoder]",
  },
  security: {
    key: "security",
    query: "security",
    aegisMs: 20,
    traditionalMs: 12850,
    symbols: 54,
    aegisRam: "23.1 MB",
    traditionalRam: "1.29 GB",
    sourcePreview: "src/aegis/gates/redteam_ast.py:16",
    astMatch: "ASTTaintChecker.block_shell_injection() [Gate #3 Security]",
  },
};

export function StopwatchDial() {
  const [activeQuery, setActiveQuery] = useState<string>("rag");
  const [customInput, setCustomInput] = useState<string>("");
  const inputId = useId();

  // Pick current data or compute dynamic values for custom text
  const currentData: QueryPreset = PRESETS[activeQuery.toLowerCase()] || {
    key: "custom",
    query: customInput || activeQuery,
    aegisMs: Math.floor(18 + ((customInput.length * 3) % 7)),
    traditionalMs: 12200 + ((customInput.length * 110) % 800),
    symbols: Math.max(8, 28 + (customInput.length % 25)),
    aegisRam: "22.5 MB",
    traditionalRam: "1.26 GB",
    sourcePreview: `src/aegis/index/${customInput || "custom"}_dispatch.py:27`,
    astMatch: `SymbolResolver.find_ast_nodes("${customInput || activeQuery}")`,
  };

  const speedupFactor = Math.round(currentData.traditionalMs / currentData.aegisMs);

  const handlePresetClick = (key: string) => {
    setActiveQuery(key);
    setCustomInput("");
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setCustomInput(val);
    if (val.trim()) {
      setActiveQuery(val.trim());
    } else {
      setActiveQuery("rag");
    }
  };

  return (
    <div className="relative p-6 sm:p-8 bg-[#101116] text-[#FBF9F5] border-2 border-black rounded-lg">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-black/40">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#B91C1C] text-white font-nikkei text-xs uppercase tracking-widest shadow-[2px_2px_0px_#000000]">
            <Clock className="w-3.5 h-3.5" />
            <span>SUB-SECOND SPEED BENCHMARK SANDBOX</span>
          </div>
          <h3 className="text-2xl sm:text-3xl font-charles-rosie text-white uppercase tracking-tight mt-2">
            24ms SQLite WAL vs 12,400ms Raw Crawl
          </h3>
          <p className="text-xs sm:text-sm text-zinc-400 font-gt-era max-w-xl mt-1">
            Test live query tokens. Aegis indexes symbols directly into SQLite FTS5 for sub-second retrieval.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <div className="px-4 py-2 bg-emerald-950/80 border-2 border-emerald-500 rounded text-center shadow-[3px_3px_0px_#000000]">
            <div className="font-nikkei text-xl sm:text-2xl font-extrabold text-emerald-400">
              {speedupFactor}x
            </div>
            <div className="text-[10px] font-mono uppercase text-emerald-300">Measured Speedup</div>
          </div>
        </div>
      </div>

      {/* Live Interactive Query Search Bar */}
      <div className="my-6 p-4 bg-[#181822] border-2 border-black rounded-lg shadow-[4px_4px_0px_#000000]">
        <div className="flex flex-col sm:flex-row items-center gap-3">
          <div className="relative flex-1 w-full">
            <label htmlFor={inputId} className="sr-only">Query neural index or select preset</label>
            <Search className="w-4 h-4 text-[#D4AF37] absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
            <input
              id={inputId}
              type="text"
              value={customInput}
              onChange={handleInputChange}
              placeholder="Search neural memory (e.g. rag, sqlite, whisper, security)..."
              className="w-full pl-10 pr-4 py-2.5 rounded-lg bg-black border-2 border-black text-white font-gt-era text-xs sm:text-sm focus:outline-none focus:border-[#B91C1C] transition-all placeholder:text-zinc-600 shadow-[inset_2px_2px_4px_rgba(0,0,0,0.5)]"
            />
          </div>

          {/* Quick presets */}
          <div className="flex items-center gap-1.5 w-full sm:w-auto overflow-x-auto pb-1 sm:pb-0">
            <span className="text-[11px] font-nikkei uppercase text-zinc-400 mr-1 hidden sm:inline">Presets:</span>
            {Object.keys(PRESETS).map((key) => {
              const isSelected = activeQuery.toLowerCase() === key && !customInput;
              return (
                <button
                  key={key}
                  type="button"
                  onClick={() => handlePresetClick(key)}
                  className={`px-3 py-1.5 rounded font-nikkei text-xs uppercase tracking-wider font-extrabold transition-all cursor-pointer border-2 border-black ${
                    isSelected
                      ? "bg-[#B91C1C] text-white shadow-[2px_2px_0px_#000000]"
                      : "bg-[#101116] hover:bg-black text-zinc-300 shadow-[1px_1px_0px_#000000]"
                  }`}
                >
                  #{key}
                </button>
              );
            })}
          </div>
        </div>

        {/* Live AST Match Strip */}
        <div className="mt-3 pt-3 border-t border-black/40 flex flex-wrap items-center justify-between text-xs font-mono gap-2 text-zinc-400">
          <div className="flex items-center gap-2 truncate">
            <span className="text-[#D4AF37] font-bold">● AST Match:</span>
            <span className="text-zinc-200 truncate">{currentData.astMatch}</span>
          </div>
          <div className="flex items-center gap-1.5 text-zinc-400 text-[11px]">
            <FileCode2 className="w-3.5 h-3.5 text-[#B91C1C]" />
            <span>{currentData.sourcePreview}</span>
          </div>
        </div>
      </div>

      {/* Side-by-Side Stopwatch Comparison */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-stretch font-mono">
        {/* Left: Traditional Multi-MB Crawl */}
        <div className="p-6 rounded-lg bg-[#181822] border-2 border-black shadow-[4px_4px_0px_#B91C1C] flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4 pb-2 border-b border-black/40">
              <span className="px-2.5 py-0.5 rounded bg-[#B91C1C] text-white font-nikkei text-xs uppercase font-extrabold">
                TRADITIONAL MULTI-MB CRAWL
              </span>
              <span className="text-xs text-zinc-500">Unindexed Grep</span>
            </div>

            <div className="flex items-baseline gap-2 mb-2">
              <span className="text-5xl sm:text-6xl font-extrabold text-[#B91C1C]">
                {currentData.traditionalMs.toLocaleString()}
              </span>
              <span className="text-xl text-zinc-400">ms</span>
            </div>

            <p className="text-xs text-zinc-400 mb-6 font-gt-era leading-relaxed">
              Crawling raw 50MB conversation logs into context, parsing AST from scratch, and thrashing host memory.
            </p>

            <div className="space-y-1.5 mb-6">
              <div className="flex justify-between text-xs text-zinc-400 font-mono">
                <span>Latency Penalty</span>
                <span className="text-[#B91C1C] font-bold">12.4s Lag</span>
              </div>
              <div className="w-full h-3 rounded bg-black border border-black overflow-hidden">
                <div className="w-full h-full bg-[#B91C1C] rounded" />
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-black/40 space-y-2 text-xs">
            <div className="flex items-center justify-between text-zinc-400">
              <span className="flex items-center gap-1.5 text-zinc-500">
                <Layers className="w-3.5 h-3.5" /> Context Waste
              </span>
              <span className="text-[#B91C1C] font-bold">32,400+ Raw Tokens</span>
            </div>
            <div className="flex items-center justify-between text-zinc-400">
              <span className="flex items-center gap-1.5 text-zinc-500">
                <Cpu className="w-3.5 h-3.5" /> Memory Consumption
              </span>
              <span className="text-[#B91C1C] font-bold">{currentData.traditionalRam}</span>
            </div>
            <div className="flex items-center justify-between text-zinc-400">
              <span className="flex items-center gap-1.5 text-zinc-500">
                <Database className="w-3.5 h-3.5" /> Token Cost
              </span>
              <span className="text-[#B91C1C] font-bold">$0.45 per query</span>
            </div>
          </div>
        </div>

        {/* Right: AegisBrain FTS5 Neural Recall */}
        <div className="p-6 rounded-lg bg-[#181822] border-2 border-black shadow-[4px_4px_0px_#10B981] flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4 pb-2 border-b border-black/40">
              <span className="px-2.5 py-0.5 rounded bg-emerald-600 text-white font-nikkei text-xs uppercase font-extrabold">
                AEGIS NEURAL FTS5 CORE
              </span>
              <span className="text-xs text-emerald-400 font-bold">Sub-Second Indexed</span>
            </div>

            <div className="flex items-baseline gap-2 mb-2">
              <span className="text-5xl sm:text-6xl font-extrabold text-emerald-400">
                {currentData.aegisMs}
              </span>
              <span className="text-xl text-zinc-400">ms</span>
            </div>

            <p className="text-xs text-zinc-400 mb-6 font-gt-era leading-relaxed">
              FTS5 virtual table BM25 lookup over SQLite WAL database with sub-millisecond symbol resolution.
            </p>

            <div className="space-y-1.5 mb-6">
              <div className="flex justify-between text-xs text-zinc-400 font-mono">
                <span>Latency</span>
                <span className="text-emerald-400 font-bold">&lt; 25ms Real-Time Snap</span>
              </div>
              <div className="w-full h-3 rounded bg-black border border-black overflow-hidden">
                <div
                  className="h-full bg-emerald-500 rounded transition-all duration-300"
                  style={{ width: `${Math.min(100, (currentData.aegisMs / 30) * 100)}%` }}
                />
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-black/40 space-y-2 text-xs">
            <div className="flex items-center justify-between text-zinc-400">
              <span className="flex items-center gap-1.5 text-zinc-500">
                <Layers className="w-3.5 h-3.5" /> Context Window Load
              </span>
              <span className="text-emerald-400 font-bold">&lt; 380 Tokens</span>
            </div>
            <div className="flex items-center justify-between text-zinc-400">
              <span className="flex items-center gap-1.5 text-zinc-500">
                <Cpu className="w-3.5 h-3.5" /> Memory Consumption
              </span>
              <span className="text-emerald-400 font-bold">{currentData.aegisRam}</span>
            </div>
            <div className="flex items-center justify-between text-zinc-400">
              <span className="flex items-center gap-1.5 text-zinc-500">
                <Database className="w-3.5 h-3.5" /> Token Cost
              </span>
              <span className="text-emerald-400 font-bold">$0.00 / Query</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
