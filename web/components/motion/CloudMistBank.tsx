"use client";

import React from "react";
import { motion } from "motion/react";

interface CloudMistBankProps {
  fillColor?: string;
  className?: string;
}

export function CloudMistBank({
  fillColor = "#FAF8F5",
  className = "",
}: CloudMistBankProps) {
  return (
    <div
      className={`relative w-full overflow-visible pointer-events-none select-none ${className}`}
      aria-hidden="true"
    >
      <div className="relative w-full flex flex-col items-center">
        {/* Layer 1: Ambient Background Mist Plume (Deep Parallax Drift) */}
        <motion.div
          animate={{
            x: [-16, 16, -16],
            y: [-6, 8, -6],
            scale: [0.99, 1.025, 0.99],
          }}
          transition={{ duration: 7.8, repeat: Infinity, ease: "easeInOut" }}
          className="absolute inset-0 w-full opacity-40 blur-[1px] pointer-events-none"
        >
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="/santioni-cloud-plume-hd.png"
            alt=""
            className="w-full h-auto block select-none pointer-events-none brightness-75"
          />
        </motion.div>

        {/* Layer 2: Primary Authentic Santioni Graphic Novel Cumulus Smoke Plume (Visible Active Billow) */}
        <motion.div
          animate={{
            y: [-10, 10, -10],
            scaleY: [1, 1.035, 1],
            scaleX: [1, 1.018, 1],
            rotate: [-0.4, 0.4, -0.4],
          }}
          transition={{ duration: 5.8, repeat: Infinity, ease: "easeInOut" }}
          className="relative w-full overflow-hidden leading-none origin-bottom"
        >
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="/santioni-cloud-plume-hd.png"
            alt="Santioni Spirits Graphic Novel Smoke Cloud"
            className="w-full h-auto block select-none pointer-events-none drop-shadow-[0_-20px_35px_rgba(0,0,0,0.92)]"
          />
        </motion.div>

        {/* Seamless Ivory Base Extension to anchor into Feature Cards */}
        <div
          className="w-full h-10 sm:h-16 -mt-[2px]"
          style={{ backgroundColor: fillColor }}
        />
      </div>
    </div>
  );
}
