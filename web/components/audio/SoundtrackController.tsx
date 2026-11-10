"use client";

import React, { useEffect, useRef } from "react";
import { Volume2, VolumeX } from "lucide-react";

interface SoundtrackControllerProps {
  soundActive: boolean;
  onToggleSound: (active: boolean) => void;
}

export type SfxName =
  | "click"
  | "transition"
  | "expand"
  | "success"
  | "done"
  | "tab"
  | "worker"
  | "gate"
  | "whoosh"
  | "textbox"
  | "beam"
  | "hover";

export function SoundtrackController({
  soundActive,
  onToggleSound,
}: SoundtrackControllerProps) {
  const audioCtxRef = useRef<AudioContext | null>(null);
  const bgAudioRef = useRef<HTMLAudioElement | null>(null);
  const lastWhooshRef = useRef<number>(0);

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

  // Continuous subtle atmospheric background music
  useEffect(() => {
    const bgAudio = new Audio("/audio/ambient-drone.mp3");
    bgAudio.loop = true;
    bgAudio.volume = 0;
    bgAudioRef.current = bgAudio;

    return () => {
      bgAudio.pause();
      bgAudio.src = "";
    };
  }, []);

  // Sync background ambient music with soundActive toggle
  useEffect(() => {
    const audio = bgAudioRef.current;
    if (!audio) return;

    if (soundActive) {
      audio
        .play()
        .then(() => {
          let v = 0;
          const fade = setInterval(() => {
            v = Math.min(v + 0.015, 0.12);
            if (audio) audio.volume = v;
            if (v >= 0.12) clearInterval(fade);
          }, 80);
        })
        .catch(() => {
          // Awaiting user gesture
        });
    } else {
      let v = audio.volume;
      const fade = setInterval(() => {
        v = Math.max(v - 0.02, 0);
        if (audio) audio.volume = v;
        if (v <= 0) {
          clearInterval(fade);
          audio.pause();
        }
      }, 60);
    }
  }, [soundActive]);

  // Auto-unlock audio context and start music on first user gesture if active
  useEffect(() => {
    const handleFirstGesture = () => {
      try {
        const ctx = getAudioContext();
        if (ctx && ctx.state === "suspended") {
          ctx.resume();
        }
        if (soundActive && bgAudioRef.current && bgAudioRef.current.paused) {
          bgAudioRef.current.play().catch(() => {});
        }
      } catch (err) {
        console.warn("Audio unlock err:", err);
      }
    };

    window.addEventListener("pointerdown", handleFirstGesture, { once: true });
    window.addEventListener("keydown", handleFirstGesture, { once: true });
    return () => {
      window.removeEventListener("pointerdown", handleFirstGesture);
      window.removeEventListener("keydown", handleFirstGesture);
    };
  }, [soundActive]);

  // Dedicated hover SFX listener: triggers on buttons, links, and tabs
  useEffect(() => {
    let lastTarget: Element | null = null;
    let lastHoverTime = 0;
    const handleMouseOver = (e: MouseEvent) => {
      if (!soundActive) return;
      const target = (e.target as HTMLElement | null)?.closest?.(
        "button, a[href], [role='button'], [role='tab'], input[type='range']"
      );
      if (!target) {
        lastTarget = null;
        return;
      }
      if (target === lastTarget) return;
      lastTarget = target;
      const now = performance.now();
      if (now - lastHoverTime < 90) return;
      lastHoverTime = now;
      triggerSoundEffect("hover");
    };

    window.addEventListener("mouseover", handleMouseOver, { passive: true });
    return () => {
      window.removeEventListener("mouseover", handleMouseOver);
    };
  }, [soundActive]);

  // Universal Click SFX Listener with event capture: ensures EVERY button/link has satisfying feedback
  useEffect(() => {
    let lastClickTime = 0;
    const handleClick = (e: MouseEvent) => {
      if (!soundActive) return;
      const target = (e.target as HTMLElement | null)?.closest?.(
        "button, a[href], [role='button'], [role='tab']"
      );
      if (!target) return;
      const now = performance.now();
      if (now - lastClickTime < 60) return; // Debounce double clicks
      lastClickTime = now;
      triggerSoundEffect("click");
    };

    window.addEventListener("click", handleClick, { capture: true, passive: true });
    return () => {
      window.removeEventListener("click", handleClick, { capture: true });
    };
  }, [soundActive]);

  // High-fidelity tactile sound synthesizer (Zero boring beeps; rich mechanical snap & cinematic whoosh)
  useEffect(() => {
    const handlePlaySfx = (e: CustomEvent<{ name: SfxName }>) => {
      if (!soundActive) return;
      try {
        const ctx = getAudioContext();
        const sfxName = e.detail?.name || "click";

        if (sfxName === "hover") {
          // Ultra-subtle, gentle tactile micro-tick
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = "sine";
          osc.frequency.setValueAtTime(520, ctx.currentTime);
          osc.frequency.exponentialRampToValueAtTime(680, ctx.currentTime + 0.012);
          gain.gain.setValueAtTime(0.015, ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.012);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start();
          osc.stop(ctx.currentTime + 0.014);
        } else if (sfxName === "whoosh") {
          // Subtle, very light cinematic whoosh sound for elements transitioning into view
          const now = performance.now();
          if (now - lastWhooshRef.current < 550) return;
          lastWhooshRef.current = now;

          const bufferSize = Math.floor(ctx.sampleRate * 0.38);
          const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
          const data = buffer.getChannelData(0);
          for (let i = 0; i < bufferSize; i++) {
            data[i] = (Math.random() * 2 - 1) * 0.45;
          }
          const noise = ctx.createBufferSource();
          noise.buffer = buffer;

          const filter = ctx.createBiquadFilter();
          filter.type = "bandpass";
          filter.Q.setValueAtTime(1.4, ctx.currentTime);
          filter.frequency.setValueAtTime(190, ctx.currentTime);
          filter.frequency.exponentialRampToValueAtTime(760, ctx.currentTime + 0.16);
          filter.frequency.exponentialRampToValueAtTime(130, ctx.currentTime + 0.38);

          const gain = ctx.createGain();
          gain.gain.setValueAtTime(0.0001, ctx.currentTime);
          gain.gain.linearRampToValueAtTime(0.038, ctx.currentTime + 0.15);
          gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.38);

          noise.connect(filter);
          filter.connect(gain);
          gain.connect(ctx.destination);
          noise.start();
          noise.stop(ctx.currentTime + 0.39);
        } else if (sfxName === "worker") {
          // Rich mechanical toggle for Tier 3 Execution Workers (Hermes, Ollama, OpenCode)
          const osc1 = ctx.createOscillator();
          const gain1 = ctx.createGain();
          osc1.type = "sine";
          osc1.frequency.setValueAtTime(1400, ctx.currentTime);
          osc1.frequency.exponentialRampToValueAtTime(320, ctx.currentTime + 0.02);
          gain1.gain.setValueAtTime(0.18, ctx.currentTime);
          gain1.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.02);
          osc1.connect(gain1);
          gain1.connect(ctx.destination);
          osc1.start();
          osc1.stop(ctx.currentTime + 0.025);

          const osc2 = ctx.createOscillator();
          const gain2 = ctx.createGain();
          osc2.type = "triangle";
          osc2.frequency.setValueAtTime(320, ctx.currentTime);
          osc2.frequency.exponentialRampToValueAtTime(110, ctx.currentTime + 0.045);
          gain2.gain.setValueAtTime(0.16, ctx.currentTime);
          gain2.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.045);
          osc2.connect(gain2);
          gain2.connect(ctx.destination);
          osc2.start();
          osc2.stop(ctx.currentTime + 0.05);
        } else if (sfxName === "gate") {
          // Double precision inspection shutter tick (Karpathy simplicity, Watermark scrubber, etc.)
          const oscA = ctx.createOscillator();
          const gainA = ctx.createGain();
          oscA.type = "sine";
          oscA.frequency.setValueAtTime(920, ctx.currentTime);
          gainA.gain.setValueAtTime(0.15, ctx.currentTime);
          gainA.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.01);
          oscA.connect(gainA);
          gainA.connect(ctx.destination);
          oscA.start();
          oscA.stop(ctx.currentTime + 0.012);

          const oscB = ctx.createOscillator();
          const gainB = ctx.createGain();
          oscB.type = "sine";
          oscB.frequency.setValueAtTime(1250, ctx.currentTime + 0.014);
          oscB.frequency.exponentialRampToValueAtTime(450, ctx.currentTime + 0.035);
          gainB.gain.setValueAtTime(0.14, ctx.currentTime + 0.014);
          gainB.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.035);
          oscB.connect(gainB);
          gainB.connect(ctx.destination);
          oscB.start(ctx.currentTime + 0.014);
          oscB.stop(ctx.currentTime + 0.038);
        } else if (sfxName === "tab") {
          // Resonant pneumatic card / tab slide snap
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = "triangle";
          osc.frequency.setValueAtTime(540, ctx.currentTime);
          osc.frequency.exponentialRampToValueAtTime(210, ctx.currentTime + 0.035);
          gain.gain.setValueAtTime(0.16, ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.035);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start();
          osc.stop(ctx.currentTime + 0.04);
        } else if (sfxName === "click") {
          // Tactile mechanical precision switch (sharp snap + body resonance)
          const osc1 = ctx.createOscillator();
          const gain1 = ctx.createGain();
          osc1.type = "sine";
          osc1.frequency.setValueAtTime(1200, ctx.currentTime);
          osc1.frequency.exponentialRampToValueAtTime(360, ctx.currentTime + 0.018);
          gain1.gain.setValueAtTime(0.14, ctx.currentTime);
          gain1.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.018);
          osc1.connect(gain1);
          gain1.connect(ctx.destination);
          osc1.start();
          osc1.stop(ctx.currentTime + 0.02);

          const osc2 = ctx.createOscillator();
          const gain2 = ctx.createGain();
          osc2.type = "triangle";
          osc2.frequency.setValueAtTime(260, ctx.currentTime);
          osc2.frequency.exponentialRampToValueAtTime(95, ctx.currentTime + 0.03);
          gain2.gain.setValueAtTime(0.12, ctx.currentTime);
          gain2.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.03);
          osc2.connect(gain2);
          gain2.connect(ctx.destination);
          osc2.start();
          osc2.stop(ctx.currentTime + 0.032);
        } else if (sfxName === "transition" || sfxName === "expand") {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = "triangle";
          osc.frequency.setValueAtTime(160, ctx.currentTime);
          osc.frequency.exponentialRampToValueAtTime(55, ctx.currentTime + 0.18);
          gain.gain.setValueAtTime(0.18, ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.18);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start();
          osc.stop(ctx.currentTime + 0.19);
        } else if (sfxName === "success" || sfxName === "done") {
          // Bright dual chime (659Hz E5 -> 880Hz A5)
          const osc1 = ctx.createOscillator();
          const gain1 = ctx.createGain();
          osc1.type = "sine";
          osc1.frequency.setValueAtTime(659, ctx.currentTime);
          gain1.gain.setValueAtTime(0.12, ctx.currentTime);
          gain1.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.08);
          osc1.connect(gain1);
          gain1.connect(ctx.destination);
          osc1.start();
          osc1.stop(ctx.currentTime + 0.09);

          const osc2 = ctx.createOscillator();
          const gain2 = ctx.createGain();
          osc2.type = "sine";
          osc2.frequency.setValueAtTime(880, ctx.currentTime + 0.06);
          gain2.gain.setValueAtTime(0.14, ctx.currentTime + 0.06);
          gain2.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.2);
          osc2.connect(gain2);
          gain2.connect(ctx.destination);
          osc2.start(ctx.currentTime + 0.06);
          osc2.stop(ctx.currentTime + 0.22);
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
        title={soundActive ? "Mute Atmospheric Sound" : "Enable Sound Atmosphere & SFX"}
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

export function triggerSoundEffect(name: SfxName = "click") {
  if (typeof window !== "undefined") {
    window.dispatchEvent(
      new CustomEvent("aegis-play-sfx", { detail: { name } })
    );
  }
}
