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
  History,
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
  { id: "gemini-4", name: "Gemini 4 Flash", tier: "Tier 1 Senior Boss", badge: "Cloud Brain", color: "text-cyan-400" },
  { id: "opus-5.5", name: "Claude Opus 5.5", tier: "Tier 1 Strategic", badge: "Deep Reasoner", color: "text-purple-400" },
  { id: "fable-5.1", name: "Fable 5.1 Orchestrator", tier: "Tier 1 Boss", badge: "Synthesis", color: "text-emerald-400" },
  { id: "argon", name: "Argon High-Cognition", tier: "Tier 1 Manager", badge: "Zero-Leak", color: "text-blue-400" },
  { id: "hermes-3", name: "Hermes 3 (Local)", tier: "Tier 3 Worker", badge: "$0.00 / Token", color: "text-amber-400" },
];

const COMMANDS = [
  { cmd: "/recall", desc: "Sub-second SQLite FTS5 neural memory retrieval (<25ms)" },
  { cmd: "/briefing", desc: "Generate offline task, git status & tech radar briefing" },
  { cmd: "/challenge", desc: "Run red-team adversarial AST security audit on code" },
  { cmd: "/snapshot", desc: "Create point-in-time restore point before code mutations" },
  { cmd: "/pipeline", desc: "Dispatch raw draft through 4-Decision Quality Architecture Gate" },
];

