"use client";

import React from "react";
import { motion } from "motion/react";
import { ArrowDown, Sparkles } from "lucide-react";

interface SceneTransitionProps {
  fromAct?: string;
  toAct?: string;
  badge?: string;
  accentColor?: string;
}

export function SceneTransition({
  fromAct = "ACT I",
  toAct = "ACT II",
  badge = "CONVERGENCE → NEURAL PERSISTENCE",
  accentColor = "cyan",
}: SceneTransitionProps) {
  return (
    <div className="relative w-full py-16 flex flex-col items-center justify-center pointer-events-none">
      {/* Background ambient radial glow */}
      <div className="absolute w-72 h-32 bg-cyan-500/10 rounded-full blur-3xl" />

      {/* Horizontal Seam Bar */}
      <div className="scene-seam-bar max-w-4xl" />

      {/* Center Floating Connector Pill */}
      <motion.div
        initial={{ opacity: 0, y: 10, scale: 0.95 }}
        whileInView={{ opacity: 1, y: 0, scale: 1 }}
        viewport={{ once: true, margin: "-40px" }}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
        className="relative -top-4 pointer-events-auto"
      >
        <div className="glass-panel-glow px-4 py-1.5 rounded-full flex items-center gap-2.5 text-[11px] font-mono uppercase tracking-widest text-cyan-300 border border-cyan-400/40 shadow-[0_0_20px_rgba(0,240,255,0.3)]">
          <Sparkles className="w-3.5 h-3.5 text-cyan-400 animate-pulse" />
          <span className="font-bold">{badge}</span>
          <ArrowDown className="w-3.5 h-3.5 text-cyan-400" />
        </div>
      </motion.div>
    </div>
  );
}
