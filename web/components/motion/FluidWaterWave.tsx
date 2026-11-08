"use client";

import React from "react";
import { motion } from "motion/react";

interface FluidWaterWaveProps {
  fillColor?: string;
  className?: string;
}

export function FluidWaterWave({
  fillColor = "#FBF9F5",
  className = "",
}: FluidWaterWaveProps) {
  return (
    <div
      className={`relative w-full overflow-hidden pointer-events-none select-none ${className}`}
      aria-hidden="true"
    >
      {/* Billowing Multi-Layer Liquid Fluid Waves */}
      <svg
        viewBox="0 0 1440 320"
        className="w-full h-auto min-h-[160px] sm:min-h-[220px] text-white fill-current filter drop-shadow-[0_-12px_24px_rgba(0,0,0,0.6)]"
        preserveAspectRatio="none"
      >
        <defs>
          <linearGradient id="waveGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#FFFFFF" stopOpacity="0.95" />
            <stop offset="60%" stopColor={fillColor} stopOpacity="1" />
            <stop offset="100%" stopColor={fillColor} stopOpacity="1" />
          </linearGradient>
          <linearGradient id="crestHighlight" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#B91C1C" stopOpacity="0.4" />
            <stop offset="35%" stopColor="#FFFFFF" stopOpacity="0.9" />
            <stop offset="70%" stopColor="#10B981" stopOpacity="0.3" />
            <stop offset="100%" stopColor="#FFFFFF" stopOpacity="0.9" />
          </linearGradient>
        </defs>

        {/* Deep Background Liquid Wave (Lower Opacity) */}
        <motion.path
          animate={{
            d: [
              "M0,320 L1440,320 L1440,160 C1360,190 1280,120 1200,140 C1100,165 1020,110 940,135 C860,160 800,120 720,130 C640,140 580,180 500,160 C420,140 360,110 280,130 C200,150 120,170 0,150 Z",
              "M0,320 L1440,320 L1440,140 C1360,120 1280,170 1200,155 C1100,135 1020,175 940,150 C860,125 800,160 720,145 C640,130 580,150 500,135 C420,120 360,160 280,145 C200,130 120,145 0,135 Z",
              "M0,320 L1440,320 L1440,160 C1360,190 1280,120 1200,140 C1100,165 1020,110 940,135 C860,160 800,120 720,130 C640,140 580,180 500,160 C420,140 360,110 280,130 C200,150 120,170 0,150 Z",
            ],
          }}
          transition={{ duration: 16, repeat: Infinity, ease: "easeInOut" }}
          fill="rgba(255, 255, 255, 0.45)"
        />

        {/* Foreground Monumental Billowing Crest */}
        <motion.path
          animate={{
            d: [
              "M0,320 L1440,320 L1440,190 C1380,180 1340,130 1280,140 C1220,150 1190,210 1130,200 C1070,190 1040,110 970,120 C900,130 870,220 800,210 C730,200 700,90 620,100 C540,110 510,190 440,180 C370,170 340,70 260,90 C180,110 140,210 80,190 C40,175 20,230 0,220 Z",
              "M0,320 L1440,320 L1440,175 C1380,195 1340,150 1280,135 C1220,120 1190,190 1130,185 C1070,180 1040,130 970,140 C900,150 870,200 800,190 C730,180 700,110 620,120 C540,130 510,175 440,165 C370,155 340,90 260,105 C180,120 140,190 80,175 C40,160 20,215 0,205 Z",
              "M0,320 L1440,320 L1440,190 C1380,180 1340,130 1280,140 C1220,150 1190,210 1130,200 C1070,190 1040,110 970,120 C900,130 870,220 800,210 C730,200 700,90 620,100 C540,110 510,190 440,180 C370,170 340,70 260,90 C180,110 140,210 80,190 C40,175 20,230 0,220 Z",
            ],
          }}
          transition={{ duration: 12, repeat: Infinity, ease: "easeInOut" }}
          fill="url(#waveGradient)"
        />

      </svg>
    </div>
  );
}