const EFFORTS = [
  { level: 1, label: "Low", desc: "Direct worker generation", color: "bg-emerald-500" },
  { level: 2, label: "Med", desc: "Tier 2 AST audit", color: "bg-cyan-500" },
  { level: 3, label: "High", desc: "Coaching convergence loop", color: "bg-purple-500" },
  { level: 4, label: "Max", desc: "Full Dual-Env verification + Sparks", color: "bg-amber-500" },
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
    }, 1200);
  };

  const handleCommandSelect = (cmd: string) => {
    setPrompt(`${cmd} `);
    setCommandsMenuOpen(false);
  };

  return (
    <div ref={containerRef} className="prompt-bar-container">
      {/* Glow highlight */}
      <div className="absolute -inset-1 rounded-2xl bg-gradient-to-r from-cyan-500/20 via-purple-500/20 to-emerald-500/20 blur-lg opacity-75 group-hover:opacity-100 transition-opacity pointer-events-none" />

      <div className="relative prompt-bar-glass p-3 sm:p-4">
        {/* Top Control Bar: Model Picker & Effort Dial */}
        <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-zinc-800/80">
          {/* Model Selector Button */}
          <div className="relative">
            <button
              type="button"
              onClick={() => {
                setModelDropdownOpen(!modelDropdownOpen);
                setCommandsMenuOpen(false);
              }}
              className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-zinc-900/90 border border-cyan-500/30 hover:border-cyan-400 text-xs font-mono text-zinc-200 transition-colors cursor-pointer"
            >
              <Cpu className={`w-3.5 h-3.5 ${selectedModel.color}`} />
              <span className="font-semibold">{selectedModel.name}</span>
              <span className="text-[10px] px-1.5 py-0.2 rounded bg-zinc-800 text-zinc-400 border border-zinc-700">
                {selectedModel.badge}
              </span>
              <ChevronDown className="w-3 h-3 text-zinc-400" />
            </button>

            {/* Model Dropdown Menu */}
            <AnimatePresence>
              {modelDropdownOpen && (
                <motion.div
                  initial={{ opacity: 0, y: -8, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: -8, scale: 0.95 }}
                  transition={{ duration: 0.15 }}
                  className="absolute left-0 top-full mt-2 w-72 model-dropdown-menu z-50 p-2 space-y-1"
                >
                  <div className="px-2 py-1 text-[10px] font-mono uppercase text-zinc-400 font-bold tracking-wider">
                    Select Execution Engine
                  </div>
                  {MODELS.map((m) => (
                    <button
                      key={m.id}
                      onClick={() => {
                        setSelectedModel(m);
                        setModelDropdownOpen(false);
                      }}
                      className={`w-full flex items-center justify-between p-2 rounded-lg text-left text-xs font-mono transition-colors cursor-pointer ${
                        selectedModel.id === m.id
                          ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40"
                          : "text-zinc-300 hover:bg-zinc-800/60"
                      }`}
                    >
                      <div>
                        <div className="font-semibold text-white">{m.name}</div>
                        <div className="text-[10px] text-zinc-400">{m.tier}</div>
                      </div>
                      <span className="text-[10px] px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-700 text-zinc-300">
                        {m.badge}
                      </span>
                    </button>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Effort Dial (Low -> Max with Sparks) */}
          <div className="flex items-center gap-2.5">
            <div className="flex items-center gap-1.5 text-[11px] font-mono text-zinc-400">
              <Sliders className="w-3.5 h-3.5 text-cyan-400" />
              <span>Cognition Effort:</span>
            </div>

            <div className="flex items-center gap-1 bg-zinc-900/90 p-1 rounded-lg border border-zinc-800">
              {EFFORTS.map((eff) => {
                const isActive = eff.level === effort;
                return (
                  <button
                    key={eff.level}
                    type="button"
                    onClick={() => setEffort(eff.level)}
                    title={eff.desc}
                    className={`px-2.5 py-0.5 rounded text-[11px] font-mono font-medium transition-all cursor-pointer ${
                      isActive
                        ? eff.level === 4
                          ? "bg-amber-500/20 text-amber-300 border border-amber-500/60 shadow-[0_0_12px_rgba(245,158,11,0.5)] effort-max-sparks"
                          : "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-[0_0_10px_rgba(0,240,255,0.3)]"
                        : "text-zinc-500 hover:text-zinc-300"
                    }`}
                  >
                    {eff.label}
                    {eff.level === 4 && isActive && " ✨"}
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
            className="p-2 rounded-xl bg-zinc-900/80 hover:bg-zinc-800 border border-zinc-800 hover:border-cyan-500/40 text-zinc-400 hover:text-cyan-300 transition-colors cursor-pointer"
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
            className="flex-1 bg-transparent px-3 py-2 text-sm sm:text-base text-white placeholder-zinc-500 font-sans focus:outline-none"
          />

          {/* Voice Microphone Toggle */}
          <button
            type="button"
            onClick={() => setIsRecording(!isRecording)}
            title={isRecording ? "Stop Voice Input" : "Dictate via Whisper Voice Shield"}
            className={`p-2 rounded-xl border transition-all cursor-pointer ${
              isRecording
                ? "bg-red-500/20 border-red-500 text-red-400 shadow-[0_0_15px_rgba(239,68,68,0.5)] animate-pulse"
                : "bg-zinc-900/80 hover:bg-zinc-800 border-zinc-800 text-zinc-400 hover:text-zinc-200"
            }`}
          >
            {isRecording ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
          </button>

          {/* Morphing Send / Stop Button */}
          <button
            type="button"
            onClick={handleSend}
            disabled={!prompt.trim() && !isGenerating}
            title={isGenerating ? "Stop Execution" : "Dispatch Prompt"}
            className={`p-2.5 rounded-xl flex items-center justify-center transition-all cursor-pointer ${
              isGenerating
                ? "bg-red-500 text-white shadow-[0_0_20px_rgba(239,68,68,0.6)]"
                : prompt.trim()
                ? "bg-cyan-500 text-black shadow-[0_0_20px_rgba(0,240,255,0.6)] hover:bg-cyan-400"
                : "bg-zinc-800 text-zinc-600 cursor-not-allowed"
            }`}
          >
            {isGenerating ? (
              <Square className="w-4 h-4 fill-white" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </button>
        </div>

        {/* Commands Dropdown */}
        <AnimatePresence>
          {commandsMenuOpen && (
            <motion.div
              initial={{ opacity: 0, y: -6, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -6, scale: 0.98 }}
              className="absolute left-4 top-full mt-2 w-80 model-dropdown-menu z-50 p-2 space-y-1"
            >
              <div className="px-2 py-1 text-[10px] font-mono uppercase text-zinc-400 font-bold tracking-wider">
                Autonomous Directives
              </div>
              {COMMANDS.map((c) => (
                <button
                  key={c.cmd}
                  onClick={() => handleCommandSelect(c.cmd)}
                  className="w-full flex items-start gap-2.5 p-2 rounded-lg text-left font-mono text-xs text-zinc-300 command-item-hover transition-colors cursor-pointer"
                >
                  <span className="font-bold text-cyan-400">{c.cmd}</span>
                  <span className="text-[11px] text-zinc-400 leading-tight">{c.desc}</span>
                </button>
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Live Execution Feedback Badge */}
        {isGenerating && (
          <div className="mt-3 flex items-center justify-between px-3 py-2 rounded-lg bg-cyan-950/40 border border-cyan-500/30 font-mono text-xs text-cyan-300 animate-pulse">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
              <span>Tier 1 Senior Boss dispatches to Tier 2 Junior Boss...</span>
            </div>
            <span className="text-zinc-500">Tier 3 Hermes generating @ $0.00</span>
          </div>
        )}

        {/* Execution Result Banner */}
        {lastExecuted && (
          <motion.div
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-3 p-3 rounded-xl bg-zinc-950/90 border border-emerald-500/30 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs font-mono"
          >
            <div className="flex items-center gap-2 text-emerald-400">
              <Check className="w-4 h-4 shrink-0" />
              <span>Verified: &ldquo;{lastExecuted.text.slice(0, 36)}...&rdquo;</span>
            </div>
            <div className="flex items-center gap-3 text-zinc-400">
              <span className="text-cyan-400">⚡ {lastExecuted.latency}</span>
              <span className="text-emerald-400">💰 {lastExecuted.tokensSaved}</span>
              <span className="px-1.5 py-0.5 rounded bg-emerald-950 border border-emerald-500/40 text-emerald-300 text-[10px]">
                4/4 GATES PASSED
              </span>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}
