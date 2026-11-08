"use client";

import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import {
  Sparkles,
  Send,
  Square,
  Mic,
  MicOff,
  Sliders,
  ChevronDown,
  Terminal,
  Cpu,
  Zap,
  Flame,
  Check,
  Search,
  Shield,
  Layers,
  Clock,
} from "lucide-react";
import "./PromptBar.css";

interface ModelOption {
  id: string;
  name: string;
  tier: string;
  badge: string;
  color: string;
}

const MODELS: ModelOption[] = [
  { id: "gemini-4", name: "Gemini 4 Flash", tier: "Tier 1 Senior Boss", badge: "Cloud Brain", color: "text-[#D4AF37]" },
  { id: "opus-5.5", name: "Claude Opus 5.5", tier: "Tier 1 Strategic", badge: "Deep Reasoner", color: "text-[#B91C1C]" },
  { id: "fable-5.1", name: "Fable 5.1 Orchestrator", tier: "Tier 1 Boss", badge: "Synthesis", color: "text-[#10B981]" },
  { id: "argon", name: "Argon High-Cognition", tier: "Tier 1 Manager", badge: "Zero-Leak", color: "text-[#F59E0B]" },
  { id: "hermes-3", name: "Hermes 3 (Local)", tier: "Tier 3 Worker", badge: "$0.00 / Token", color: "text-[#FBF9F5]" },
];

const COMMANDS = [
  { cmd: "/recall", desc: "Sub-second SQLite FTS5 neural memory retrieval (<25ms)" },
  { cmd: "/briefing", desc: "Generate offline task, git status & tech radar briefing" },
  { cmd: "/challenge", desc: "Run red-team adversarial AST security audit on code" },
  { cmd: "/snapshot", desc: "Create point-in-time restore point before code mutations" },
  { cmd: "/pipeline", desc: "Dispatch raw draft through 4-Decision Quality Architecture Gate" },
];

const EFFORTS = [
  { level: 1, label: "Low", desc: "Direct worker generation", color: "bg-[#10B981]" },
  { level: 2, label: "Med", desc: "Tier 2 AST audit", color: "bg-[#D4AF37]" },
  { level: 3, label: "High", desc: "Coaching convergence loop", color: "bg-[#F59E0B]" },
  { level: 4, label: "Max", desc: "Full Dual-Env verification + Sparks", color: "bg-[#B91C1C]" },
];

