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
        {/* Authentic Santioni Spirits Graphic Novel Smoke Cloud Plume */}
        <div className="relative w-full overflow-hidden leading-none">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="/santioni-cloud-plume.png"
            alt="Santioni Graphic Novel Cumulus Smoke Plume"
            className="w-full h-auto block select-none pointer-events-none drop-shadow-[0_-15px_30px_rgba(0,0,0,0.85)]"
          />
        </div>
        {/* Seamless Ivory Base Extension to anchor into Feature Cards */}
        <div
          className="w-full h-8 sm:h-12 -mt-[2px]"
          style={{ backgroundColor: fillColor }}
        />
      </div>
    </div>
  );
}
