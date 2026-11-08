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
          }, 450);
          return 100;
        }
        const increment = prev < 40 ? 3 : prev < 80 ? 4 : 2;
        return Math.min(100, prev + increment);
      });
    }, 28);

    return () => clearInterval(interval);
  }, [onComplete]);

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
          {/* Subtle Horizontal Dry-Brush Chalk Streaks */}
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
            TOP-LEFT: OFFICIAL AEGISBRAIN LOGO LOCKUP (Exactly as requested)
            ====================================================================
          */}
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="relative z-10 flex flex-col"
          >
            <div className="flex items-baseline">
              <span className="font-extrabold text-2xl sm:text-3xl text-white tracking-tight">
                AegisBrain
              </span>
              <span className="font-extrabold text-2xl sm:text-3xl text-[#B91C1C]">.</span>
            </div>
            <span className="text-[11px] sm:text-xs font-gt-era text-white/60 tracking-wider mt-0.5">
              Autonomous engineering chassis, neural memory bus &amp; multi-agent governor.
            </span>
          </motion.div>

          {/* 
            ====================================================================
            CENTER: GRAPHIC NOVEL CHAPTER CARD (Santioni Spirits Aesthetic)
            ====================================================================
          */}
          <div className="relative z-10 my-auto flex flex-col items-center justify-center max-w-xl mx-auto w-full text-center">
            {/* Chapter Header */}
            <div className="font-nikkei text-xs sm:text-sm text-[#B91C1C] uppercase tracking-[0.3em] font-extrabold mb-2">
              CHAPTER I
            </div>

            {/* Monolithic Serif Title */}
            <h2 className="font-charles-rosie text-4xl sm:text-6xl text-white tracking-tight uppercase leading-none mb-3">
              The Sovereign Chassis
            </h2>

            {/* Thin Decorative Hairline Divider */}
            <div className="w-24 h-[2px] bg-gradient-to-r from-transparent via-[#D4AF37] to-transparent my-4" />

            {/* Editorial Subtitle */}
            <p className="font-gt-era text-xs sm:text-sm text-white/70 max-w-md mx-auto leading-relaxed">
              Synthesizing permanent neural memory, 3-tier token arbitrage, and immortal runtime telemetry.
            </p>

            {/* Large Minimalist Numeric Progress Counter */}
            <div className="font-charles-rosie text-6xl sm:text-8xl text-white font-extrabold tracking-tighter mt-8 leading-none">
              {progress < 10 ? `0${progress}` : progress}
              <span className="text-2xl sm:text-4xl text-[#B91C1C] ml-1 font-normal">%</span>
            </div>

            {/* Fine Hairline Progress Track */}
            <div className="w-48 h-[2px] bg-white/10 rounded-full mt-6 overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-[#B91C1C] to-[#D4AF37]"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>

          {/* 
            ====================================================================
            BOTTOM: EDITORIAL MOTTO
            ====================================================================
          */}
          <div className="relative z-10 flex items-center justify-between pt-6 border-t border-white/10 text-xs font-gt-era text-white/40">
            <span className="italic font-charles-rosie text-white/60">
              &ldquo;Memoriam Non Perdet, Tempus Non Teret&rdquo;
            </span>
            <span className="uppercase font-nikkei tracking-widest text-[10px]">
              Sovereign Release v2.4.0
            </span>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
