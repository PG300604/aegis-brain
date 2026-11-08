"use client";

import React, { useEffect, useRef, useState, useCallback } from "react";
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
  const masterGainRef = useRef<GainNode | null>(null);
  const filterNodeRef = useRef<BiquadFilterNode | null>(null);
  const oscillatorsRef = useRef<OscillatorNode[]>([]);

  // Synthesize a custom high-end analog ambient pad soundscape
  const startAtmosphericSynth = useCallback(() => {
    try {
      const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      if (!audioCtxRef.current) {
        audioCtxRef.current = new AudioCtx();
      }
      const ctx = audioCtxRef.current;
      if (ctx.state === "suspended") {
        ctx.resume();
      }

      // Master Gain with smooth fade-in
      const masterGain = ctx.createGain();
      masterGain.gain.setValueAtTime(0.001, ctx.currentTime);
      masterGain.gain.exponentialRampToValueAtTime(0.18, ctx.currentTime + 3.0);
      masterGainRef.current = masterGain;

      // Resonant Lowpass Filter (Moog ladder style cutoff)
      const filter = ctx.createBiquadFilter();
      filter.type = "lowpass";
      filter.frequency.setValueAtTime(380, ctx.currentTime);
      filter.Q.setValueAtTime(3.2, ctx.currentTime);
      filterNodeRef.current = filter;

      // Slow breathing LFO filter modulation
      const lfo = ctx.createOscillator();
      const lfoGain = ctx.createGain();
      lfo.frequency.setValueAtTime(0.06, ctx.currentTime); // 0.06 Hz slow cycle
      lfoGain.gain.setValueAtTime(140, ctx.currentTime);
      lfo.connect(lfoGain);
      lfoGain.connect(filter.frequency);
      lfo.start();

      // Ambient Chord Harmonics (Sub-bass 55Hz, Pad 110Hz, 164.8Hz, 220Hz)
      const frequencies = [55, 110, 164.8, 220, 329.6];
      const oscs: OscillatorNode[] = [];

      frequencies.forEach((freq, idx) => {
        const osc = ctx.createOscillator();
        const oscGain = ctx.createGain();

        // Sub bass is sine wave; upper harmonics are warm detuned triangles
        osc.type = idx === 0 ? "sine" : "triangle";
        osc.frequency.setValueAtTime(freq, ctx.currentTime);
        // Slight subtle analog detuning
        osc.detune.setValueAtTime((idx - 2) * 4.5, ctx.currentTime);

        const level = idx === 0 ? 0.35 : 0.12 / (idx + 0.5);
        oscGain.gain.setValueAtTime(level, ctx.currentTime);

        osc.connect(oscGain);
        oscGain.connect(filter);
        osc.start();
        oscs.push(osc);
      });

      filter.connect(masterGain);
      masterGain.connect(ctx.destination);
      oscillatorsRef.current = oscs;
    } catch (err) {
      console.warn("Web Audio atmospheric engine initialization error:", err);
    }
  }, []);

  const stopAtmosphericSynth = useCallback(() => {
    if (!audioCtxRef.current || !masterGainRef.current) return;
    try {
      const ctx = audioCtxRef.current;
      masterGainRef.current.gain.cancelScheduledValues(ctx.currentTime);
      masterGainRef.current.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 1.2);
      setTimeout(() => {
        oscillatorsRef.current.forEach((osc) => {
          try {
            osc.stop();
            osc.disconnect();
          } catch {}
        });
        oscillatorsRef.current = [];
      }, 1300);
    } catch {}
  }, []);

  // Sync with user sound active state
  useEffect(() => {
    if (soundActive) {
      startAtmosphericSynth();
    } else {
      stopAtmosphericSynth();
    }
    return () => {
      stopAtmosphericSynth();
    };
  }, [soundActive, startAtmosphericSynth, stopAtmosphericSynth]);

  // Interactive Mouse Coupling:
  // Moving the mouse across the page gently shifts the analog filter cutoff
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!soundActive || !filterNodeRef.current || !audioCtxRef.current) return;
      const normalizedY = 1 - e.clientY / window.innerHeight; // 0 to 1
      const targetFreq = 300 + normalizedY * 420; // 300Hz to 720Hz
      filterNodeRef.current.frequency.setTargetAtTime(
        targetFreq,
        audioCtxRef.current.currentTime,
        0.25
      );
    };

    window.addEventListener("mousemove", handleMouseMove, { passive: true });
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, [soundActive]);

  // Global sound effect listener for crisp tactile mechanical clicks
  useEffect(() => {
    const handlePlaySfx = (e: CustomEvent<{ name: string }>) => {
      if (!soundActive) return;
      try {
        const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
        const ctx = audioCtxRef.current || new AudioCtx();
        const sfxName = e.detail?.name || "click";

        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        if (sfxName === "click") {
          // Tactile mechanical key click (800Hz quick impulse)
          osc.type = "sine";
          osc.frequency.setValueAtTime(840, ctx.currentTime);
          osc.frequency.exponentialRampToValueAtTime(220, ctx.currentTime + 0.04);
          gain.gain.setValueAtTime(0.15, ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.04);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start();
          osc.stop(ctx.currentTime + 0.045);
        } else if (sfxName === "transition" || sfxName === "crack") {
          // Deep low-frequency resonant thump
          osc.type = "triangle";
          osc.frequency.setValueAtTime(140, ctx.currentTime);
          osc.frequency.exponentialRampToValueAtTime(45, ctx.currentTime + 0.25);
          gain.gain.setValueAtTime(0.22, ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.25);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start();
          osc.stop(ctx.currentTime + 0.26);
        }
      } catch {}
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
          triggerSoundEffect("click");
        }}
        className="group relative flex items-center justify-center p-3 rounded-md bg-[#0B0B0E]/90 border border-white/20 hover:border-white/60 shadow-[4px_4px_0px_#000000] backdrop-blur-md transition-all cursor-pointer select-none"
        title={soundActive ? "Mute Atmospheric Soundscape" : "Enable Sovereign Ambient Soundscape"}
        aria-label="Toggle Sound"
      >
        {soundActive ? (
          <div className="flex items-end gap-[3px] h-4 w-4 justify-center">
            <span className="w-[3px] bg-[#B91C1C] h-4 animate-pulse" />
            <span className="w-[3px] bg-white h-2 animate-bounce" />
            <span className="w-[3px] bg-[#D4AF37] h-3.5 animate-pulse" />
          </div>
        ) : (
          <VolumeX className="w-4 h-4 text-white/50 group-hover:text-white transition-colors" />
        )}
      </button>
    </div>
  );
}

export function triggerSoundEffect(name: "click" | "transition" | "beam" | "textbox" = "click") {
  if (typeof window !== "undefined") {
    window.dispatchEvent(
      new CustomEvent("aegis-play-sfx", { detail: { name } })
    );
  }
}
