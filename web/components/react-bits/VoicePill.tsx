"use client";

import React, { useState, useEffect } from "react";
import { Mic, Square, Sparkles } from "lucide-react";
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
          className={`p-2 rounded-full flex items-center justify-center transition-all cursor-pointer border-2 border-black ${
            isRecording
              ? "bg-[#B91C1C] text-white shadow-[2px_2px_0px_#000000] animate-pulse"
              : "bg-[#FBF9F5] hover:bg-neutral-100 text-black shadow-[2px_2px_0px_#000000]"
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
          <span className="text-xs font-nikkei uppercase tracking-wider text-black font-bold">
            Whisper Voice Shield
          </span>
        )}

        {/* Status / Timer */}
        <div className="font-mono text-xs font-bold text-black flex items-center gap-1.5 pl-1 border-l-2 border-black/20">
          {isRecording ? (
            <span className="text-[#B91C1C] flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-[#B91C1C] animate-ping" />
              {formatTime(seconds)} / 00:25s
            </span>
          ) : (
            <span className="text-black/60 text-[11px]">25s Max Chunk</span>
          )}
        </div>
      </div>

      {/* Real-time Transcription Chip */}
      {transcribedText && (
        <div className="flex items-center gap-2 px-3 py-1 bg-[#FBF9F5] border-2 border-black rounded-lg shadow-[3px_3px_0px_#000000] text-xs font-mono text-black animate-in fade-in slide-in-from-bottom-1">
          <Sparkles className="w-3.5 h-3.5 text-[#B91C1C]" />
          <span>Whisper STT: <strong className="text-[#B91C1C]">&ldquo;{transcribedText}&rdquo;</strong></span>
        </div>
      )}
    </div>
  );
}
