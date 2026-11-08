"use client";

import React from "react";
import { motion } from "motion/react";
import { ArrowDown, Sparkles } from "lucide-react";

interface SceneTransitionProps {
  fromAct?: string;
  toAct?: string;
  badge?: string;
  dark?: boolean;
}

export function SceneTransition({
  fromAct = "FEATURE 01",
  toAct = "FEATURE 02",
  badge = "CONVERGENCE → NEURAL PERSISTENCE",
  dark = true,
}: SceneTransitionProps) {
  return (
    <div className="relative w-full py-10 sm:py-14 flex flex-col items-center justify-center pointer-events-none select-none min-h-[90px]">
      {/* Horizontal Inked Seam Bar */}
      <div className={`w-full max-w-4xl px-4 ${dark ? "scene-seam-bar-dark" : "scene-seam-bar"}`} />

      {/* Center Floating Inked Connector Pill */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-60px" }}
        transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        className="relative -top-3.5 pointer-events-auto"
      >
        <div className="bg-white border-2 border-black shadow-[4px_4px_0px_#000000] px-4 py-1.5 flex items-center gap-2.5 text-[11px] font-nikkei uppercase tracking-widest text-black">
          <Sparkles className="w-3.5 h-3.5 text-[#B91C1C]" />
          <span className="font-extrabold text-[#B91C1C]">{fromAct}</span>
          <span className="text-black/40">/</span>
          <span>{badge}</span>
          <ArrowDown className="w-3 h-3 text-[#B91C1C]" />
        </div>
      </motion.div>
    </div>
  );
}
