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

        {/* Floating Splatter Ink Droplets rising upwards */}
        <g fill="#FFFFFF">
          <motion.circle
            cx="280"
            cy="50"
            r="14"
            animate={{ y: [-8, 8, -8], opacity: [0.8, 1, 0.8] }}
            transition={{ duration: 4.2, repeat: Infinity, ease: "easeInOut" }}
          />
          <motion.circle
            cx="260"
            cy="20"
            r="7"
            animate={{ y: [-5, 7, -5], opacity: [0.6, 0.9, 0.6] }}
            transition={{ duration: 3.6, repeat: Infinity, ease: "easeInOut", delay: 0.3 }}
          />
          <motion.circle
            cx="610"
            cy="65"
            r="11"
            animate={{ y: [-9, 9, -9], opacity: [0.75, 1, 0.75] }}
            transition={{ duration: 4.8, repeat: Infinity, ease: "easeInOut", delay: 0.7 }}
          />
          <motion.circle
            cx="635"
            cy="35"
            r="5"
            animate={{ y: [-4, 6, -4], opacity: [0.5, 0.8, 0.5] }}
            transition={{ duration: 3.2, repeat: Infinity, ease: "easeInOut", delay: 1.1 }}
          />
          <motion.circle
            cx="985"
            cy="75"
            r="16"
            animate={{ y: [-11, 10, -11], opacity: [0.85, 1, 0.85] }}
            transition={{ duration: 5.1, repeat: Infinity, ease: "easeInOut", delay: 0.2 }}
          />
          <motion.circle
            cx="960"
            cy="45"
            r="8"
            animate={{ y: [-6, 6, -6], opacity: [0.6, 0.9, 0.6] }}
            transition={{ duration: 3.9, repeat: Infinity, ease: "easeInOut", delay: 0.8 }}
          />
          <motion.circle
            cx="1270"
            cy="85"
            r="12"
            animate={{ y: [-8, 7, -8], opacity: [0.7, 1, 0.7] }}
            transition={{ duration: 4.4, repeat: Infinity, ease: "easeInOut", delay: 0.5 }}
          />
          <motion.circle
            cx="1295"
            cy="55"
            r="6"
            animate={{ y: [-4, 5, -4], opacity: [0.5, 0.85, 0.5] }}
            transition={{ duration: 3.4, repeat: Infinity, ease: "easeInOut", delay: 1.3 }}
          />
        </g>
      </svg>
    </div>
  );
}
