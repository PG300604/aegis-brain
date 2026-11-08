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
  const droneRef = useRef<HTMLAudioElement | null>(null);
  const windRef = useRef<HTMLAudioElement | null>(null);

  // Initialize background audio elements
  useEffect(() => {
    const drone = new Audio("/audio/ambient-drone.mp3");
    drone.loop = true;
    drone.volume = 0.28;
    droneRef.current = drone;

    const wind = new Audio("/audio/ambient-wind.mp3");
    wind.loop = true;
    wind.volume = 0.12;
    windRef.current = wind;

    return () => {
      drone.pause();
      drone.src = "";
      wind.pause();
      wind.src = "";
    };
  }, []);

  // Handle play / pause based on user sound toggle
  useEffect(() => {
    if (soundActive) {
      droneRef.current?.play().catch(() => {
        // Autoplay policy fallback
      });
      windRef.current?.play().catch(() => {});
    } else {
      droneRef.current?.pause();
      windRef.current?.pause();
    }
  }, [soundActive]);

  // Global sound effect listener
  useEffect(() => {
    const handlePlaySfx = (e: CustomEvent<{ name: string }>) => {
      if (!soundActive) return;
      const sfxName = e.detail?.name || "ui-click";
      let audioFile = "/audio/ui-click.mp3";
      let vol = 0.4;

      if (sfxName === "crack" || sfxName === "transition") {
        audioFile = "/audio/transition-crack.mp3";
        vol = 0.55;
      } else if (sfxName === "textbox" || sfxName === "type") {
        audioFile = "/audio/textbox.mp3";
        vol = 0.35;
      } else if (sfxName === "beam") {
        audioFile = "/audio/beam.mp3";
        vol = 0.45;
      }

      const sfx = new Audio(audioFile);
      sfx.volume = vol;
      sfx.play().catch(() => {});
    };

    window.addEventListener("aegis-play-sfx", handlePlaySfx as EventListener);
    return () => {
      window.removeEventListener("aegis-play-sfx", handlePlaySfx as EventListener);
    };
  }, [soundActive]);

  return (
    <>
      {/* Floating Bottom-Right Santioni Equalizer Button */}
      <div className="fixed bottom-6 right-6 z-50 pointer-events-auto">
        <button
          onClick={() => {
            const nextState = !soundActive;
            onToggleSound(nextState);
            if (nextState) {
              window.dispatchEvent(
                new CustomEvent("aegis-play-sfx", { detail: { name: "click" } })
              );
            }
          }}
          className="group relative flex items-center justify-center p-3 rounded-md bg-[#0B0B0E]/90 border border-white/20 hover:border-white/60 shadow-[4px_4px_0px_#000000] backdrop-blur-md transition-all cursor-pointer select-none"
          title={soundActive ? "Mute Atmospheric Sound" : "Listen to Experience Soundtrack"}
          aria-label="Toggle Sound"
        >
          {soundActive ? (
            <div className="flex items-end gap-[3px] h-4 w-4 justify-center">
              <span className="w-[2.5px] bg-white rounded-full sound-bar-1 animate-pulse" />
              <span className="w-[2.5px] bg-[#B91C1C] rounded-full sound-bar-2" style={{ animationDuration: "0.8s" }} />
              <span className="w-[2.5px] bg-white rounded-full sound-bar-3" style={{ animationDuration: "1.1s" }} />
            </div>
          ) : (
            <div className="flex items-end gap-[3px] h-4 w-4 justify-center opacity-60 group-hover:opacity-100">
              <span className="w-[2.5px] h-1.5 bg-zinc-400 rounded-full" />
              <span className="w-[2.5px] h-3 bg-zinc-400 rounded-full" />
              <span className="w-[2.5px] h-1 bg-zinc-400 rounded-full" />
            </div>
          )}
        </button>
      </div>
    </>
  );
}

// Global helper to play sound effects from anywhere in the app
export function triggerSoundEffect(name: "click" | "crack" | "transition" | "textbox" | "beam" = "click") {
  if (typeof window !== "undefined") {
    window.dispatchEvent(
      new CustomEvent("aegis-play-sfx", { detail: { name } })
    );
  }
}
