"use client";

import React, { useEffect, useRef } from "react";
import { Volume2, VolumeX } from "lucide-react";

interface SoundtrackControllerProps {
  soundActive: boolean;
  onToggleSound: (active: boolean) => void;
}

export function SoundtrackController({
  soundActive,
  onToggleSound,
}: SoundtrackControllerProps) {
  const audioCtxRef = useRef<AudioContext | null>(null);

  // Initialize Web Audio context on user demand
  const getAudioContext = () => {
    if (!audioCtxRef.current) {
      const AudioCtx =
        window.AudioContext ||
        (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      audioCtxRef.current = new AudioCtx();
    }
    if (audioCtxRef.current.state === "suspended") {
      audioCtxRef.current.resume();
    }
    return audioCtxRef.current;
  };

  // Pure tactile mechanical click & UI interaction sound synthesizer (Zero background noise)
  useEffect(() => {
    const handlePlaySfx = (e: CustomEvent<{ name: string }>) => {
      if (!soundActive) return;
      try {
        const ctx = getAudioContext();
        const sfxName = e.detail?.name || "click";

        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        if (sfxName === "click" || sfxName === "tab") {
          // Crisp mechanical tactile impulse (like a precision Leica shutter)
          osc.type = "sine";
          osc.frequency.setValueAtTime(820, ctx.currentTime);
          osc.frequency.exponentialRampToValueAtTime(240, ctx.currentTime + 0.035);
          gain.gain.setValueAtTime(0.18, ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.035);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start();
          osc.stop(ctx.currentTime + 0.04);
        } else if (sfxName === "transition" || sfxName === "expand") {
          // Subtle resonant paper / deckle slide thump
          osc.type = "triangle";
          osc.frequency.setValueAtTime(160, ctx.currentTime);
          osc.frequency.exponentialRampToValueAtTime(55, ctx.currentTime + 0.18);
          gain.gain.setValueAtTime(0.2, ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.18);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start();
          osc.stop(ctx.currentTime + 0.19);
        } else if (sfxName === "success" || sfxName === "done") {
          // High chime harmonic
          osc.type = "sine";
          osc.frequency.setValueAtTime(520, ctx.currentTime);
          osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.12);
          gain.gain.setValueAtTime(0.14, ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.12);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start();
          osc.stop(ctx.currentTime + 0.13);
        }
      } catch (err) {
        console.warn("SFX error:", err);
      }
    };

    window.addEventListener("aegis-play-sfx", handlePlaySfx as EventListener);
    return () => {
      window.removeEventListener("aegis-play-sfx", handlePlaySfx as EventListener);
    };
  }, [soundActive]);

  return (
    <div className="fixed bottom-6 right-6 z-50 pointer-events-auto">
      <button
        onClick={() => {
          const nextState = !soundActive;
          onToggleSound(nextState);
          if (nextState) {
            triggerSoundEffect("click");
          }
        }}
        className="group relative flex items-center justify-center p-3 rounded-md bg-[#0B0B0E]/90 border border-white/20 hover:border-white/60 shadow-[4px_4px_0px_#000000] backdrop-blur-md transition-all cursor-pointer select-none"
        title={soundActive ? "Mute Click Sound Effects" : "Enable Tactile Click SFX"}
        aria-label="Toggle Sound Effects"
      >
        {soundActive ? (
          <Volume2 className="w-4 h-4 text-[#B91C1C] animate-pulse" />
        ) : (
          <VolumeX className="w-4 h-4 text-white/50 group-hover:text-white transition-colors" />
        )}
      </button>
    </div>
  );
}

export function triggerSoundEffect(
  name: "click" | "transition" | "expand" | "success" | "tab" | "textbox" | "beam" = "click"
) {
  if (typeof window !== "undefined") {
    window.dispatchEvent(
      new CustomEvent("aegis-play-sfx", { detail: { name } })
    );
  }
}
