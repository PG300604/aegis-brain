"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import {
  Smartphone,
  Mic,
  Send,
  Zap,
  Radio,
  FileAudio,
  CheckCheck,
  Bot,
  Terminal,
  Clock,
  Sparkles,
  Repeat,
  ShieldCheck,
  Play,
  Volume2,
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
  const [activeScenario, setActiveScenario] = useState<number>(0); // 0: Briefing, 1: Voice, 2: Keystroke
  const [typedInput, setTypedInput] = useState<string>("");
  const [messages, setMessages] = useState<TelegramMessage[]>([]);
  const [isAudioPlaying, setIsAudioPlaying] = useState(false);

  // Auto-run video/GIF looping simulation
  useEffect(() => {
    let timer1: NodeJS.Timeout;
    let timer2: NodeJS.Timeout;
    let timer3: NodeJS.Timeout;
    let timer4: NodeJS.Timeout;

    if (activeScenario === 0) {
      // Step 1: /briefing
      setMessages([]);
      setTypedInput("");
      let charIdx = 0;
      const text = "/briefing";
      const interval = setInterval(() => {
        if (charIdx <= text.length) {
          setTypedInput(text.slice(0, charIdx));
          charIdx++;
        } else {
          clearInterval(interval);
          timer1 = setTimeout(() => {
            setTypedInput("");
            setMessages([
              {
                id: "msg-1",
                sender: "user",
                text: "/briefing",
                timestamp: "10:41 AM",
                tag: "COMMAND",
              },
            ]);
            timer2 = setTimeout(() => {
              setMessages((prev) => [
                ...prev,
                {
                  id: "msg-2",
                  sender: "bot",
                  text: "🛡️ AegisBrain Briefing Digest\n• Restore Point: snap-20261108 (Active)\n• Daemon: http://127.0.0.1:8765 Healthy (Win32 KeepAlive 24/7)\n• Memory: SQLite WAL FTS5 Index Ready (<25ms recall)\n• Tests: 286/286 pytest units passing (0 failing)",
                  timestamp: "10:41 AM",
                  tag: "STATUS DIGEST",
                },
              ]);
              timer3 = setTimeout(() => {
                setActiveScenario(1);
              }, 4000);
            }, 600);
          }, 300);
        }
      }, 50);

      return () => {
        clearInterval(interval);
        clearTimeout(timer1);
        clearTimeout(timer2);
        clearTimeout(timer3);
      };
    } else if (activeScenario === 1) {
      // Step 2: 45s Voice Note
      setTypedInput("");
      setMessages((prev) => [
        ...prev,
        {
          id: "msg-3",
          sender: "user",
          isAudio: true,
          audioDuration: "0:45",
          timestamp: "10:42 AM",
          tag: "VOICE DIRECTIVE (45s)",
        },
      ]);
      setIsAudioPlaying(true);

      timer1 = setTimeout(() => {
        // Chunking & Transcribing
        setMessages((prev) =>
          prev.map((m) =>
            m.id === "msg-3"
              ? {
                  ...m,
                  chunks: [
                    { id: "chunk_001.ogg", duration: "25.0s", status: "Whisper STT Verified" },
                    { id: "chunk_002.ogg", duration: "20.0s", status: "Whisper STT Verified" },
                  ],
                  transcript:
                    '"Refactor memory index to WAL mode and run full test suite with unslop gate"',
                }
              : m
          )
        );

        timer2 = setTimeout(() => {
          setIsAudioPlaying(false);
          setMessages((prev) => [
            ...prev,
            {
              id: "msg-4",
              sender: "bot",
              text: "🚀 Voice Directive Accepted (45s sliced into 2 deterministic chunks):\n• Dispatched to Tier 2 Subagent\n• Invoking hermes chat for code correction\n• 4-Decision Quality Architecture Gate: PASSED\n• pytest: 286/286 PASSED in 48.2s",
              timestamp: "10:42 AM",
              tag: "AUTO-EXECUTE",
            },
          ]);
          timer3 = setTimeout(() => {
            setActiveScenario(2);
          }, 4500);
        }, 1200);
      }, 1500);

      return () => {
        clearTimeout(timer1);
        clearTimeout(timer2);
        clearTimeout(timer3);
      };
    } else if (activeScenario === 2) {
      // Step 3: /type in-flight interrupt
      setTypedInput("");
      let charIdx = 0;
      const text = "/type git status /alt+m";
      const interval = setInterval(() => {
        if (charIdx <= text.length) {
          setTypedInput(text.slice(0, charIdx));
          charIdx++;
        } else {
          clearInterval(interval);
          timer1 = setTimeout(() => {
            setTypedInput("");
            setMessages((prev) => [
              ...prev,
              {
                id: "msg-5",
                sender: "user",
                text: "/type git status /alt+m",
                timestamp: "10:43 AM",
                tag: "IN-FLIGHT INTERRUPT",
              },
            ]);

            timer2 = setTimeout(() => {
              setMessages((prev) => [
                ...prev,
                {
                  id: "msg-6",
                  sender: "bot",
                  text: "⌨️ Injected keystrokes directly into active Antigravity CLI session:\n$ git status\nOn branch main\nYour branch is up to date with 'origin/main'.\nnothing to commit, working tree clean",
                  timestamp: "10:43 AM",
                  tag: "STDOUT STREAM",
                },
              ]);
              timer3 = setTimeout(() => {
                setActiveScenario(0); // Loop back
              }, 4500);
            }, 600);
          }, 300);
        }
      }, 45);

      return () => {
        clearInterval(interval);
        clearTimeout(timer1);
        clearTimeout(timer2);
        clearTimeout(timer3);
      };
    }
  }, [activeScenario]);

  return (
    <div className="w-full">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: Live Telemetry & Scenario Indicators (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          <div className="bg-[#101015] border-2 border-black shadow-[6px_6px_0px_#000000] p-5 rounded-lg space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="font-nikkei text-sm font-bold uppercase tracking-wider text-black bg-[#FBF9F5] border border-black px-3 py-1 inline-flex items-center gap-2 shadow-[2px_2px_0px_#000000]">
                <Zap className="w-4 h-4 text-[#B91C1C]" />
                Live Telemetry Simulator
              </h3>
              <span className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#0A3320] text-[#6EE7B7] text-[10px] font-mono font-bold border border-emerald-500/30">
                <Repeat className="w-3 h-3 animate-spin" style={{ animationDuration: "6s" }} />
                AUTOPLAY LOOP
              </span>
            </div>

            <p className="text-xs text-zinc-300 font-gt-era leading-relaxed">
              Demonstrating AegisBrain&apos;s 24/7 Telegram companion (<code className="font-mono text-[#D4AF37]">@HHAACLIBot</code>). Voice notes are sliced deterministically, transcribed locally with Whisper, and executed in-flight.
            </p>

            {/* 3 Step Indicators */}
            <div className="space-y-2.5 pt-2">
              {/* Step 1 Indicator */}
              <div
                onClick={() => setActiveScenario(0)}
                className={`p-3 rounded border-2 transition-all cursor-pointer ${
                  activeScenario === 0
                    ? "bg-[#1C1F2E] border-[#3B82F6] shadow-[3px_3px_0px_#3B82F6]"
                    : "bg-[#15161F] border-black/80 hover:border-white/20"
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-black text-[#60A5FA] font-bold">
                      PHASE 1
                    </span>
                    <span className="text-xs font-bold text-white font-mono">System Briefing Digest</span>
                  </div>
                  {activeScenario === 0 && (
                    <span className="text-[10px] font-mono text-[#60A5FA] font-bold animate-pulse">
                      ● Active
                    </span>
                  )}
                </div>
                <div className="text-[11px] text-zinc-400 mt-1 font-gt-era">
                  Automated query for restore points, keepalive daemon &amp; pytest status.
                </div>
              </div>

              {/* Step 2 Indicator */}
              <div
                onClick={() => setActiveScenario(1)}
                className={`p-3 rounded border-2 transition-all cursor-pointer ${
                  activeScenario === 1
                    ? "bg-[#1C1F2E] border-[#10B981] shadow-[3px_3px_0px_#10B981]"
                    : "bg-[#15161F] border-black/80 hover:border-white/20"
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-black text-[#10B981] font-bold">
                      PHASE 2
                    </span>
                    <span className="text-xs font-bold text-white font-mono">25s Whisper Audio Shield</span>
                  </div>
                  {activeScenario === 1 && (
                    <span className="text-[10px] font-mono text-[#10B981] font-bold animate-pulse">
                      ● Active
                    </span>
                  )}
                </div>
                <div className="text-[11px] text-zinc-400 mt-1 font-gt-era">
                  Slices 45s voice into 25s &amp; 20s chunks. Zero hallucination guarantee.
                </div>
              </div>

              {/* Step 3 Indicator */}
              <div
                onClick={() => setActiveScenario(2)}
                className={`p-3 rounded border-2 transition-all cursor-pointer ${
                  activeScenario === 2
                    ? "bg-[#1C1F2E] border-[#D4AF37] shadow-[3px_3px_0px_#D4AF37]"
                    : "bg-[#15161F] border-black/80 hover:border-white/20"
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-black text-[#D4AF37] font-bold">
                      PHASE 3
                    </span>
                    <span className="text-xs font-bold text-white font-mono">In-Flight /type /alt+m Interrupt</span>
                  </div>
                  {activeScenario === 2 && (
                    <span className="text-[10px] font-mono text-[#D4AF37] font-bold animate-pulse">
                      ● Active
                    </span>
                  )}
                </div>
                <div className="text-[11px] text-zinc-400 mt-1 font-gt-era">
                  Direct keystroke injection into live Antigravity CLI session without ssh.
                </div>
              </div>
            </div>

            {/* Architecture Metrics Card */}
            <div className="p-3 bg-black/60 rounded border border-white/10 space-y-1.5 font-mono text-[11px] text-zinc-400">
              <div className="flex justify-between">
                <span>Daemon Service:</span>
                <span className="text-emerald-400 font-bold">Win32 Scheduled Task (:8765)</span>
              </div>
              <div className="flex justify-between">
                <span>Whisper STT Latency:</span>
                <span className="text-emerald-400 font-bold">480ms (Local C++)</span>
              </div>
              <div className="flex justify-between">
                <span>Audio Drop Rate:</span>
                <span className="text-emerald-400 font-bold">0.0% (Deterministic Slicing)</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Phone Telegram UI Mockup (7 cols) */}
        <div className="lg:col-span-7">
          <div className="relative mx-auto max-w-[480px] bg-[#171926] rounded-2xl border-4 border-black shadow-[10px_10px_0px_#000000] overflow-hidden">
            {/* Telegram Header */}
            <div className="bg-[#12141F] px-4 py-3 border-b-2 border-black flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="relative w-9 h-9 rounded-full bg-[#1F2235] border border-white/20 flex items-center justify-center text-white">
                  <Bot className="w-5 h-5 text-[#D4AF37]" />
                  <span className="absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full bg-emerald-500 border border-black" />
                </div>
                <div>
                  <div className="text-xs font-bold text-white flex items-center gap-1.5 font-mono">
                    AegisBrain Bot
                    <span className="text-[10px] bg-[#0A3320] text-emerald-400 px-1 rounded">24/7</span>
                  </div>
                  <div className="text-[10px] text-zinc-400 font-mono">@HHAACLIBot • Daemon :8765</div>
                </div>
              </div>

              <div className="text-right">
                <span className="text-[10px] font-mono text-emerald-400 bg-black/50 px-2 py-0.5 rounded border border-emerald-500/30">
                  ONLINE
                </span>
              </div>
            </div>

            {/* Telegram Messages Scroll View */}
            <div className="p-4 space-y-3.5 min-h-[380px] max-h-[460px] overflow-y-auto bg-[#0C0D15] font-sans">
              <div className="text-center my-1">
                <span className="text-[10px] font-mono text-zinc-500 bg-black/40 px-2.5 py-0.5 rounded-full border border-white/5">
                  Today • Sovereign Mobile Telemetry
                </span>
              </div>

              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex flex-col ${
                    msg.sender === "user" ? "items-end" : "items-start"
                  }`}
                >
                  <div
                    className={`max-w-[88%] p-3 rounded-xl text-xs space-y-1.5 ${
                      msg.sender === "user"
                        ? "bg-[#2563EB] text-white rounded-tr-none shadow-[2px_2px_0px_#000000]"
                        : "bg-[#1C1F2E] text-zinc-200 border border-white/10 rounded-tl-none shadow-[2px_2px_0px_#000000]"
                    }`}
                  >
                    {/* Tag badge */}
                    {msg.tag && (
                      <div className="flex items-center gap-1 text-[9px] font-mono uppercase tracking-wider text-white/70">
                        <span>{msg.tag}</span>
                      </div>
                    )}

                    {/* Standard Text Message */}
                    {msg.text && (
                      <p className="whitespace-pre-line font-mono text-[11px] leading-relaxed">
                        {msg.text}
                      </p>
                    )}

                    {/* Audio Note Message */}
                    {msg.isAudio && (
                      <div className="space-y-2">
                        <div className="flex items-center gap-2.5 bg-black/30 p-2 rounded">
                          <button
                            type="button"
                            className="w-7 h-7 rounded-full bg-white text-black flex items-center justify-center flex-shrink-0"
                          >
                            <Play className="w-3.5 h-3.5 fill-black ml-0.5" />
                          </button>
                          <div className="flex-1">
                            {/* Animated Audio Waveform */}
                            <div className="flex items-center gap-[2px] h-5">
                              {[12, 24, 18, 30, 16, 28, 22, 14, 26, 32, 20, 16, 28, 12, 24, 18].map(
                                (h, idx) => (
                                  <motion.span
                                    key={idx}
                                    animate={{
                                      scaleY: isAudioPlaying ? [0.4, 1.2, 0.4] : 0.6,
                                    }}
                                    transition={{
                                      duration: 0.6,
                                      repeat: Infinity,
                                      delay: idx * 0.04,
                                    }}
                                    style={{ height: `${h}px` }}
                                    className="w-[3px] bg-white rounded-full inline-block"
                                  />
                                )
                              )}
                            </div>
                            <div className="flex justify-between text-[9px] font-mono text-white/80 mt-1">
                              <span>0:14 / {msg.audioDuration}</span>
                              <span>Opus 48kHz</span>
                            </div>
                          </div>
                        </div>

                        {/* Deterministic Chunks Readout */}
                        {msg.chunks && (
                          <div className="space-y-1 pt-1 border-t border-white/20">
                            <div className="text-[10px] font-mono text-white/90 font-bold flex items-center gap-1">
                              <Sparkles className="w-3 h-3 text-[#D4AF37]" />
                              Deterministic 25s Transcode Shield:
                            </div>
                            {msg.chunks.map((chk) => (
                              <div
                                key={chk.id}
                                className="text-[10px] font-mono bg-black/40 px-2 py-0.5 rounded flex justify-between"
                              >
                                <span className="text-zinc-300">{chk.id} ({chk.duration})</span>
                                <span className="text-emerald-300">{chk.status}</span>
                              </div>
                            ))}
                          </div>
                        )}

                        {/* Local Whisper Transcript */}
                        {msg.transcript && (
                          <div className="p-2 bg-[#0A3320] border border-emerald-400/40 rounded text-[10px] font-mono text-emerald-200">
                            <span className="font-bold text-white">Local Whisper STT: </span>
                            {msg.transcript}
                          </div>
                        )}
                      </div>
                    )}

                    {/* Timestamp & Read ticks */}
                    <div className="flex items-center justify-end gap-1 text-[9px] text-white/60 pt-0.5">
                      <span>{msg.timestamp}</span>
                      {msg.sender === "user" && (
                        <CheckCheck className="w-3 h-3 text-[#60A5FA]" />
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Telegram Input Bar (Simulates Typing) */}
            <div className="bg-[#12141F] p-3 border-t-2 border-black flex items-center gap-2">
              <div className="flex-1 bg-[#1F2235] rounded-full px-4 py-2 border border-white/10 flex items-center text-xs text-white font-mono">
                {typedInput ? (
                  <span className="text-white flex items-center">
                    {typedInput}
                    <span className="inline-block w-1.5 h-3.5 ml-0.5 bg-[#D4AF37] animate-pulse" />
                  </span>
                ) : (
                  <span className="text-zinc-500 text-[11px]">Message or /command...</span>
                )}
              </div>

              <div className="w-8 h-8 rounded-full bg-[#2563EB] flex items-center justify-center text-white flex-shrink-0 shadow">
                <Send className="w-4 h-4 ml-0.5" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
