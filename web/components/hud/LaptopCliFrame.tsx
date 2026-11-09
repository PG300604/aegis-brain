"use client";

import React, { useState } from "react";
import { motion } from "motion/react";
import { CheckCircle2 } from "lucide-react";
import { triggerSoundEffect } from "@/components/audio/SoundtrackController";

export function LaptopCliFrame() {
  const [activeTab, setActiveTab] = useState<"persistent" | "amnesia">("persistent");

  return (
    <div className="relative w-full py-8 select-none">
      {/* 
        ========================================================================
        COMIC BOOK ANNOTATION CALLOUTS (Radiating from the sides of the laptop)
        ========================================================================
      */}
      <div className="relative w-full max-w-[1320px] mx-auto flex flex-col items-center">
        {/* The Central Laptop Display Unit */}
        <div className="relative w-full max-w-[1060px] flex flex-col items-center z-10">
          
          {/* 
            ====================================================================
            LEFT COMIC CALLOUT (Pointing to Latency & Memory)
            ====================================================================
          */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="hidden xl:block absolute -left-32 top-16 z-30 w-64 bg-[#FAF8F5] text-black border-2 border-black p-4 rounded-none shadow-[6px_6px_0px_#000000] rotate-[-2deg]"
          >
            <div className="flex items-center justify-between border-b-2 border-black pb-1.5 mb-2">
              <span className="font-nikkei text-[10px] uppercase font-extrabold text-[#B91C1C]">
                SPEED AUDIT
              </span>
              <span className="font-mono text-[10px] font-bold text-emerald-700">516x Faster</span>
            </div>
            <p className="font-gt-era text-xs text-black/85 leading-snug">
              Standard agents crawl 50MB of raw text logs across disk (<span className="text-red-700 font-bold">13,100ms</span>).
              Aegis recalls exact symbols instantly in <span className="text-emerald-700 font-bold">24ms</span> via SQLite WAL.
            </p>
            {/* Callout Pointer Arrow */}
            <div className="absolute top-1/2 -right-3 -translate-y-1/2 w-0 h-0 border-t-[8px] border-t-transparent border-b-[8px] border-b-transparent border-l-[12px] border-l-black" />
          </motion.div>

          {/* 
            ====================================================================
            RIGHT COMIC CALLOUT (Pointing to Token Quota Cliff)
            ====================================================================
          */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="hidden xl:block absolute -right-32 top-24 z-30 w-64 bg-[#FAF8F5] text-black border-2 border-black p-4 rounded-none shadow-[6px_6px_0px_#000000] rotate-[2deg]"
          >
            <div className="flex items-center justify-between border-b-2 border-black pb-1.5 mb-2">
              <span className="font-nikkei text-[10px] uppercase font-extrabold text-[#B91C1C]">
                TOKEN QUOTA SHIELD
              </span>
              <span className="font-mono text-[10px] font-bold text-emerald-700">-99.3% Waste</span>
            </div>
            <p className="font-gt-era text-xs text-black/85 leading-snug">
              No more hitting the <span className="text-red-700 font-bold">HTTP 429 Cliff</span>.
              Injects only <span className="text-emerald-700 font-bold">380 tokens</span> of exact symbol context instead of 54,200 raw dump tokens.
            </p>
            {/* Callout Pointer Arrow */}
            <div className="absolute top-1/2 -left-3 -translate-y-1/2 w-0 h-0 border-t-[8px] border-t-transparent border-b-[8px] border-b-transparent border-r-[12px] border-r-black" />
          </motion.div>

          {/* 
            ====================================================================
            LAPTOP MONITOR DISPLAY BEZEL (Studio Display / MacBook Pro Aesthetic)
            ====================================================================
          */}
          <div className="w-full rounded-[20px] bg-[#14151C] p-3 sm:p-4 shadow-[0_30px_90px_rgba(0,0,0,0.9),0_0_0_2px_rgba(255,255,255,0.1)] border-2 border-black relative">
            
            {/* Top Camera Dot */}
            <div className="absolute top-2 left-1/2 -translate-x-1/2 w-3 h-3 rounded-full bg-[#08090D] border border-white/20 flex items-center justify-center z-30">
              <span className="w-1 h-1 rounded-full bg-emerald-400 animate-pulse" />
            </div>

            {/* Display Glass Canvas */}
            <div className="relative rounded-[12px] overflow-hidden bg-[#0A0A0E] border border-black shadow-inner">
              
              {/* macOS Terminal Title Bar */}
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between px-4 py-2.5 bg-[#12131A] border-b border-black gap-2 select-none">
                <div className="flex items-center gap-3">
                  <div className="flex items-center gap-2">
                    <span className="w-3 h-3 rounded-full bg-[#EF4444] border border-black/30" />
                    <span className="w-3 h-3 rounded-full bg-[#F59E0B] border border-black/30" />
                    <span className="w-3 h-3 rounded-full bg-[#10B981] border border-black/30" />
                  </div>
                  <div className="font-mono text-xs text-zinc-300 flex items-center gap-2">
                    <span className="text-[#D97706] font-bold">✳ claude</span>
                    <span className="text-zinc-600">•</span>
                    <span className="text-zinc-300">~/vault/aegis-brain</span>
                  </div>
                </div>

                {/* Sleek Terminal Mode Tabs */}
                <div className="flex items-center gap-1.5 font-mono text-[11px]">
                  <button
                    type="button"
                    onClick={() => {
                      setActiveTab("persistent");
                      triggerSoundEffect("click");
                    }}
                    className={`px-3 py-1 rounded transition-all cursor-pointer ${
                      activeTab === "persistent"
                        ? "bg-emerald-700 text-white font-bold shadow-[2px_2px_0px_#000000]"
                        : "bg-black/50 text-zinc-400 hover:text-white border border-white/10"
                    }`}
                  >
                    ● Persistent Recall (21ms)
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setActiveTab("amnesia");
                      triggerSoundEffect("click");
                    }}
                    className={`px-3 py-1 rounded transition-all cursor-pointer ${
                      activeTab === "amnesia"
                        ? "bg-[#B91C1C] text-white font-bold shadow-[2px_2px_0px_#000000]"
                        : "bg-black/50 text-zinc-400 hover:text-white border border-white/10"
                    }`}
                  >
                    ● Amnesia Crash (13.1s)
                  </button>
                </div>
              </div>

              {/* 
                ================================================================
                AUTHENTIC CLAUDE CODE CLI TERMINAL BODY
                ================================================================
              */}
              <div className="p-5 sm:p-7 font-mono text-xs sm:text-[13px] leading-relaxed bg-[#0A0B10] text-[#F3F4F6] min-h-[340px] select-text">
                
                {/* Claude Code Welcome Box (Exact replica from ProductTalk article) */}
                <div className="text-zinc-400 text-[11px] sm:text-xs mb-5 font-mono">
                  <div className="text-zinc-500">╭─────────────────────────────────────────────────────────────────╮</div>
                  <div className="text-zinc-300">│ <span className="text-[#D97706] font-bold">Claude Code</span> research preview (v0.2.29)                       │</div>
                  <div className="text-zinc-400">│ Welcome to Claude Code!                                         │</div>
                  <div className="text-zinc-400">│ Connected to AegisBrain Persistence Engine (SQLite WAL FTS5)   │</div>
                  <div className="text-zinc-500">╰─────────────────────────────────────────────────────────────────╯</div>
                </div>

                {/* Developer Prompt Line */}
                <div className="flex items-start gap-2 mb-4">
                  <span className="text-[#D97706] font-extrabold select-none">&gt;</span>
                  <span className="text-white font-medium">
                    Continue working on the authentication middleware we started yesterday.
                  </span>
                </div>

                {/* Scenario A: Traditional Amnesia Crash */}
                {activeTab === "amnesia" && (
                  <div className="space-y-2.5 text-zinc-300">
                    <div className="flex items-center gap-2 text-zinc-400">
                      <span className="w-2 h-2 rounded-full bg-red-500" />
                      <span>● Searching disk for past session transcripts...</span>
                    </div>
                    <div className="text-zinc-400 pl-4 border-l-2 border-red-500/40">
                      ● Crawling unindexed transcript.jsonl across storage (48.2 MB)...
                    </div>
                    <div className="text-[#B91C1C] pl-4 border-l-2 border-red-500/40 font-bold">
                      ● Injected 54,200 raw tokens into context window (TPM limit: 50,000/min)
                    </div>
                    <div className="mt-4 p-4 rounded bg-red-950/80 border-2 border-[#B91C1C] shadow-[4px_4px_0px_#000000] text-red-200">
                      <div className="flex items-center gap-2 text-[#B91C1C] font-bold text-xs uppercase mb-1">
                        <span>[HTTP 429 CLIFF CRASH] TPM RATE LIMIT EXCEEDED</span>
                      </div>
                      <p className="text-[11px] text-zinc-300 mt-1">
                        Claude: &ldquo;I apologize, but my session context was lost due to rate-limit overflow. What were we building again?&rdquo;
                      </p>
                    </div>
                  </div>
                )}

                {/* Scenario B: AegisBrain Instant Persistence */}
                {activeTab === "persistent" && (
                  <div className="space-y-2.5 text-zinc-300">
                    <div className="flex items-center gap-2 text-emerald-400 font-semibold">
                      <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                      <span>● Querying AegisBrain neural index (brain.db)...</span>
                    </div>
                    <div className="text-zinc-300 pl-4 border-l-2 border-emerald-500/40">
                      ● Retrieved 4 auth symbols &amp; invariants in <span className="text-emerald-400 font-bold">21ms</span> (FTS5 BM25 match)
                    </div>
                    <div className="text-emerald-400 pl-4 border-l-2 border-emerald-500/40 font-semibold">
                      ● Injected <span className="text-white font-bold">380 tokens</span> into active context (-99.3% token footprint savings)
                    </div>
                    <div className="mt-4 p-4 rounded bg-emerald-950/70 border-2 border-emerald-500 shadow-[4px_4px_0px_#000000] text-emerald-100">
                      <div className="flex items-center gap-2 text-emerald-400 font-bold text-xs uppercase mb-1">
                        <CheckCircle2 className="w-4 h-4" />
                        <span>[200 OK] INSTANT CONTEXT RESTORED (21MS)</span>
                      </div>
                      <p className="text-[11px] text-zinc-200 mt-1">
                        Claude: &ldquo;Context restored from snapshot #042 in 21ms. Continuing authentication middleware: all 286/286 pytest invariants passing. Ready to edit.&rdquo;
                      </p>
                    </div>
                  </div>
                )}

                {/* Claude Code Status Bar Footer */}
                <div className="mt-6 pt-4 border-t border-white/10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 text-[10px] text-zinc-500 font-mono select-none">
                  <div className="flex items-center gap-3">
                    <span>Cost: <span className="text-white font-bold">{activeTab === "persistent" ? "$0.001" : "$0.84"}</span></span>
                    <span>•</span>
                    <span>Tokens: <span className="text-white font-bold">{activeTab === "persistent" ? "380" : "54,200"}</span></span>
                    <span>•</span>
                    <span>Latency: <span className={activeTab === "persistent" ? "text-emerald-400 font-bold" : "text-red-400 font-bold"}>{activeTab === "persistent" ? "21ms" : "13,100ms"}</span></span>
                  </div>
                  <div>esc to cancel • /help for commands</div>
                </div>
              </div>
            </div>
          </div>

          {/* Laptop Base Hinge & Stand */}
          <div className="w-40 h-3 bg-[#111218] rounded-b-md border-x-2 border-b-2 border-black shadow-md -mt-0.5" />
          <div className="w-full max-w-[1100px] h-3.5 bg-gradient-to-b from-[#1C1D24] to-[#111218] rounded-b-xl border-x-2 border-b-2 border-black shadow-[0_20px_45px_rgba(0,0,0,0.85)] flex justify-center items-center">
            <div className="w-24 h-1 bg-black/70 rounded-full" />
          </div>
        </div>

        {/* Bottom Annotations: Graphic Novel Captions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6 w-full max-w-4xl">
          <div className="p-4 bg-[#FAF8F5] border-2 border-black rounded-none shadow-[4px_4px_0px_#000000]">
            <div className="font-nikkei text-xs uppercase text-[#B91C1C] font-extrabold mb-1">
              HOST HEADROOM: 19.8 MB VS 1.35 GB
            </div>
            <p className="font-gt-era text-xs text-black/80">
              Aegis runs directly in SQLite WAL mode. Your RAM overhead stays negligible, eliminating CPU throttling and host machine freezes.
            </p>
          </div>
          <div className="p-4 bg-[#FAF8F5] border-2 border-black rounded-none shadow-[4px_4px_0px_#000000]">
            <div className="font-nikkei text-xs uppercase text-emerald-800 font-extrabold mb-1">
              ZERO SESSION BOUNDARY CRASHES
            </div>
            <p className="font-gt-era text-xs text-black/80">
              When terminal sessions terminate, restore points guarantee 100% context survival on your next prompt.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