export function PromptBar() {
  const [prompt, setPrompt] = useState("");
  const [effort, setEffort] = useState(4); // default Max
  const [selectedModel, setSelectedModel] = useState<ModelOption>(MODELS[0]);
  const [modelDropdownOpen, setModelDropdownOpen] = useState(false);
  const [commandsMenuOpen, setCommandsMenuOpen] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [lastExecuted, setLastExecuted] = useState<{
    text: string;
    model: string;
    latency: string;
    tokensSaved: string;
    gatePassed: boolean;
  } | null>(null);

  const containerRef = useRef<HTMLDivElement>(null);

  // Close menus on outside click
  useEffect(() => {
    const handleOutsideClick = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setModelDropdownOpen(false);
        setCommandsMenuOpen(false);
      }
    };
    document.addEventListener("mousedown", handleOutsideClick);
    return () => document.removeEventListener("mousedown", handleOutsideClick);
  }, []);

  const handleSend = () => {
    if (!prompt.trim() && !isGenerating) return;

    if (isGenerating) {
      setIsGenerating(false);
      return;
    }

    setIsGenerating(true);
    setLastExecuted(null);

    // Simulate multi-tier execution
    setTimeout(() => {
      setIsGenerating(false);
      setLastExecuted({
        text: prompt,
        model: selectedModel.name,
        latency: "22 ms",
        tokensSaved: "2,840 tokens ($0.042 saved)",
        gatePassed: true,
      });
      setPrompt("");
    }, 1100);
  };

  const handleCommandSelect = (cmd: string) => {
    setPrompt(`${cmd} `);
    setCommandsMenuOpen(false);
  };

  return (
    <div ref={containerRef} className="prompt-bar-container">
      <div className="relative prompt-bar-glass p-3 sm:p-4 bg-[#101116] border-2 sm:border-3 border-black rounded-xl shadow-[6px_6px_0px_#000000]">
        {/* Top Control Bar: Model Picker & Effort Dial */}
        <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-black/40">
          {/* Model Selector Button */}
          <div className="relative">
            <button
              type="button"
              onClick={() => {
                setModelDropdownOpen(!modelDropdownOpen);
                setCommandsMenuOpen(false);
              }}
              className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#181822] border-2 border-black hover:border-[#B91C1C] text-xs font-mono text-[#FBF9F5] shadow-[2px_2px_0px_#000000] transition-all cursor-pointer"
            >
              <Cpu className={`w-3.5 h-3.5 ${selectedModel.color}`} />
              <span className="font-nikkei font-bold uppercase tracking-wider">{selectedModel.name}</span>
              <span className="text-[10px] px-1.5 py-0.2 rounded bg-black text-[#D4AF37] border border-[#D4AF37]/30 font-mono">
                {selectedModel.badge}
              </span>
              <ChevronDown className="w-3 h-3 text-white/50" />
            </button>

            {/* Model Dropdown Menu */}
            <AnimatePresence>
              {modelDropdownOpen && (
                <motion.div
                  initial={{ opacity: 0, y: -8, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: -8, scale: 0.95 }}
                  transition={{ duration: 0.15 }}
                  className="absolute left-0 top-full mt-2 w-72 model-dropdown-menu z-50 p-2 space-y-1 bg-[#14141C] border-2 border-black shadow-[6px_6px_0px_#000000] rounded-lg"
                >
                  <div className="px-2 py-1 text-[10px] font-nikkei uppercase text-[#D4AF37] font-bold tracking-wider">
                    Select Execution Engine
                  </div>
                  {MODELS.map((m) => (
                    <button
                      key={m.id}
                      onClick={() => {
                        setSelectedModel(m);
                        setModelDropdownOpen(false);
                      }}
                      className={`w-full flex items-center justify-between p-2 rounded text-left text-xs font-mono transition-colors cursor-pointer ${
                        selectedModel.id === m.id
                          ? "bg-[#B91C1C]/20 text-white border border-[#B91C1C]"
                          : "text-zinc-300 hover:bg-black/60"
                      }`}
                    >
                      <div>
                        <div className="font-nikkei font-bold text-white uppercase">{m.name}</div>
                        <div className="text-[10px] text-zinc-400 font-gt-era">{m.tier}</div>
                      </div>
                      <span className="text-[10px] px-1.5 py-0.5 rounded bg-black border border-white/20 text-[#D4AF37]">
                        {m.badge}
                      </span>
                    </button>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Effort Dial (Low -> Max with Inked Sparks) */}
          <div className="flex items-center gap-2">
            <div className="flex items-center gap-1.5 text-[11px] font-nikkei uppercase tracking-wider text-white/70">
              <Sliders className="w-3.5 h-3.5 text-[#D4AF37]" />
              <span className="hidden sm:inline">Cognition:</span>
            </div>

            <div className="flex items-center gap-1 bg-[#181822] p-1 rounded-lg border-2 border-black shadow-[2px_2px_0px_#000000]">
              {EFFORTS.map((eff) => {
                const isActive = eff.level === effort;
                return (
                  <button
                    key={eff.level}
                    type="button"
                    onClick={() => setEffort(eff.level)}
                    title={eff.desc}
                    className={`px-2.5 py-0.5 rounded text-[11px] font-nikkei uppercase tracking-wider font-extrabold transition-all cursor-pointer ${
                      isActive
                        ? eff.level === 4
                          ? "bg-[#B91C1C] text-white border border-black shadow-[1px_1px_0px_#000000] effort-max-sparks"
                          : "bg-[#D4AF37] text-black border border-black shadow-[1px_1px_0px_#000000]"
                        : "text-zinc-400 hover:text-white"
                    }`}
                  >
                    {eff.label}
                    {eff.level === 4 && isActive && " ★"}
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Input Bar Area */}
        <div className="relative mt-3 flex items-center gap-2">
          {/* Quick Slash Commands Trigger */}
          <button
            type="button"
            onClick={() => {
              setCommandsMenuOpen(!commandsMenuOpen);
              setModelDropdownOpen(false);
            }}
            title="Aegis Commands"
            className="p-2 rounded-lg bg-[#181822] hover:bg-[#20202e] border-2 border-black text-[#D4AF37] hover:text-white shadow-[2px_2px_0px_#000000] transition-colors cursor-pointer"
          >
            <Terminal className="w-4 h-4" />
          </button>

          {/* Prompt Input */}
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            placeholder="Ask AegisBrain to recall memory, audit AST security, or dispatch local workers..."
            className="flex-1 bg-transparent px-3 py-2 text-sm sm:text-base text-[#FBF9F5] placeholder-white/35 font-gt-era focus:outline-none"
          />

          {/* Voice Microphone Toggle */}
          <button
            type="button"
            onClick={() => setIsRecording(!isRecording)}
            title={isRecording ? "Stop Voice Input" : "Dictate via Whisper Voice Shield"}
            className={`p-2 rounded-lg border-2 border-black transition-all cursor-pointer shadow-[2px_2px_0px_#000000] ${
              isRecording
                ? "bg-[#B91C1C] text-white animate-pulse"
                : "bg-[#181822] hover:bg-[#222230] text-zinc-300"
            }`}
          >
            {isRecording ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
          </button>

          {/* Send / Stop Action Button */}
          <button
            type="button"
            onClick={handleSend}
            disabled={!prompt.trim() && !isGenerating}
            className={`px-4 py-2 rounded-lg font-nikkei text-xs uppercase tracking-wider font-extrabold flex items-center gap-1.5 border-2 border-black shadow-[3px_3px_0px_#000000] transition-all cursor-pointer ${
              isGenerating
                ? "bg-[#B91C1C] text-white animate-pulse"
                : prompt.trim()
                ? "bg-[#B91C1C] hover:bg-red-800 text-white hover:-translate-y-0.5 hover:shadow-[4px_4px_0px_#000000]"
                : "bg-zinc-800 text-zinc-500 cursor-not-allowed border-black/40 shadow-none"
            }`}
          >
            {isGenerating ? (
              <>
                <Square className="w-3.5 h-3.5 fill-current" />
                <span className="hidden sm:inline">HALT</span>
              </>
            ) : (
              <>
                <Send className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">DISPATCH</span>
              </>
            )}
          </button>
        </div>

        {/* Slash Commands Dropdown Menu */}
        <AnimatePresence>
          {commandsMenuOpen && (
            <motion.div
              initial={{ opacity: 0, y: -6, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -6, scale: 0.98 }}
              className="absolute left-4 top-full mt-2 w-80 bg-[#14141C] border-2 border-black rounded-lg shadow-[6px_6px_0px_#000000] z-50 p-2 space-y-1"
            >
              <div className="px-2 py-1 text-[10px] font-nikkei uppercase text-[#D4AF37] font-bold tracking-wider">
                Aegis Autonomous Commands
              </div>
              {COMMANDS.map((c) => (
                <button
                  key={c.cmd}
                  onClick={() => handleCommandSelect(c.cmd)}
                  className="w-full p-2 text-left rounded hover:bg-black/60 transition-colors cursor-pointer group"
                >
                  <div className="font-mono text-xs font-bold text-[#D4AF37] group-hover:text-white">
                    {c.cmd}
                  </div>
                  <div className="text-[11px] font-gt-era text-zinc-400 mt-0.5 leading-snug">
                    {c.desc}
                  </div>
                </button>
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Real-time Execution Toast / Result Pill */}
        <AnimatePresence>
          {lastExecuted && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="mt-3 pt-3 border-t border-black/40 flex flex-wrap items-center justify-between gap-2 text-xs font-mono"
            >
              <div className="flex items-center gap-2 text-zinc-300">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
                <span className="font-nikkei font-bold uppercase text-white">Dispatched:</span>
                <span className="italic text-zinc-400 truncate max-w-[200px] sm:max-w-xs">
                  &ldquo;{lastExecuted.text}&rdquo;
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 rounded bg-black border border-[#D4AF37]/40 text-[#D4AF37] text-[11px] font-mono">
                  {lastExecuted.latency}
                </span>
                <span className="px-2 py-0.5 rounded bg-emerald-950/80 border border-emerald-500/50 text-emerald-300 text-[11px] font-mono">
                  4-Gate Passed
                </span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
