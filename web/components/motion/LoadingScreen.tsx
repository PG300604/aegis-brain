"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";

interface LoadingScreenProps {
  onComplete?: () => void;
}

export function LoadingScreen({ onComplete }: LoadingScreenProps) {
  const [progress, setProgress] = useState<number>(0);
  const [isDone, setIsDone] = useState<boolean>(false);

  useEffect(() => {
    // High-precision smooth numeric increment
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setTimeout(() => {
            setIsDone(true);
            onComplete?.();
          }, 350);
          return 100;
        }
        const increment = prev < 40 ? 3 : prev < 80 ? 4 : 2;
        return Math.min(100, prev + increment);
      });
    }, 25);

    return () => clearInterval(interval);
  }, [onComplete]);

  // Generate 48 sacred geometry radial spokes with deterministic rounding (prevents SSR float hydration diffs)
  const spokes = Array.from({ length: 48 }, (_, i) => {
    const angle = (i * 360) / 48;
    const rad = (angle * Math.PI) / 180;
    const isMajor = i % 4 === 0;
    const rInner = isMajor ? 32 : 44;
    const rOuter = isMajor ? 90 : 82;
    return {
      x1: Math.round((100 + rInner * Math.cos(rad)) * 100) / 100,
      y1: Math.round((100 + rInner * Math.sin(rad)) * 100) / 100,
      x2: Math.round((100 + rOuter * Math.cos(rad)) * 100) / 100,
      y2: Math.round((100 + rOuter * Math.sin(rad)) * 100) / 100,
      isMajor,
    };
  });

  return (
    <AnimatePresence>
      {!isDone && (
        <motion.div
          key="aegis-editorial-loader"
          initial={{ opacity: 1 }}
          exit={{
            y: "-100%",
            transition: { duration: 0.85, ease: [0.76, 0, 0.24, 1] },
          }}
          className="fixed inset-0 z-[100] flex flex-col justify-between p-6 sm:p-12 bg-[#070709] text-[#FAF8F5] select-none pointer-events-auto overflow-hidden"
        >
          {/* Subtle Horizontal Dry-Brush Chalk Background */}
          <div
            className="absolute inset-0 pointer-events-none opacity-15"
            style={{
              backgroundImage: `repeating-linear-gradient(
                0deg,
                transparent,
                transparent 48px,
                rgba(255, 255, 255, 0.03) 48px,
                rgba(255, 255, 255, 0.03) 49px
              )`,
            }}
          />

          {/* 
            ====================================================================
            TOP CENTER: OFFICIAL AEGISBRAIN LOGO LOCKUP (Clean & Sovereign)
            ====================================================================
          */}
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="relative z-10 flex flex-col items-center pt-6 sm:pt-8"
          >
            <div className="flex items-baseline">
              <span className="font-extrabold text-3xl sm:text-4xl text-white tracking-tight">
                AegisBrain
              </span>
              <span className="font-extrabold text-3xl sm:text-4xl text-[#B91C1C]">.</span>
            </div>
          </motion.div>

          {/* 
            ====================================================================
            SCREEN CENTER: SACRED GEOMETRY SUNBURST / LENS EMBLEM (Rotating)
            ====================================================================
          */}
          <div className="relative z-10 my-auto flex flex-col items-center justify-center">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 45, repeat: Infinity, ease: "linear" }}
              className="relative w-48 h-48 sm:w-64 sm:h-64 flex items-center justify-center"
            >
              <svg
                viewBox="0 0 200 200"
                className="w-full h-full text-white drop-shadow-[0_0_20px_rgba(212,175,55,0.2)]"
              >
                {/* Outermost Thin Reference Ring */}
                <circle
                  cx="100"
                  cy="100"
                  r="95"
                  fill="none"
                  stroke="#FAF8F5"
                  strokeWidth="0.8"
                  opacity="0.3"
                />

                {/* Concentric Dashed Ring */}
                <circle
                  cx="100"
                  cy="100"
                  r="90"
                  fill="none"
                  stroke="#D4AF37"
                  strokeWidth="0.75"
                  strokeDasharray="2 4"
                  opacity="0.6"
                />

                {/* Radiating Fine Sunburst Spokes */}
                {spokes.map((spoke, idx) => (
                  <line
                    key={idx}
                    x1={spoke.x1}
                    y1={spoke.y1}
                    x2={spoke.x2}
                    y2={spoke.y2}
                    stroke={spoke.isMajor ? "#FAF8F5" : "#D4AF37"}
                    strokeWidth={spoke.isMajor ? "1" : "0.6"}
                    opacity={spoke.isMajor ? "0.85" : "0.45"}
                  />
                ))}

                {/* Middle Concentric Ring */}
                <circle
                  cx="100"
                  cy="100"
                  r="44"
                  fill="none"
                  stroke="#FAF8F5"
                  strokeWidth="1"
                  opacity="0.7"
                />

                {/* Inner Concentric Ring */}
                <circle
                  cx="100"
                  cy="100"
                  r="32"
                  fill="none"
                  stroke="#D4AF37"
                  strokeWidth="1.2"
                  opacity="0.9"
                />

                {/* Center Core Dot */}
                <circle
                  cx="100"
                  cy="100"
                  r="4"
                  fill="#B91C1C"
                />
              </svg>
            </motion.div>
          </div>

          {/* 
            ====================================================================
            BOTTOM CENTER: SLEEK RAZOR-THIN PROGRESS BAR & METRIC
            ====================================================================
          */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="relative z-10 flex flex-col items-center pb-8 sm:pb-12 w-full max-w-xs mx-auto gap-3"
          >
            {/* Razor-thin progress line (2px) */}
            <div className="w-full h-[2px] bg-white/20 rounded-full overflow-hidden">
              <div
                className="h-full bg-white transition-all duration-75 ease-out"
                style={{ width: `${progress}%` }}
              />
            </div>

            {/* Clean Monospace Progress Counter */}
            <div className="font-mono text-xs text-white/50 tracking-widest">
              {progress < 10 ? `0${progress}` : progress}%
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
