"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import {
  Play,
  Pause,
  CheckCheck,
  Send,
  Paperclip,
  Smile,
  Mic,
  ChevronLeft,
  Info,
  Radio,
  Cpu,
  Wifi,
  Battery,
  Terminal,
} from "lucide-react";
import { triggerSoundEffect } from "@/components/audio/SoundtrackController";

interface Message {
  id: string;
  sender: "user" | "bot";
  text?: string;
  isAudio?: boolean;
  audioDuration?: string;
  transcript?: string;
  chunks?: { id: string; duration: string; status: string }[];
  timestamp: string;
  tag?: string;
}

export function TelegramSimulator() {
  const [activeScenario, setActiveScenario] = useState<number>(0);
  const [typedInput, setTypedInput] = useState<string>("");
  const [isAudioPlaying, setIsAudioPlaying] = useState<boolean>(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "msg-1",
      sender: "user",
      text: "/briefing",
      timestamp: "10:41 AM",
      tag: "IN-FLIGHT QUERY",
    },
    {
      id: "msg-2",
      sender: "bot",
      text: "⚡ AegisBrain 24/7 Briefing:\n• Snapshot #042 active (WAL clean)\n• HackerNews #1: Local MoE token arbitrage\n• Open PR: 0 defects, 286/286 unit tests passing\n• Priority: Ready for voice or terminal directives.",
      timestamp: "10:41 AM",
      tag: "MEMORY RECALL (24ms)",
    },
  ]);

  // Autoplay scenarios sequentially with typewriter effect
  useEffect(() => {
    let timer1: NodeJS.Timeout;
    let timer2: NodeJS.Timeout;
    let timer3: NodeJS.Timeout;

    if (activeScenario === 0) {
      // Step 1: /briefing
      let charIdx = 0;
      const text = "/briefing";
      const initTimer = setTimeout(() => {
        setTypedInput("");
      }, 0);
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
                tag: "IN-FLIGHT QUERY",
              },
              {
                id: "msg-2",
                sender: "bot",
                text: "⚡ AegisBrain 24/7 Briefing:\n• Snapshot #042 active (WAL clean)\n• HackerNews #1: Local MoE token arbitrage\n• Open PR: 0 defects, 286/286 unit tests passing\n• Priority: Ready for voice or terminal directives.",
                timestamp: "10:41 AM",
                tag: "MEMORY RECALL (24ms)",
              },
            ]);
            timer2 = setTimeout(() => {
              setActiveScenario(1);
            }, 3600);
          }, 300);
        }
      }, 55);

      return () => {
        clearTimeout(initTimer);
        clearInterval(interval);
        clearTimeout(timer1);
        clearTimeout(timer2);
        clearTimeout(timer3);
      };
    } else if (activeScenario === 1) {
      // Step 2: 45s Voice Note
      const initTimer = setTimeout(() => {
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
      }, 0);

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
          }, 4200);
        }, 1300);
      }, 1600);

      return () => {
        clearTimeout(initTimer);
        clearTimeout(timer1);
        clearTimeout(timer2);
        clearTimeout(timer3);
      };
    } else if (activeScenario === 2) {
      // Step 3: /type in-flight interrupt
      let charIdx = 0;
      const text = "/type git status /alt+m";
      const initTimer = setTimeout(() => {
        setTypedInput("");
      }, 0);
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
        clearTimeout(initTimer);
        clearInterval(interval);
        clearTimeout(timer1);
        clearTimeout(timer2);
        clearTimeout(timer3);
      };
    }
  }, [activeScenario]);

  return (
    <div className="w-full">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
        {/* Left Column: Graphic Novel Editorial Narration & Telemetry (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          <div className="border-2 border-black bg-white shadow-[6px_6px_0px_#000000] p-6 space-y-4">
            <div className="border-b-2 border-black pb-3">
              <h3 className="font-charles-rosie text-2xl sm:text-3xl text-black uppercase tracking-tight leading-none">
                Sovereign Mobile Telemetry
              </h3>
            </div>

            {/* Editorial Narration Box matching Santioni graphic novel style */}
            <div className="border-2 border-black bg-[#FAF8F5] p-3 text-[11px] font-mono text-black font-bold uppercase tracking-wider leading-relaxed shadow-[3px_3px_0px_#000000]">
              THE SAINT SPEAKS FROM ANY DEVICE. 45-SECOND RAW AUDIO NOTES ARE INSTANTLY SLICED INTO DETERMINISTIC 25-SECOND CHUNKS, PREVENTING WHISPER HALLUCINATIONS AND INJECTING CODE DIRECTLY IN-FLIGHT.
            </div>

            {/* 3 Step Interactive Indicators */}
            <div className="space-y-2.5 pt-1">
              <button
                type="button"
                onClick={() => {
                  setActiveScenario(0);
                  triggerSoundEffect("click");
                }}
                className={`w-full text-left p-3 border-2 border-black transition-all cursor-pointer ${
                  activeScenario === 0
                    ? "bg-black text-white shadow-[4px_4px_0px_#B91C1C]"
                    : "bg-[#FBF9F5] text-black hover:bg-neutral-100"
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className={`text-[10px] font-mono px-1.5 py-0.5 border border-black font-bold ${
                      activeScenario === 0 ? "bg-[#B91C1C] text-white" : "bg-black text-white"
                    }`}>
                      PHASE 1
                    </span>
                    <span className="font-nikkei text-xs uppercase font-extrabold">
                      Instant Briefing
                    </span>
                  </div>
                  {activeScenario === 0 && (
                    <span className="text-[10px] font-mono text-emerald-400 font-bold">
                      ● Active
                    </span>
                  )}
                </div>
                <div className={`text-[11px] mt-1 font-gt-era ${activeScenario === 0 ? "text-zinc-300" : "text-black/70"}`}>
                  Retrieves active session state, restore point ID, and HackerNews trends in 24ms.
                </div>
              </button>

              <button
                type="button"
                onClick={() => {
                  setActiveScenario(1);
                  triggerSoundEffect("click");
                }}
                className={`w-full text-left p-3 border-2 border-black transition-all cursor-pointer ${
                  activeScenario === 1
                    ? "bg-black text-white shadow-[4px_4px_0px_#B91C1C]"
                    : "bg-[#FBF9F5] text-black hover:bg-neutral-100"
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className={`text-[10px] font-mono px-1.5 py-0.5 border border-black font-bold ${
                      activeScenario === 1 ? "bg-[#B91C1C] text-white" : "bg-black text-white"
                    }`}>
                      PHASE 2
                    </span>
                    <span className="font-nikkei text-xs uppercase font-extrabold">
                      45s Voice Directive
                    </span>
                  </div>
                  {activeScenario === 1 && (
                    <span className="text-[10px] font-mono text-emerald-400 font-bold">
                      ● Active
                    </span>
                  )}
                </div>
                <div className={`text-[11px] mt-1 font-gt-era ${activeScenario === 1 ? "text-zinc-300" : "text-black/70"}`}>
                  Deterministic 25s chunking shield feeds Whisper C++ with zero hallucination.
                </div>
              </button>

              <button
                type="button"
                onClick={() => {
                  setActiveScenario(2);
                  triggerSoundEffect("click");
                }}
                className={`w-full text-left p-3 border-2 border-black transition-all cursor-pointer ${
                  activeScenario === 2
                    ? "bg-black text-white shadow-[4px_4px_0px_#B91C1C]"
                    : "bg-[#FBF9F5] text-black hover:bg-neutral-100"
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className={`text-[10px] font-mono px-1.5 py-0.5 border border-black font-bold ${
                      activeScenario === 2 ? "bg-[#B91C1C] text-white" : "bg-black text-white"
                    }`}>
                      PHASE 3
                    </span>
                    <span className="font-nikkei text-xs uppercase font-extrabold">
                      In-Flight /type /alt+m
                    </span>
                  </div>
                  {activeScenario === 2 && (
                    <span className="text-[10px] font-mono text-emerald-400 font-bold">
                      ● Active
                    </span>
                  )}
                </div>
                <div className={`text-[11px] mt-1 font-gt-era ${activeScenario === 2 ? "text-zinc-300" : "text-black/70"}`}>
                  Injects keystrokes directly into active terminal session without SSH or restart.
                </div>
              </button>
            </div>

            {/* Architecture Invariants */}
            <div className="p-3 bg-black text-white border-2 border-black space-y-1 font-mono text-[11px]">
              <div className="flex justify-between">
                <span className="text-zinc-400">Daemon Runtime:</span>
                <span className="text-emerald-400 font-bold">Win32 Task Scheduler (:8765)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-zinc-400">Whisper Latency:</span>
                <span className="text-emerald-400 font-bold">480ms (Local C++ binary)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-zinc-400">Audio Drop Rate:</span>
                <span className="text-emerald-400 font-bold">0.0% (Deterministic Shield)</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Realistic iPhone 16 Pro with Authentic Telegram iOS (7 cols) */}
        <div className="lg:col-span-7 flex justify-center py-4">
          {/* Outer iPhone Chassis */}
          <div className="relative w-full max-w-[370px] rounded-[50px] p-[10px] bg-[#1C1C20] border-[3px] border-[#383842] shadow-[0_25px_60px_-15px_rgba(0,0,0,0.95),inset_0_1px_1px_rgba(255,255,255,0.2)]">
            {/* Screen Glass Container */}
            <div className="relative w-full rounded-[42px] overflow-hidden bg-[#0E1621] border border-black flex flex-col min-h-[580px] max-h-[620px] select-none">
              
              {/* Dynamic Island */}
              <div className="absolute top-2.5 left-1/2 -translate-x-1/2 w-[105px] h-[26px] bg-black rounded-full z-40 flex items-center justify-between px-3.5 shadow-md">
                <div className="w-2.5 h-2.5 rounded-full bg-[#18181A] border border-[#2D2D35] flex items-center justify-center">
                  <div className="w-1 h-1 rounded-full bg-[#102030]" />
                </div>
                <div className="w-2 h-2 rounded-full bg-[#101014]" />
              </div>

              {/* iOS Status Bar */}
              <div className="relative z-30 pt-2 px-6 flex items-center justify-between text-white text-[12px] font-sans font-semibold">
                <span>9:41</span>
                <div className="flex items-center gap-1.5">
                  <span className="text-[10px] tracking-tighter font-bold">5G</span>
                  <Wifi className="w-3.5 h-3.5" />
                  <div className="w-5 h-2.5 rounded-sm border border-white/80 p-[1px] flex items-center">
                    <div className="w-full h-full bg-emerald-400 rounded-[1px]" />
                  </div>
                </div>
              </div>

              {/* Authentic Telegram iOS Navigation Bar */}
              <div className="relative z-20 bg-[#17212B]/95 backdrop-blur-md px-3 py-2.5 border-b border-black/40 flex items-center justify-between mt-1">
                {/* Back to Chats Button with Unread Badge */}
                <button
                  type="button"
                  className="flex items-center gap-0.5 text-[#50A7EA] font-sans text-xs font-medium cursor-pointer"
                >
                  <ChevronLeft className="w-4 h-4 stroke-[2.5]" />
                  <span>Chats</span>
                  <span className="ml-0.5 px-1.5 py-0.2 bg-[#50A7EA] text-white text-[10px] font-bold rounded-full">
                    24
                  </span>
                </button>

                {/* Center Contact Profile */}
                <div className="flex flex-col items-center">
                  <div className="flex items-center gap-1">
                    <span className="font-sans font-semibold text-white text-[13px] leading-tight">
                      AegisBrain Bot
                    </span>
                    <span className="w-3 h-3 rounded-full bg-[#50A7EA] text-white flex items-center justify-center text-[8px] font-bold">
                      ✓
                    </span>
                  </div>
                  <span className="text-[10px] font-sans text-[#708499] leading-tight">
                    bot
                  </span>
                </div>

                {/* Right Profile Avatar */}
                <div className="w-7 h-7 rounded-full bg-[#2AABEE] text-white flex items-center justify-center font-bold text-xs shadow-inner">
                  <BotIcon className="w-4 h-4" />
                </div>
              </div>

              {/* Authentic Telegram iOS Chat Message Scroll View */}
              <div className="flex-1 p-3 space-y-3 overflow-y-auto bg-[#0E1621] font-sans text-xs">
                {/* Date Divider */}
                <div className="text-center my-1">
                  <span className="text-[10px] font-sans text-[#708499] bg-[#151E27] px-2.5 py-0.5 rounded-full">
                    Today
                  </span>
                </div>

                {/* Messages Feed */}
                {messages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex flex-col ${
                      msg.sender === "user" ? "items-end" : "items-start"
                    }`}
                  >
                    <div
                      className={`max-w-[85%] rounded-2xl p-2.5 shadow-sm text-xs ${
                        msg.sender === "user"
                          ? "bg-[#2B5278] text-white rounded-br-sm"
                          : "bg-[#182533] text-zinc-100 rounded-bl-sm"
                      }`}
                    >
                      {/* Normal text message */}
                      {msg.text && (
                        <div className="whitespace-pre-wrap leading-relaxed font-sans text-[11.5px]">
                          {msg.text}
                        </div>
                      )}

                      {/* User Voice Note in Telegram Style */}
                      {msg.isAudio && (
                        <div className="space-y-2">
                          <div className="flex items-center gap-2.5">
                            <button
                              type="button"
                              onClick={() => {
                                setIsAudioPlaying(!isAudioPlaying);
                                triggerSoundEffect("click");
                              }}
                              className="w-9 h-9 rounded-full bg-[#50A7EA] flex items-center justify-center text-white flex-shrink-0 cursor-pointer shadow"
                            >
                              {isAudioPlaying ? (
                                <Pause className="w-4 h-4" />
                              ) : (
                                <Play className="w-4 h-4 ml-0.5" />
                              )}
                            </button>

                            {/* Telegram Audio Waveform */}
                            <div className="flex-1">
                              <div className="flex items-center gap-[2px] h-6">
                                {[6, 12, 18, 10, 22, 16, 26, 14, 8, 20, 28, 18, 12, 24, 16, 8, 14, 20, 12, 18].map(
                                  (h, idx) => (
                                    <span
                                      key={idx}
                                      style={{ height: `${h}px` }}
                                      className={`w-[2.5px] rounded-full inline-block ${
                                        isAudioPlaying ? "bg-white animate-pulse" : "bg-white/60"
                                      }`}
                                    />
                                  )
                                )}
                              </div>
                              <div className="flex justify-between text-[9px] text-white/80 mt-0.5 font-sans">
                                <span>0:14 / {msg.audioDuration}</span>
                                <span>Opus 48kHz</span>
                              </div>
                            </div>
                          </div>

                          {/* Deterministic Chunking Output */}
                          {msg.chunks && (
                            <div className="pt-1.5 border-t border-white/20 space-y-1">
                              <div className="text-[10px] font-mono text-emerald-300 font-bold flex items-center gap-1.5">
                                <span className="text-[#D4AF37] font-bold">●</span>
                                Deterministic 25s Slicing Engine:
                              </div>
                              {msg.chunks.map((chk) => (
                                <div
                                  key={chk.id}
                                  className="text-[9.5px] font-mono bg-black/40 px-2 py-0.5 rounded flex justify-between"
                                >
                                  <span className="text-zinc-300">{chk.id} ({chk.duration})</span>
                                  <span className="text-emerald-300 font-bold">{chk.status}</span>
                                </div>
                              ))}
                            </div>
                          )}

                          {/* Whisper Local Transcript */}
                          {msg.transcript && (
                            <div className="p-1.5 bg-[#0A3320] border border-emerald-400/40 rounded text-[10px] font-mono text-emerald-200">
                              <span className="font-bold text-white">Whisper STT: </span>
                              {msg.transcript}
                            </div>
                          )}
                        </div>
                      )}

                      {/* Timestamp & Double Checkmarks */}
                      <div className="flex items-center justify-end gap-1 text-[9px] text-white/60 pt-0.5 font-sans">
                        <span>{msg.timestamp}</span>
                        {msg.sender === "user" && (
                          <CheckCheck className="w-3 h-3 text-[#50A7EA]" />
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Authentic Telegram iOS Bottom Input Dock */}
              <div className="bg-[#17212B] px-3 py-2 border-t border-black/40 flex items-center gap-2">
                <button
                  type="button"
                  className="text-[#708499] hover:text-white transition-colors cursor-pointer"
                  title="Attach file"
                >
                  <Paperclip className="w-5 h-5" />
                </button>

                {/* Pill Text Input */}
                <div className="flex-1 bg-[#0E1621] rounded-full px-3.5 py-1.5 border border-[#242F3D] flex items-center text-white text-[12px] font-sans">
                  {typedInput ? (
                    <span className="text-white flex items-center font-mono">
                      {typedInput}
                      <span className="inline-block w-1.5 h-3.5 ml-0.5 bg-[#50A7EA] animate-pulse" />
                    </span>
                  ) : (
                    <span className="text-[#708499] text-[12px]">Message</span>
                  )}
                  <Smile className="w-4 h-4 text-[#708499] ml-auto" />
                </div>

                {/* Right Action Button: Mic or Send */}
                {typedInput ? (
                  <button
                    type="button"
                    className="w-8 h-8 rounded-full bg-[#2AABEE] text-white flex items-center justify-center flex-shrink-0 shadow"
                  >
                    <Send className="w-4 h-4 ml-0.5" />
                  </button>
                ) : (
                  <button
                    type="button"
                    className="text-[#50A7EA] p-1 flex-shrink-0 cursor-pointer"
                    title="Send Voice"
                  >
                    <Mic className="w-5 h-5" />
                  </button>
                )}
              </div>

              {/* iOS Home Indicator */}
              <div className="py-1 bg-[#17212B]">
                <div className="w-32 h-1 bg-white/40 rounded-full mx-auto" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function BotIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      {...props}
    >
      <rect width="18" height="10" x="3" y="11" rx="2" />
      <circle cx="12" cy="5" r="2" />
      <path d="M12 7v4" />
      <line x1="8" x2="8" y1="16" y2="16" />
      <line x1="16" x2="16" y1="16" y2="16" />
    </svg>
  );
}
