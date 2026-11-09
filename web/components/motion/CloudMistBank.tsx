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
        {/* Floating Graphic Novel Smoke Droplets Above the Summit */}
        <div className="absolute -top-10 sm:-top-16 inset-x-0 flex items-center justify-center gap-6 sm:gap-10 pointer-events-none z-10">
          <motion.div
            animate={{ y: [-5, 5, -5], x: [-2, 2, -2], rotate: [-2, 2, -2] }}
            transition={{ duration: 4.8, repeat: Infinity, ease: "easeInOut" }}
            className="w-3 h-3 sm:w-4 sm:h-4 rounded-full bg-[#FAF8F5] border-2 border-black shadow-[2px_2px_0px_#000000]"
          />
          <motion.div
            animate={{ y: [-7, 7, -7], x: [1.5, -1.5, 1.5], rotate: [1, -1, 1] }}
            transition={{ duration: 5.6, repeat: Infinity, ease: "easeInOut", delay: 0.4 }}
            className="w-4 h-4 sm:w-5 sm:h-5 rounded-full bg-[#FAF8F5] border-2 border-black shadow-[2px_2px_0px_#000000] -translate-y-2"
          />
          <motion.div
            animate={{ y: [-4, 6, -4], x: [-1, 2, -1], rotate: [-1, 2, -1] }}
            transition={{ duration: 4.2, repeat: Infinity, ease: "easeInOut", delay: 0.9 }}
            className="w-2.5 h-2.5 sm:w-3.5 sm:h-3.5 rounded-full bg-[#FAF8F5] border-2 border-black shadow-[2px_2px_0px_#000000]"
          />
        </div>

        {/* Ambient Secondary Cloud Plume (Subtle Parallax Shadow Layer) */}
        <motion.div
          animate={{
            x: [-8, 8, -8],
            y: [-2, 3, -2],
            scale: [0.99, 1.01, 0.99],
          }}
          transition={{ duration: 8.5, repeat: Infinity, ease: "easeInOut" }}
          className="absolute inset-0 w-full opacity-30 blur-[1px] pointer-events-none"
        >
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="/santioni-cloud-plume.png"
            alt=""
            className="w-full h-auto block select-none pointer-events-none brightness-90"
          />
        </motion.div>

        {/* Primary Authentic Santioni Spirits Graphic Novel Smoke Cloud Plume */}
        <motion.div
          animate={{
            y: [-3, 4, -3],
            scaleY: [1, 1.02, 1],
            scaleX: [1, 1.01, 1],
          }}
          transition={{ duration: 6.2, repeat: Infinity, ease: "easeInOut" }}
          className="relative w-full overflow-hidden leading-none origin-bottom"
        >
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="/santioni-cloud-plume.png"
            alt="Santioni Graphic Novel Cumulus Smoke Plume"
            className="w-full h-auto block select-none pointer-events-none drop-shadow-[0_-15px_30px_rgba(0,0,0,0.85)]"
          />
        </motion.div>

        {/* Seamless Ivory Base Extension to anchor into Feature Cards */}
        <div
          className="w-full h-8 sm:h-12 -mt-[2px]"
          style={{ backgroundColor: fillColor }}
        />
      </div>
    </div>
  );
}
