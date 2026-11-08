"use client";

import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Mic, MicOff, Square, Send, ChevronLeft, Volume2, Sparkles, Check } from "lucide-react";
import "./VoicePill.css";

interface VoicePillProps {
  onTranscriptionComplete?: (text: string) => void;
  className?: string;
}

export function VoicePill({ onTranscriptionComplete, className = "" }: VoicePillProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [seconds, setSeconds] = useState(0);
  const [transcribedText, setTranscribedText] = useState<string | null>(null);

  // Timer simulation during recording
  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;
    if (isRecording) {
      interval = setInterval(() => {
        setSeconds((prev) => {
          if (prev >= 24) {
            // Reached the 25s chunking shield threshold
            handleFinishRecording();
            return 0;
          }
          return prev + 1;
        });
      }, 1000);
    } else {
      setSeconds(0);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isRecording]);

  const handleToggle = () => {
    if (isRecording) {
      handleFinishRecording();
    } else {
      setIsRecording(true);
      setTranscribedText(null);
    }
  };

  const handleFinishRecording = () => {
    setIsRecording(false);
    const sampleOutputs = [
      "aegis recall 'neural memory benchmark'",
      "aegis challenge src/aegis/memory.py",
      "/type npm run test /alt+m",
      "aegis briefing",
    ];
    const picked = sampleOutputs[Math.floor(Math.random() * sampleOutputs.length)];
    setTranscribedText(picked);
    if (onTranscriptionComplete) {
      onTranscriptionComplete(picked);
    }
  };

  const handleCancel = () => {
    setIsRecording(false);
    setSeconds(0);
    setTranscribedText(null);
  };

  const formatTime = (sec: number) => {
    const mins = Math.floor(sec / 60);
    const remaining = sec % 60;
    return `${mins.toString().padStart(2, "0")}:${remaining.toString().padStart(2, "0")}`;
  };

  return (
    <div className={`voice-pill-container flex flex-col items-center gap-2 ${className}`}>
      <div className={`voice-pill-capsule ${isRecording ? "is-active" : ""}`}>
        {/* Mic / Stop Trigger */}
        <button
          type="button"
          onClick={handleToggle}
          className={`p-2 rounded-full flex items-center justify-center transition-all cursor-pointer ${
            isRecording
              ? "bg-red-500 text-white shadow-[0_0_15px_rgba(239,68,68,0.8)] animate-pulse"
              : "bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 border border-cyan-500/40"
          }`}
          title={isRecording ? "Finish Recording" : "Dictate Audio via Whisper Shield"}
        >
          {isRecording ? <Square className="w-3.5 h-3.5 fill-white" /> : <Mic className="w-3.5 h-3.5" />}
        </button>

        {/* Live Animated Waveform */}
        {isRecording ? (
          <div className="flex items-center gap-1 h-5 px-1">
            <span className="waveform-bar active anim-wave-1" />
            <span className="waveform-bar active anim-wave-2" />
            <span className="waveform-bar active anim-wave-3" />
            <span className="waveform-bar active anim-wave-4" />
            <span className="waveform-bar active anim-wave-5" />
            <span className="waveform-bar active anim-wave-6" />
            <span className="waveform-bar active anim-wave-7" />
            <span className="waveform-bar active anim-wave-8" />
          </div>
        ) : (
          <div className="flex items-center gap-1 h-4 px-1 opacity-50">
            <span className="waveform-bar" style={{ height: "4px" }} />
            <span className="waveform-bar" style={{ height: "8px" }} />
            <span className="waveform-bar" style={{ height: "14px" }} />
            <span className="waveform-bar" style={{ height: "6px" }} />
            <span className="waveform-bar" style={{ height: "10px" }} />
          </div>
        )}

        {/* Elapsed Timer & Whisper Shield Indicator */}
        <div className="font-mono text-xs font-semibold">
          {isRecording ? (
            <span className="text-red-400">
              {formatTime(seconds)}{" "}
              <span className="text-[10px] text-zinc-400 font-normal">/ 00:25s shield</span>
            </span>
          ) : (
            <span className="text-zinc-400">25s Whisper Shield</span>
          )}
        </div>

        {/* Slide-to-cancel or Action button */}
        {isRecording ? (
          <button
            type="button"
            onClick={handleCancel}
            className="slide-cancel-text hover:text-red-300 transition-colors cursor-pointer"
          >
            <ChevronLeft className="w-3.5 h-3.5 text-zinc-400" />
            <span>Cancel</span>
          </button>
        ) : (
          <button
            type="button"
            onClick={handleToggle}
            className="font-mono text-[11px] text-cyan-400 hover:text-cyan-300 flex items-center gap-1 cursor-pointer"
          >
            <span>Record Voice Memo</span>
          </button>
        )}
      </div>

      {/* Transcription Banner Result */}
      <AnimatePresence>
        {transcribedText && (
          <motion.div
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 6 }}
            className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-950/70 border border-emerald-500/30 text-emerald-300 text-xs font-mono"
          >
            <Check className="w-3 h-3 text-emerald-400" />
            <span>Transcribed: &ldquo;{transcribedText}&rdquo;</span>
            <span className="text-[10px] text-zinc-400">(&lt;1.2s transcode)</span>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
