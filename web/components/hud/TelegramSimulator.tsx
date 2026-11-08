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
import { VoicePill } from "@/components/react-bits/VoicePill";

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
      sender: "user",
      text: "/briefing",
      timestamp: "10:41 AM",
      tag: "COMMAND",
    },
    {
      id: "init-2",
      sender: "bot",
      text: "⚡ AegisBrain Briefing Protocol\n• Restore Point: snap-2026-11-08-01 (100% clean)\n• Active Workers: Hermes 3 (Idle), MoE Qwen 2.5 (Idle)\n• Host Hardware: CPU 18% | RAM 4.2GB Free\n• Priorities: 0 failing tests (286/286 passing)",
      timestamp: "10:41 AM",
      tag: "STATUS DIGEST",
    },
  ]);

  const [simulatingAudio, setSimulatingAudio] = useState(false);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const [customText, setCustomText] = useState("");

  const handleSimulateAudio = () => {
    setSimulatingAudio(true);
    const audioMsgId = `audio-${Date.now()}`;

    // 1. User sends a 45-second raw voice note
    const userAudioMsg: TelegramMessage = {
      id: audioMsgId,
      sender: "user",
      isAudio: true,
      audioDuration: "0:45",
      timestamp: "Just now",
      tag: "VOICE NOTE (45s)",
    };

    setMessages((prev) => [...prev, userAudioMsg]);

    // 2. Simulate Aegis chunking & transcription in stages
    setTimeout(() => {
      setMessages((prev) =>
        prev.map((m) =>
          m.id === audioMsgId
            ? {
                ...m,
                chunks: [
                  { id: "chunk_001.ogg", duration: "25.0s", status: "Transcribed via Whisper" },
                  { id: "chunk_002.ogg", duration: "20.0s", status: "Transcribed via Whisper" },
                ],
                transcript:
                  "\"aegis: fix memory leak in test_token_guard and run full test suite with unslop gate\"",
              }
            : m
        )
      );

      // 3. Bot responds with execution acknowledgement
      setTimeout(() => {
        const botReply: TelegramMessage = {
          id: `bot-${Date.now()}`,
          sender: "bot",
          text: "🚀 Voice Directive Accepted (45s sliced into 2 deterministic chunks):\n• Dispatched to Tier 2 Subagent\n• Invoking hermes chat for code correction\n• 4-Decision Quality Architecture Gate: PASSED\n• pytest: 286/286 PASSED in 51.7s",
          timestamp: "Just now",
          tag: "AUTO-EXECUTE",
        };
        setMessages((prev) => [...prev, botReply]);
        setSimulatingAudio(false);
      }, 1200);
    }, 1500);
  };

  const handleSimulateInterrupt = () => {
    const userMsg: TelegramMessage = {
      id: `user-${Date.now()}`,
      sender: "user",
      text: "/type git status /alt+m",
      timestamp: "Just now",
      tag: "IN-FLIGHT INTERRUPT",
    };

    setMessages((prev) => [...prev, userMsg]);

    setTimeout(() => {
      const botReply: TelegramMessage = {
        id: `bot-${Date.now()}`,
        sender: "bot",
        text: "⌨️ Injected keystrokes directly into active Antigravity CLI session:\n$ git status\nOn branch main\nnothing to commit, working tree clean",
        timestamp: "Just now",
        tag: "STDOUT STREAM",
      };
      setMessages((prev) => [...prev, botReply]);
    }, 900);
  };

  const handleSimulateBriefing = () => {
    const userMsg: TelegramMessage = {
      id: `user-${Date.now()}`,
      sender: "user",
      text: "/briefing",
      timestamp: "Just now",
      tag: "COMMAND",
    };

    setMessages((prev) => [...prev, userMsg]);

    setTimeout(() => {
      const botReply: TelegramMessage = {
        id: `bot-${Date.now()}`,
        sender: "bot",
        text: "🛡️ AegisBrain 24/7 Radar:\n1. Latest Snapshot: snap-2026-11-08-01\n2. Tech Radar: LocalLLaMA trending Qwen 2.5 Coder 32B\n3. Scheduled Task: AegisBrainDaemonKeepAlive Active (Every 5 min)\n4. Token Arbitrage: $1,840/mo saved",
        timestamp: "Just now",
        tag: "BRIEFING DIGEST",
      };
      setMessages((prev) => [...prev, botReply]);
    }, 900);
  };

  const handleVoiceComplete = (transcribed: string) => {
    const userAudioMsg: TelegramMessage = {
      id: `voice-pill-${Date.now()}`,
      sender: "user",
      isAudio: true,
      audioDuration: "0:24",
      chunks: [
        { id: "chunk_live.ogg", duration: "24.0s", status: "Deterministic Whisper Shield" },
      ],
      transcript: transcribed,
      timestamp: "Just now",
      tag: "LIVE MIC TRANSCRIPT",
    };
    setMessages((prev) => [...prev, userAudioMsg]);

    setTimeout(() => {
      const botReply: TelegramMessage = {
        id: `bot-voice-${Date.now()}`,
        sender: "bot",
        text: `⚡ Directive Executed: "${transcribed}"\n• Processed locally via Whisper STT (0 cloud tokens)\n• Dispatched to Tier 3 Worker CLI (hermes chat)\n• Dual-environment verification: 100% clean`,
        timestamp: "Just now",
        tag: "AUTONOMOUS AGENT",
      };
      setMessages((prev) => [...prev, botReply]);
    }, 1100);
  };

  const handleSendCustom = (e: React.FormEvent) => {
    e.preventDefault();
    if (!customText.trim()) return;

    const userMsg: TelegramMessage = {
      id: `custom-${Date.now()}`,
      sender: "user",
      text: customText,
      timestamp: "Just now",
      tag: customText.startsWith("/") ? "COMMAND" : "INBOX MESSAGE",
    };

    setMessages((prev) => [...prev, userMsg]);
    const currentInput = customText;
    setCustomText("");

    setTimeout(() => {
      const botReply: TelegramMessage = {
        id: `bot-resp-${Date.now()}`,
        sender: "bot",
        text: currentInput.startsWith("/recall")
          ? "🔍 Sub-second recall: retrieved 4 AST symbols from brain.db in 22ms. Invariants restored."
          : `⚡ Message queued into telegram_inbox in brain.db. Dispatched to background execution queue.`,
        timestamp: "Just now",
        tag: "TELEGRAM DAEMON",
      };
      setMessages((prev) => [...prev, botReply]);
    }, 800);
  };

  return (
    <div className="w-full">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: Interactive Command Triggers (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          <div className="bg-[#101015] border-2 border-black shadow-[6px_6px_0px_#000000] p-5 rounded-lg space-y-3">
            <h3 className="font-nikkei text-sm font-bold uppercase tracking-wider text-black bg-[#FBF9F5] border border-black px-3 py-1 inline-flex items-center gap-2 shadow-[2px_2px_0px_#000000]">
              <Zap className="w-4 h-4 text-[#B91C1C]" />
              Simulation Triggers
            </h3>
            <p className="text-xs text-zinc-300 font-gt-era leading-relaxed">
              Test AegisBrain&apos;s 24/7 Telegram companion capabilities. Slices audio notes deterministically, runs local Whisper STT, and injects in-flight commands.
            </p>

            <div className="space-y-2.5 pt-2">
              {/* Trigger 1: 45s Audio */}
              <button
                onClick={handleSimulateAudio}
                disabled={simulatingAudio}
                className="w-full p-3 rounded bg-[#181822] hover:bg-[#222230] border-2 border-black hover:border-[#B91C1C] text-left transition-all group flex items-center justify-between shadow-[3px_3px_0px_#000000]"
              >
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded bg-[#B91C1C]/20 text-[#B91C1C] border border-[#B91C1C]/40">
                    <FileAudio className="w-4 h-4" />
                  </div>
                  <div>
                    <div className="text-xs font-bold text-white group-hover:text-[#B91C1C] font-mono">
                      Simulate 45s Voice Note
                    </div>
                    <div className="text-[11px] text-zinc-400">
                      Tests deterministic 25s slicing + Whisper STT
                    </div>
                  </div>
                </div>
                <span className="text-xs font-mono text-[#B91C1C] font-bold">Run →</span>
              </button>

              {/* Trigger 2: In-flight /type */}
              <button
                onClick={handleSimulateInterrupt}
                className="w-full p-3 rounded bg-[#181822] hover:bg-[#222230] border-2 border-black hover:border-[#10B981] text-left transition-all group flex items-center justify-between shadow-[3px_3px_0px_#000000]"
              >
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">
                    <Terminal className="w-4 h-4" />
                  </div>
                  <div>
                    <div className="text-xs font-bold text-white group-hover:text-emerald-300 font-mono">
                      In-Flight /type /alt+m Interrupt
                    </div>
                    <div className="text-[11px] text-zinc-400">
                      Inject keystrokes directly into active CLI
                    </div>
                  </div>
                </div>
                <span className="text-xs font-mono text-emerald-400 font-bold">Run →</span>
              </button>

              {/* Trigger 3: /briefing */}
              <button
                onClick={handleSimulateBriefing}
                className="w-full p-3 rounded bg-[#181822] hover:bg-[#222230] border-2 border-black hover:border-[#F59E0B] text-left transition-all group flex items-center justify-between shadow-[3px_3px_0px_#000000]"
              >
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded bg-amber-500/20 text-amber-400 border border-amber-500/40">
                    <Sparkles className="w-4 h-4" />
                  </div>
                  <div>
                    <div className="text-xs font-bold text-white group-hover:text-amber-300 font-mono">
                      Run /briefing Task Status
                    </div>
                    <div className="text-[11px] text-zinc-400">
                      Zero-prompt offline milestone & snapshot digest
                    </div>
                  </div>
                </div>
                <span className="text-xs font-mono text-amber-400 font-bold">Run →</span>
              </button>
            </div>
          </div>

          {/* Key Specs Card */}
          <div className="bg-[#101015] p-4 rounded-lg border-2 border-black shadow-[4px_4px_0px_#000000] space-y-2 font-mono text-xs">
            <div className="flex items-center justify-between text-zinc-400">
              <span>Listener Daemon:</span>
              <span className="text-emerald-400 font-semibold">aegis.server (:8765)</span>
            </div>
            <div className="flex items-center justify-between text-zinc-400">
              <span>Audio Slicer:</span>
              <span className="text-[#B91C1C] font-semibold">FFmpeg deterministic 25s</span>
            </div>
            <div className="flex items-center justify-between text-zinc-400">
              <span>STT Engine:</span>
              <span className="text-white font-semibold">Local Whisper ($0.00 cloud cost)</span>
            </div>
            <div className="flex items-center justify-between text-zinc-400">
              <span>In-Flight Control:</span>
              <span className="text-amber-400 font-semibold">/type &lt;cmd&gt; /alt+m</span>
            </div>
          </div>
        </div>

        {/* Right Column: Realistic Smartphone Mockup with React Bits VoicePill (7 cols) */}
        <div className="lg:col-span-7 flex justify-center">
          <div className="w-full max-w-[390px] rounded-[44px] p-3 bg-[#000000] border-4 border-black shadow-[10px_10px_0px_#000000] relative overflow-hidden">
            {/* Dynamic Island / Speaker Notch */}
            <div className="absolute top-5 left-1/2 -translate-x-1/2 w-28 h-6 bg-black rounded-full z-20 flex items-center justify-center border border-zinc-800">
              <div className="w-2.5 h-2.5 rounded-full bg-zinc-900 border border-zinc-700 mr-2" />
              <div className="w-10 h-1 bg-zinc-900 rounded-full" />
            </div>

            {/* Screen Content Container */}
            <div className="w-full h-[580px] bg-[#121217] rounded-[36px] overflow-hidden flex flex-col pt-8 pb-3 px-3 relative border border-white/10">
              {/* Telegram Header */}
              <div className="flex items-center justify-between py-2.5 border-b border-white/10 mb-2">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-full bg-[#B91C1C] border border-black flex items-center justify-center font-bold text-white text-xs shadow-[2px_2px_0px_#000000]">
                    AB
                  </div>
                  <div>
                    <div className="text-xs font-bold text-white flex items-center gap-1.5 font-mono">
                      @HHAACLIBot
                      <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                    </div>
                    <div className="text-[10px] text-zinc-400">Aegis 24/7 Mobile Daemon</div>
                  </div>
                </div>
                <div className="text-[10px] font-mono text-zinc-400 bg-black/40 px-2 py-0.5 rounded border border-white/10">
                  ONLINE
                </div>
              </div>

              {/* Telegram Messages Feed */}
              <div className="flex-1 overflow-y-auto py-2 space-y-2.5 text-xs pr-1">
                {messages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex flex-col ${
                      msg.sender === "user" ? "items-end" : "items-start"
                    }`}
                  >
                    <div
                      className={`max-w-[88%] rounded-2xl px-3 py-2 text-xs border ${
                        msg.sender === "user"
                          ? "bg-[#B91C1C] border-black text-white rounded-br-xs shadow-[2px_2px_0px_#000000]"
                          : "bg-[#181822] border-black text-zinc-200 rounded-bl-xs shadow-[2px_2px_0px_#000000]"
                      }`}
                    >
                      {/* Tag pill if available */}
                      {msg.tag && (
                        <div className="inline-block text-[9px] font-mono px-1.5 py-0.5 rounded bg-black/40 text-amber-300 border border-white/10 mb-1">
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
                        <div className="whitespace-pre-line leading-relaxed font-mono text-[11px]">{msg.text}</div>
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
                        <div className="mt-2 p-2 rounded bg-black/60 border border-white/20 font-mono text-[10px] text-emerald-300">
                          <div className="text-[9px] text-zinc-400 uppercase tracking-wider mb-0.5">
                            Local Whisper Transcript:
                          </div>
                          {msg.transcript}
                        </div>
                      )}

                      {/* Message Footer / Timestamp */}
                      <div className="flex items-center justify-end gap-1 mt-1 text-[9px] text-zinc-400 font-mono">
                        <span>{msg.timestamp}</span>
                        {msg.sender === "user" && <CheckCheck className="w-3 h-3 text-white" />}
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* React Bits VoicePill & Telegram Input Bar */}
              <div className="pt-2 border-t border-white/10 space-y-2">
                {/* Embedded VoicePill */}
                <div className="flex justify-center">
                  <VoicePill onTranscriptionComplete={handleVoiceComplete} />
                </div>

                <form onSubmit={handleSendCustom} className="flex items-center gap-2">
                  <input
                    type="text"
                    value={customText}
                    onChange={(e) => setCustomText(e.target.value)}
                    placeholder="Message @HHAACLIBot or /recall..."
                    className="flex-1 bg-black border border-white/20 rounded-full px-3.5 py-1.5 text-xs text-white placeholder:text-zinc-500 focus:outline-none focus:border-[#B91C1C] font-mono"
                  />
                  <button
                    type="submit"
                    className="p-2 rounded-full bg-[#B91C1C] text-white hover:bg-red-700 transition-colors border border-black shadow-[2px_2px_0px_#000000]"
                  >
                    <Send className="w-3.5 h-3.5" />
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default TelegramSimulator;
