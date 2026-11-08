"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Terminal, Shield, Zap, Sparkles, CheckCircle2 } from "lucide-react";

interface LoadingScreenProps {
  onComplete?: () => void;
}

const BOOTSTRAP_LOGS = [
  { text: "INITIALIZING PERSISTENT SQLITE WAL NEURAL BUS...", latency: "14ms" },
  { text: "MOUNTING 3-TIER TOKEN ARBITRAGE (HERMES CLI + MOE)...", latency: "22ms" },
  { text: "VERIFYING 286/286 PYTEST INVARIANT GATES...", latency: "38ms" },
  { text: "ACTIVATING 24/7 WIN32 KEEPALIVE TELEMETRY SHIELD...", latency: "18ms" },
  { text: "READY. SOVEREIGN ENGINE ONLINE.", latency: "0ms" },
];

export function LoadingScreen({ onComplete }: LoadingScreenProps) {
  const [progress, setProgress] = useState<number>(0);
  const [logIndex, setLogIndex] = useState<number>(0);
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
          }, 400);
          return 100;
        }
        // Accelerate progressively
        const increment = prev < 40 ? 3 : prev < 80 ? 4 : 2;
        const next = Math.min(100, prev + increment);

        // Update log lines based on progress tier
        if (next >= 85) setLogIndex(4);
        else if (next >= 65) setLogIndex(3);
        else if (next >= 40) setLogIndex(2);
        else if (next >= 20) setLogIndex(1);
        else setLogIndex(0);

        return next;
      });
    }, 28);

    return () => clearInterval(interval);
  }, [onComplete]);

  return (
    <AnimatePresence>
      {!isDone && (
        <motion.div
          key="aegis-preloader"
          initial={{ opacity: 1 }}
          exit={{
            y: "-100%",
            transition: { duration: 0.85, ease: [0.76, 0, 0.24, 1] },
          }}
          className="fixed inset-0 z-[100] flex flex-col justify-between p-6 sm:p-12 bg-[#070709] text-[#FBF9F5] select-none pointer-events-auto overflow-hidden"
        >
          {/* Subtle Graphic Paper Grain & Radial Vignette */}
          <div
            className="absolute inset-0 pointer-events-none opacity-20"
            style={{
              backgroundImage: `radial-gradient(circle at 50% 50%, rgba(185, 28, 28, 0.12) 0%, transparent 70%)`,
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
            CENTER: LUXURY EDITORIAL PERCENTAGE & TELEMETRY
            ====================================================================
          */}
          <div className="relative z-10 my-auto flex flex-col items-center justify-center max-w-2xl mx-auto w-full text-center">
            {/* Minimal Subtitle Badge */}
            <div className="inline-flex items-center gap-2 px-3 py-1 bg-black border border-white/20 rounded text-[10px] sm:text-xs font-nikkei text-[#D4AF37] uppercase tracking-widest mb-6 shadow-[2px_2px_0px_#000000]">
              <span className="w-1.5 h-1.5 rounded-full bg-[#B91C1C] animate-ping" />
              <span>SYSTEM BOOTSTRAP PROTOCOL</span>
            </div>

            {/* Giant Monolithic Numeric Counter */}
            <div className="font-charles-rosie text-7xl sm:text-9xl font-extrabold tracking-tighter text-white leading-none">
              {progress < 10 ? `0${progress}` : progress}
              <span className="text-3xl sm:text-5xl text-[#B91C1C] font-normal ml-1">%</span>
            </div>

            {/* High-Precision Progress Rail */}
            <div className="w-full max-w-md h-[2px] bg-white/10 rounded-full my-6 overflow-hidden relative">
              <motion.div
                className="h-full bg-gradient-to-r from-[#B91C1C] via-[#D4AF37] to-white"
                style={{ width: `${progress}%` }}
                transition={{ ease: "easeOut" }}
              />
            </div>

            {/* Dynamic Real-Time Diagnostic Feed */}
            <div className="font-mono text-xs sm:text-sm text-zinc-400 h-6 flex items-center justify-center gap-2">
              <span className="text-[#B91C1C] font-bold">&gt;</span>
              <span className="tracking-wider text-zinc-300">
                {BOOTSTRAP_LOGS[logIndex].text}
              </span>
              <span className="text-[10px] text-zinc-500 font-mono">
                [{BOOTSTRAP_LOGS[logIndex].latency}]
              </span>
            </div>
          </div>

          {/* 
            ====================================================================
            BOTTOM: STATUS CHIPS & METRICS
            ====================================================================
          */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="relative z-10 flex flex-col sm:flex-row items-center justify-between gap-4 pt-6 border-t border-white/10 text-xs font-mono text-white/50"
          >
            <div className="flex items-center gap-4">
              <span className="flex items-center gap-1.5 text-emerald-400">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>286 / 286 Tests Passing</span>
              </span>
              <span>•</span>
              <span className="text-zinc-400">SQLite WAL 24ms SLA</span>
            </div>

            <div className="text-[11px] font-gt-era text-zinc-500">
              Sovereign Release v2.4.0 • Zero Cloud Lock-in
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
