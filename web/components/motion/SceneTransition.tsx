"use client";

import React, { useRef, useEffect } from "react";
import { motion, useScroll, useTransform } from "motion/react";
import { triggerSoundEffect } from "@/components/audio/SoundtrackController";

interface SceneTransitionProps {
  fromAct?: string;
  toAct?: string;
  dark?: boolean;
  className?: string;
}

export function SceneTransition({
  fromAct = "ACT I • MEMORY ENGINE",
  toAct = "ACT II • TOKEN ARBITRAGE",
  dark = true,
  className = "",
}: SceneTransitionProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start end", "end start"],
  });

  // Smooth curtain wave expansion and opacity based on scroll
  const curtainScale = useTransform(scrollYProgress, [0.1, 0.5, 0.9], [0.85, 1.05, 0.9]);
  const curtainOpacity = useTransform(scrollYProgress, [0.05, 0.35, 0.7, 0.95], [0.2, 0.95, 0.95, 0.2]);

  // Procedural Woodcut Vertical Frequency Wave on Canvas (Santioni Engraving Aesthetic)
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animId: number;
    let time = 0;

    const render = () => {
      time += 0.035;
      const width = canvas.width;
      const height = canvas.height;
      ctx.clearRect(0, 0, width, height);

      // Dense vertical frequency wave lines
      const numLines = Math.floor(width / 8);
      const colWidth = width / numLines;

      for (let i = 0; i < numLines; i++) {
        const x = i * colWidth;
        // Multi-frequency wave calculation matching Santioni BorderShader
        const wave1 = Math.sin(i * 0.16 + time * 1.4) * 28;
        const wave2 = Math.cos(i * 0.09 - time * 0.7) * 20;
        const wave3 = Math.sin(i * 0.32 + time * 2.1) * 12;
        const totalWave = wave1 + wave2 + wave3;

        // Rhythmically place blood-red ink accents
        const isRed = (i % 22 >= 9 && i % 22 <= 13);
        ctx.strokeStyle = isRed ? "#B91C1C" : (dark ? "rgba(250, 248, 245, 0.75)" : "rgba(13, 13, 17, 0.7)");
        ctx.lineWidth = i % 3 === 0 ? 2.5 : 1.2;

        ctx.beginPath();
        const startY = Math.max(0, height * 0.18 + totalWave);
        const endY = Math.min(height, height * 0.82 + totalWave);

        // Segmented woodcut hatch line with hand-engraved gaps
        const segments = 10;
        const segLen = (endY - startY) / segments;
        for (let j = 0; j < segments; j++) {
          if ((j + i) % 4 !== 0) {
            const y1 = startY + j * segLen;
            const y2 = y1 + segLen * 0.82;
            ctx.moveTo(x, y1);
            ctx.lineTo(x, y2);
          }
        }
        ctx.stroke();
      }

      animId = requestAnimationFrame(render);
    };

    const handleResize = () => {
      if (!canvas) return;
      canvas.width = canvas.parentElement?.clientWidth || 1200;
      canvas.height = 120;
    };

    handleResize();
    window.addEventListener("resize", handleResize);
    render();

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", handleResize);
    };
  }, [dark]);

  return (
    <div
      ref={containerRef}
      className={`relative w-full py-6 sm:py-10 flex flex-col items-center justify-center pointer-events-none select-none overflow-hidden z-20 ${className}`}
    >
      {/* Background Vertical Frequency Wave Canvas */}
      <motion.div
        style={{ scale: curtainScale, opacity: curtainOpacity }}
        className="w-full max-w-5xl px-4 flex justify-center"
      >
        <canvas
          ref={canvasRef}
          className="w-full h-[90px] sm:h-[120px] object-cover pointer-events-none"
        />
      </motion.div>

      {/* Minimalist Editorial Threshold Label (Santioni Spirits Aesthetic) */}
      <motion.div
        initial={{ opacity: 0, y: 14 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-40px" }}
        onViewportEnter={() => triggerSoundEffect("transition")}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
        className="relative -mt-6 pointer-events-auto z-20"
      >
        <div className="flex items-center gap-3 sm:gap-4 px-5 sm:px-7 py-2 sm:py-2.5 rounded-full border border-white/20 bg-[#070709]/85 backdrop-blur-md shadow-[0_4px_25px_rgba(0,0,0,0.85)]">
          <span className="w-1.5 h-1.5 rounded-full bg-[#B91C1C] animate-pulse shrink-0" />
          <span className="font-nikkei text-[10px] sm:text-xs text-white uppercase tracking-[0.25em] font-extrabold whitespace-nowrap">
            {fromAct}
          </span>
          <span className="text-[#B91C1C] font-mono font-bold text-xs">→</span>
          <span className="font-nikkei text-[10px] sm:text-xs text-white/90 uppercase tracking-[0.25em] font-extrabold whitespace-nowrap">
            {toAct}
          </span>
          <span className="w-1.5 h-1.5 rounded-full bg-[#B91C1C] animate-pulse shrink-0" />
        </div>
      </motion.div>
    </div>
  );
}
