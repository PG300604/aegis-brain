"use client";

import React, { useState } from "react";
import {
  Smartphone,
  Mic,
  Send,
  Zap,
  Radio,
  FileAudio,
  CheckCheck,
  Play,
  Pause,
  Bot,
  Terminal,
  Clock,
  Sparkles,
} from "lucide-react";

interface TelegramMessage {
  id: string;
  sender: "user" | "bot";
  text?: string;
  isAudio?: boolean;
  audioDuration?: string;
  chunks?: { id: string; duration: string; status: string }[];
  transcript?: string;
  timestamp: string;
  tag?: string;
}

export function TelegramSimulator() {
  const [messages, setMessages] = useState<TelegramMessage[]>([
    {
      id: "init-1",
      sender: "bot",
      text: "🛡️ AegisBrain Daemon connected on :8765. 24/7 background listener active. Send voice notes, GitHub links, or in-flight commands.",
      timestamp: "18:24",
      tag: "DAEMON 24/7",
    },
  ]);

  const [simulatingAudio, setSimulatingAudio] = useState<boolean>(false);
  const [isPlayingAudio, setIsPlayingAudio] = useState<boolean>(false);
  const [customText, setCustomText] = useState<string>("");

  // Simulation 1: Audio Chunking (45s voice note sliced into deterministic 25s chunks)
  const handleSimulateAudio = () => {
    if (simulatingAudio) return;
    setSimulatingAudio(true);

    const userAudioMsg: TelegramMessage = {
      id: `audio-${Date.now()}`,
      sender: "user",
      isAudio: true,
      audioDuration: "0:45",
      timestamp: "18:26",
    };

    setMessages((prev) => [...prev, userAudioMsg]);

    setTimeout(() => {
      const botResponse: TelegramMessage = {
        id: `chunk-resp-${Date.now()}`,
        sender: "bot",
        text: "⚡ Deterministic Slicer: 45s audio exceeded 30s threshold. Sliced into 25s discrete chunks with zero-loop guarantee.",
        chunks: [
          { id: "chunk_001.ogg", duration: "0:00 - 0:25", status: "Transcribed (0.8s)" },
          { id: "chunk_002.ogg", duration: "0:25 - 0:45", status: "Transcribed (0.6s)" },
        ],
        transcript:
          '"Aegis, run the redteam security audit on src/auth and verify restore snapshot #snapshot-104."',
        timestamp: "18:26",
        tag: "WHISPER LOCAL",
      };
      setMessages((prev) => [...prev, botResponse]);
      setSimulatingAudio(false);
    }, 1200);
  };

  // Simulation 2: In-Flight Interrupt (/type /alt+m)
  const handleSimulateInterrupt = () => {
    const interruptCmd = "/type pytest tests/test_security.py /alt+m";

    const userMsg: TelegramMessage = {
      id: `int-user-${Date.now()}`,
      sender: "user",
      text: interruptCmd,
      timestamp: "18:27",
    };

    setMessages((prev) => [...prev, userMsg]);

    setTimeout(() => {
      const botMsg: TelegramMessage = {
        id: `int-bot-${Date.now()}`,
        sender: "bot",
        text: "⚡ In-Flight Keystroke Injection Successful!\nInjected `pytest tests/test_security.py` into active Antigravity CLI session with `/alt+m` submit.\nDaemon state: Running uninterrupted on :8765.",
        timestamp: "18:27",
        tag: "KEYSTROKE INJECT",
      };
      setMessages((prev) => [...prev, botMsg]);
    }, 800);
  };

  // Simulation 3: Offline Briefing
  const handleSimulateBriefing = () => {
    const userMsg: TelegramMessage = {
      id: `brf-user-${Date.now()}`,
      sender: "user",
      text: "/briefing",
      timestamp: "18:28",
    };

    setMessages((prev) => [...prev, userMsg]);

    setTimeout(() => {
      const botMsg: TelegramMessage = {
        id: `brf-bot-${Date.now()}`,
        sender: "bot",
        text: "📊 AegisBrain Offline Briefing:\n• Snapshot: #snapshot-104 (Pre-flight safe)\n• Neural Memory: 42 symbols indexed (18ms BM25)\n• Community Radar: HackerNews #1 Agentic Security\n• Priority: 0 pending errors • Ready for instructions.",
        timestamp: "18:28",
        tag: "OFFLINE BRIEFING",
      };
      setMessages((prev) => [...prev, botMsg]);
    }, 800);
  };

  const handleSendCustom = (e: React.FormEvent) => {
    e.preventDefault();
    if (!customText.trim()) return;

    const userMsg: TelegramMessage = {
      id: `usr-${Date.now()}`,
      sender: "user",
      text: customText,
      timestamp: "18:29",
    };

    const textCopy = customText;
    setCustomText("");
    setMessages((prev) => [...prev, userMsg]);

    setTimeout(() => {
      const botMsg: TelegramMessage = {
        id: `bot-ack-${Date.now()}`,
        sender: "bot",
        text: `🛡️ Received: "${textCopy}". Synced to neural memory (~/.aegis/brain.db).`,
        timestamp: "18:29",
        tag: "ACK",
      };
      setMessages((prev) => [...prev, botMsg]);
    }, 600);
  };

  return (
    <section id="mobile" className="relative py-20 px-4 sm:px-6 max-w-6xl mx-auto">
      {/* Background radial glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[400px] bg-cyan-500/10 blur-[130px] rounded-full pointer-events-none" />

      {/* Section Header */}
      <div className="text-center mb-12 space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/60 border border-cyan-500/30 text-cyan-400 font-mono text-xs">
          <Smartphone className="w-3.5 h-3.5" />
          <span>24/7 TELEGRAM REMOTE COPILOT</span>
        </div>
        <h2 className="text-3xl sm:text-4xl font-bold tracking-tight text-white font-mono">
          Control Your Workspace From Telegram
        </h2>
        <p className="text-sm sm:text-base text-zinc-400 max-w-2xl mx-auto">
          Send voice notes transcribed locally via Whisper, inject in-flight keystrokes via `/type /alt+m`,
          and query your project memory without leaving your phone.
        </p>
      </div>

      {/* Simulator Container */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
        {/* Left: Controls & Triggers (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          <div className="glass-panel p-6 rounded-2xl border border-white/10 space-y-4">
            <h3 className="font-mono text-xs font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-2">
              <Zap className="w-4 h-4" />
              Interactive Simulation Triggers
            </h3>
            <p className="text-xs text-zinc-400">
              Click any of the automated triggers below to test AegisBrain&apos;s real-time Telegram companion capabilities:
            </p>

            <div className="space-y-2.5 pt-2">
              {/* Trigger 1: 45s Audio */}
              <button
                onClick={handleSimulateAudio}
                disabled={simulatingAudio}
                className="w-full p-3 rounded-xl bg-cyan-950/40 hover:bg-cyan-900/60 border border-cyan-500/30 hover:border-cyan-400 text-left transition-all group flex items-center justify-between"
              >
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-cyan-500/20 text-cyan-400">
                    <FileAudio className="w-4 h-4" />
                  </div>
                  <div>
                    <div className="text-xs font-bold text-white group-hover:text-cyan-300 font-mono">
                      Simulate 45s Voice Note
                    </div>
                    <div className="text-[11px] text-zinc-400">
                      Tests deterministic 25s slicing + Whisper transcription
                    </div>
                  </div>
                </div>
                <span className="text-xs font-mono text-cyan-400 font-bold">Run ➔</span>
              </button>

              {/* Trigger 2: In-flight /type */}
              <button
                onClick={handleSimulateInterrupt}
                className="w-full p-3 rounded-xl bg-emerald-950/40 hover:bg-emerald-900/60 border border-emerald-500/30 hover:border-emerald-400 text-left transition-all group flex items-center justify-between"
              >
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-emerald-500/20 text-emerald-400">
                    <Terminal className="w-4 h-4" />
                  </div>
                  <div>
                    <div className="text-xs font-bold text-white group-hover:text-emerald-300 font-mono">
                      In-Flight /type /alt+m Interrupt
                    </div>
                    <div className="text-[11px] text-zinc-400">
                      Inject keystrokes directly into running CLI session
                    </div>
                  </div>
                </div>
                <span className="text-xs font-mono text-emerald-400 font-bold">Run ➔</span>
              </button>

              {/* Trigger 3: /briefing */}
              <button
                onClick={handleSimulateBriefing}
                className="w-full p-3 rounded-xl bg-purple-950/40 hover:bg-purple-900/60 border border-purple-500/30 hover:border-purple-400 text-left transition-all group flex items-center justify-between"
              >
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-purple-500/20 text-purple-400">
                    <Sparkles className="w-4 h-4" />
                  </div>
                  <div>
                    <div className="text-xs font-bold text-white group-hover:text-purple-300 font-mono">
                      Run /briefing Task Status
                    </div>
                    <div className="text-[11px] text-zinc-400">
                      Zero-prompt offline milestone & snapshot digest
                    </div>
                  </div>
                </div>
                <span className="text-xs font-mono text-purple-400 font-bold">Run ➔</span>
              </button>
            </div>
          </div>

          {/* Key Specs Card */}
          <div className="glass-panel p-4 rounded-xl border border-white/5 space-y-2 font-mono text-xs">
            <div className="flex items-center justify-between text-zinc-400">
              <span>Listener Process:</span>
              <span className="text-emerald-400 font-semibold">aegis.server (:8765)</span>
            </div>
            <div className="flex items-center justify-between text-zinc-400">
              <span>Audio Slicer:</span>
              <span className="text-cyan-400 font-semibold">FFmpeg deterministic 25s</span>
            </div>
            <div className="flex items-center justify-between text-zinc-400">
              <span>STT Engine:</span>
              <span className="text-cyan-400 font-semibold">Local Whisper (0 cloud cost)</span>
            </div>
          </div>
        </div>

        {/* Right: Realistic Smartphone Mockup (7 cols) */}
        <div className="lg:col-span-7 flex justify-center">
          <div className="w-full max-w-[390px] rounded-[48px] p-3 bg-[#0d0f17] border-4 border-zinc-800 shadow-[0_25px_60px_rgba(0,0,0,0.9)] relative overflow-hidden">
            {/* Dynamic Island / Speaker Notch */}
            <div className="absolute top-5 left-1/2 -translate-x-1/2 w-28 h-6 bg-black rounded-full z-20 flex items-center justify-center">
              <div className="w-2.5 h-2.5 rounded-full bg-zinc-900 border border-zinc-700 mr-2" />
              <div className="w-10 h-1 bg-zinc-900 rounded-full" />
            </div>

            {/* Phone Screen Glass */}
            <div className="bg-[#05060b] rounded-[38px] pt-10 pb-4 px-3 flex flex-col h-[540px] border border-white/5 relative">
              {/* Telegram Top Header */}
              <div className="flex items-center justify-between pb-3 px-1 border-b border-white/10">
                <div className="flex items-center gap-2.5">
                  <div className="relative">
                    <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-cyan-600 to-blue-500 flex items-center justify-center text-white font-bold text-xs shadow-[0_0_10px_rgba(0,240,255,0.4)]">
                      <Bot className="w-5 h-5 text-black" />
                    </div>
                    <span className="absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full bg-emerald-500 border-2 border-black animate-pulse" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-xs text-white">@HHAACLIBot</h4>
                    <p className="text-[10px] text-emerald-400 font-mono">● Online 24/7 (:8765)</p>
                  </div>
                </div>

                <div className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/5 text-zinc-400 border border-white/5">
                  AES-256
                </div>
              </div>

              {/* Telegram Messages Feed */}
              <div className="flex-1 overflow-y-auto py-3 space-y-3 text-xs pr-1">
                {messages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex flex-col ${
                      msg.sender === "user" ? "items-end" : "items-start"
                    }`}
                  >
                    <div
                      className={`max-w-[85%] rounded-2xl px-3.5 py-2.5 shadow-sm text-xs ${
                        msg.sender === "user"
                          ? "bg-cyan-600/90 text-white rounded-br-xs"
                          : "bg-zinc-900/90 border border-white/10 text-zinc-200 rounded-bl-xs"
                      }`}
                    >
                      {/* Tag pill if available */}
                      {msg.tag && (
                        <div className="inline-block text-[9px] font-mono px-1.5 py-0.5 rounded bg-cyan-400/10 text-cyan-300 border border-cyan-400/20 mb-1.5">
                          {msg.tag}
                        </div>
                      )}

                      {/* Audio Message Render */}
                      {msg.isAudio ? (
                        <div className="flex items-center gap-3 py-1">
                          <button
                            onClick={() => setIsPlayingAudio(!isPlayingAudio)}
                            className="w-8 h-8 rounded-full bg-white text-black flex items-center justify-center flex-shrink-0"
                          >
                            {isPlayingAudio ? (
                              <Pause className="w-3.5 h-3.5 fill-black" />
                            ) : (
                              <Play className="w-3.5 h-3.5 fill-black ml-0.5" />
                            )}
                          </button>
                          <div className="space-y-1">
                            <div className="flex items-center gap-1 h-4">
                              <span className="w-1 h-3 bg-white/80 rounded-full animate-pulse" />
                              <span className="w-1 h-5 bg-white rounded-full animate-pulse" />
                              <span className="w-1 h-2 bg-white/60 rounded-full" />
                              <span className="w-1 h-4 bg-white/90 rounded-full animate-pulse" />
                              <span className="w-1 h-6 bg-white rounded-full" />
                              <span className="w-1 h-3 bg-white/70 rounded-full" />
                              <span className="w-1 h-4 bg-white rounded-full" />
                            </div>
                            <span className="text-[10px] font-mono opacity-80">{msg.audioDuration}</span>
                          </div>
                        </div>
                      ) : (
                        <div className="whitespace-pre-line leading-relaxed">{msg.text}</div>
                      )}

                      {/* Chunks breakdown box if audio */}
                      {msg.chunks && (
                        <div className="mt-2 pt-2 border-t border-white/10 space-y-1 font-mono text-[10px]">
                          <div className="text-zinc-400">Deterministic Chunks:</div>
                          {msg.chunks.map((chk) => (
                            <div key={chk.id} className="flex justify-between text-zinc-300">
                              <span>• {chk.id} ({chk.duration})</span>
                              <span className="text-emerald-400">{chk.status}</span>
                            </div>
                          ))}
                        </div>
                      )}

                      {/* Transcript box */}
                      {msg.transcript && (
                        <div className="mt-2 p-2 rounded-lg bg-black/40 border border-cyan-500/20 font-mono text-[11px] text-cyan-200">
                          <div className="text-[9px] text-zinc-400 font-sans uppercase tracking-wider mb-0.5">
                            Local Whisper Transcript:
                          </div>
                          {msg.transcript}
                        </div>
                      )}

                      {/* Message Footer / Timestamp */}
                      <div className="flex items-center justify-end gap-1 mt-1 text-[9px] text-zinc-400 font-mono">
                        <span>{msg.timestamp}</span>
                        {msg.sender === "user" && <CheckCheck className="w-3 h-3 text-cyan-200" />}
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Telegram Input Bar */}
              <form onSubmit={handleSendCustom} className="pt-2 border-t border-white/10 flex items-center gap-2">
                <input
                  type="text"
                  value={customText}
                  onChange={(e) => setCustomText(e.target.value)}
                  placeholder="Message @HHAACLIBot..."
                  className="flex-1 bg-zinc-900 border border-white/10 rounded-full px-3.5 py-2 text-xs text-white placeholder:text-zinc-500 focus:outline-none focus:border-cyan-400 font-mono"
                />
                <button
                  type="submit"
                  className="p-2 rounded-full bg-cyan-500 text-black hover:bg-cyan-400 transition-colors"
                >
                  <Send className="w-3.5 h-3.5" />
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default TelegramSimulator;
