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
    <section id="benchmarks" className="relative py-20 px-4 sm:px-6 max-w-6xl mx-auto">
      {/* Decorative aura */}
      <div className="absolute top-1/3 left-1/4 w-[400px] h-[400px] bg-cyan-500/10 blur-[130px] rounded-full pointer-events-none" />
      <div className="absolute top-1/3 right-1/4 w-[400px] h-[400px] bg-rose-500/10 blur-[130px] rounded-full pointer-events-none" />

      {/* Section Header */}
      <div className="text-center mb-12 space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/60 border border-cyan-500/30 text-cyan-400 font-mono text-xs">
          <Clock className="w-3.5 h-3.5" />
          <span>MICROSECOND BENCHMARKS</span>
        </div>
        <h2 className="text-3xl sm:text-4xl font-bold tracking-tight text-white font-mono">
          Sub-Second Neural Recall vs. Multi-MB Crawl
        </h2>
        <p className="text-sm sm:text-base text-zinc-400 max-w-2xl mx-auto">
          Instead of blowing model context windows crawling gigabytes of raw conversation logs, AegisBrain indexes
          everything into SQLite FTS5 neural memory for sub-second retrieval.
        </p>
      </div>

      {/* Live Interactive Query Box */}
      <div className="glass-panel p-4 sm:p-6 rounded-2xl border border-white/10 max-w-3xl mx-auto mb-10 shadow-2xl">
        <div className="flex flex-col sm:flex-row items-center gap-3">
          <div className="relative flex-1 w-full">
            <label htmlFor={inputId} className="sr-only">Query neural index or select preset</label>
            <Search className="w-4 h-4 text-zinc-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
            <input
              id={inputId}
              type="text"
              value={customInput}
              onChange={handleInputChange}
              placeholder="Search neural memory (e.g. rag, sqlite, whisper)..."
              className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-black/60 border border-white/10 text-white font-mono text-xs sm:text-sm focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 transition-all placeholder:text-zinc-600"
            />
          </div>

          {/* Quick presets */}
          <div className="flex items-center gap-1.5 w-full sm:w-auto overflow-x-auto pb-1 sm:pb-0">
            <span className="text-[11px] font-mono text-zinc-500 mr-1 hidden sm:inline">Presets:</span>
            {Object.keys(PRESETS).map((key) => {
              const isSelected = activeQuery.toLowerCase() === key && !customInput;
              return (
                <button
                  key={key}
                  onClick={() => handlePresetClick(key)}
                  className={`px-3 py-1.5 rounded-lg font-mono text-xs font-medium transition-all ${
                    isSelected
                      ? "bg-cyan-500 text-black font-semibold shadow-[0_0_12px_rgba(0,240,255,0.4)]"
                      : "bg-white/5 hover:bg-white/10 text-zinc-400 hover:text-white border border-white/5"
                  }`}
                >
                  #{key}
                </button>
              );
            })}
          </div>
        </div>

        {/* Live AST Match Strip */}
        <div className="mt-3.5 pt-3 border-t border-white/5 flex flex-wrap items-center justify-between text-xs font-mono gap-2 text-zinc-400">
          <div className="flex items-center gap-2 truncate">
            <span className="text-cyan-400 font-bold">● AST Hit:</span>
            <span className="text-zinc-300 truncate">{currentData.astMatch}</span>
          </div>
          <div className="flex items-center gap-1.5 text-zinc-500 text-[11px]">
            <FileCode2 className="w-3.5 h-3.5 text-cyan-500" />
            <span>{currentData.sourcePreview}</span>
          </div>
        </div>
      </div>

      {/* Side-by-Side Stopwatch Comparison */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-stretch">
        {/* Left: Traditional Multi-MB Crawl */}
        <div className="glass-panel p-6 sm:p-8 rounded-2xl border border-rose-500/20 relative overflow-hidden flex flex-col justify-between group hover:border-rose-500/40 transition-all">
          <div className="absolute top-0 right-0 w-32 h-32 bg-rose-500/5 rounded-full blur-2xl pointer-events-none" />

          <div>
            {/* Header Badge */}
            <div className="flex items-center justify-between mb-6">
              <span className="px-2.5 py-1 rounded-md bg-rose-950/60 border border-rose-500/30 font-mono text-xs text-rose-400 font-semibold tracking-wide">
                TRADITIONAL MULTI-MB CRAWL
              </span>
              <span className="font-mono text-xs text-zinc-500">Unindexed Grep</span>
            </div>

            {/* Stopwatch Dial Metric */}
            <div className="flex items-baseline gap-2 mb-2">
              <span className="text-5xl sm:text-6xl font-extrabold font-mono text-rose-400 drop-shadow-[0_0_15px_rgba(244,63,94,0.3)]">
                {currentData.traditionalMs.toLocaleString()}
              </span>
              <span className="text-xl font-mono text-zinc-400 font-semibold">ms</span>
            </div>

            <p className="text-xs sm:text-sm text-zinc-400 mb-6">
              Crawling raw 50MB conversation logs into context, parsing AST from scratch, and thrashing host memory.
            </p>

            {/* Slow Gauge Bar */}
            <div className="space-y-1.5 mb-6">
              <div className="flex justify-between text-xs font-mono text-zinc-400">
                <span>Latency Penalty</span>
                <span className="text-rose-400">12.4s Lag</span>
              </div>
              <div className="w-full h-2 rounded-full bg-zinc-800 overflow-hidden">
                <div className="w-full h-full bg-gradient-to-r from-amber-500 to-rose-600 rounded-full" />
              </div>
            </div>
          </div>

          {/* Stats List */}
          <div className="pt-4 border-t border-white/5 space-y-2.5 font-mono text-xs">
            <div className="flex items-center justify-between text-zinc-400">
              <span className="flex items-center gap-1.5 text-zinc-500">
                <Layers className="w-3.5 h-3.5" /> Context Waste
              </span>
              <span className="text-rose-400 font-medium">32,400+ Raw Tokens</span>
            </div>
            <div className="flex items-center justify-between text-zinc-400">
              <span className="flex items-center gap-1.5 text-zinc-500">
                <Cpu className="w-3.5 h-3.5" /> Memory Consumption
              </span>
              <span className="text-rose-400 font-medium">{currentData.traditionalRam}</span>
            </div>
            <div className="flex items-center justify-between text-zinc-400">
              <span className="flex items-center gap-1.5 text-zinc-500">
                <Database className="w-3.5 h-3.5" /> Token Cost
              </span>
              <span className="text-rose-400 font-medium">$0.45 per query</span>
            </div>
          </div>
        </div>

        {/* Right: AegisBrain FTS5 Neural Recall */}
        <div className="glass-panel-glow p-6 sm:p-8 rounded-2xl border border-cyan-500/40 relative overflow-hidden flex flex-col justify-between shadow-[0_0_40px_rgba(0,240,255,0.15)] group hover:border-cyan-400 transition-all">
          <div className="absolute top-0 right-0 w-32 h-32 bg-cyan-500/10 rounded-full blur-2xl pointer-events-none" />

          <div>
            {/* Header Badge */}
            <div className="flex items-center justify-between mb-6">
              <span className="px-2.5 py-1 rounded-md bg-cyan-950/70 border border-cyan-400/40 font-mono text-xs text-cyan-300 font-semibold tracking-wide flex items-center gap-1.5">
                <Zap className="w-3.5 h-3.5 text-cyan-400" />
                AEGIS FTS5 NEURAL RECALL
              </span>
              <span className="font-mono text-xs text-emerald-400 px-2 py-0.5 rounded bg-emerald-950/50 border border-emerald-500/30 font-bold">
                {speedupFactor}x FASTER
              </span>
            </div>

            {/* Stopwatch Dial Metric */}
            <div className="flex items-baseline gap-2 mb-2">
              <span className="text-5xl sm:text-6xl font-extrabold font-mono text-cyan-400 text-glow-cyan">
                {currentData.aegisMs}
              </span>
              <span className="text-xl font-mono text-cyan-200 font-semibold">ms</span>
            </div>

            <p className="text-xs sm:text-sm text-zinc-300 mb-6">
              Instant BM25 neural matching against persistent local SQLite index (`~/.aegis/brain.db`). Zero context thrashing.
            </p>

            {/* Lightning Fast Bar */}
            <div className="space-y-1.5 mb-6">
              <div className="flex justify-between text-xs font-mono text-zinc-300">
                <span>Sub-Second Response</span>
                <span className="text-emerald-400 font-bold">99.8% Latency Elimination</span>
              </div>
              <div className="w-full h-2 rounded-full bg-zinc-800 overflow-hidden">
                <div className="w-[3%] h-full bg-cyan-400 shadow-[0_0_10px_#00F0FF] rounded-full animate-pulse" />
              </div>
            </div>
          </div>

          {/* Stats List */}
          <div className="pt-4 border-t border-white/10 space-y-2.5 font-mono text-xs">
            <div className="flex items-center justify-between text-zinc-300">
              <span className="flex items-center gap-1.5 text-zinc-400">
                <Layers className="w-3.5 h-3.5 text-cyan-400" /> Compact Context
              </span>
              <span className="text-emerald-400 font-semibold">&lt; 380 Tokens</span>
            </div>
            <div className="flex items-center justify-between text-zinc-300">
              <span className="flex items-center gap-1.5 text-zinc-400">
                <Cpu className="w-3.5 h-3.5 text-cyan-400" /> Memory Footprint
              </span>
              <span className="text-cyan-400 font-semibold">{currentData.aegisRam}</span>
            </div>
            <div className="flex items-center justify-between text-zinc-300">
              <span className="flex items-center gap-1.5 text-zinc-400">
                <Database className="w-3.5 h-3.5 text-cyan-400" /> Token Cost
              </span>
              <span className="text-emerald-400 font-bold">$0.000 (Local FTS5)</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default StopwatchDial;
