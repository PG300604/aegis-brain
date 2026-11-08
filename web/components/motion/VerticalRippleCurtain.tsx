"use client";

import React, { useRef, useEffect } from "react";
import { motion, useScroll, useTransform } from "motion/react";
import { triggerSoundEffect } from "@/components/audio/SoundtrackController";

interface VerticalRippleCurtainProps {
  fromAct?: string;
  toAct?: string;
  narration?: string;
  accentColor?: string;
}

export function VerticalRippleCurtain({
  fromAct = "ACT I",
  toAct = "ACT II",
  narration = "A DIMENSIONAL SHIFT TRANSPIRES. THE MEMORY INDEX RECONVERGES WITH SUB-SECOND PRECISION.",
  accentColor = "#B91C1C",
}: VerticalRippleCurtainProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start end", "end start"],
  });

  // Calculate wave curtain expansion & opacity based on scroll
  const curtainScale = useTransform(scrollYProgress, [0.1, 0.5, 0.9], [0.8, 1.05, 0.9]);
  const curtainOpacity = useTransform(scrollYProgress, [0.05, 0.3, 0.7, 0.95], [0.3, 1, 1, 0.2]);

  // Procedural Woodcut Vertical Frequency Lines Animation on Canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animId: number;
    let time = 0;

    const render = () => {
      time += 0.04;
      const width = canvas.width;
      const height = canvas.height;
      ctx.clearRect(0, 0, width, height);

      // Draw dense vertical frequency wave lines (Santioni woodcut ripple aesthetic)
      const numLines = Math.floor(width / 7);
      const colWidth = width / numLines;

      for (let i = 0; i < numLines; i++) {
        const x = i * colWidth;
        // Multi-frequency wave calculation matching Santioni BorderShader
        const wave1 = Math.sin(i * 0.18 + time * 1.5) * 35;
        const wave2 = Math.cos(i * 0.08 - time * 0.8) * 25;
        const wave3 = Math.sin(i * 0.35 + time * 2.2) * 15;
        const totalWave = wave1 + wave2 + wave3;

        const isRed = (i % 24 >= 10 && i % 24 <= 14);
        ctx.strokeStyle = isRed ? "#B91C1C" : "#FAF8F5";
        ctx.lineWidth = i % 3 === 0 ? 3 : 1.5;

        ctx.beginPath();
        const startY = Math.max(0, height * 0.15 + totalWave);
        const endY = Math.min(height, height * 0.85 + totalWave);

        // Segmented woodcut hatch line
        const segments = 12;
        const segLen = (endY - startY) / segments;
        for (let j = 0; j < segments; j++) {
          if ((j + i) % 4 !== 0) { // Creates authentic hand-engraved gaps
            const y1 = startY + j * segLen;
            const y2 = y1 + segLen * 0.8;
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
      canvas.height = 160;
    };

    handleResize();
    window.addEventListener("resize", handleResize);
    render();

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return (
    <div
      ref={containerRef}
      className="relative w-full py-12 sm:py-20 flex flex-col items-center justify-center pointer-events-none select-none overflow-hidden"
    >
      {/* Background Vertical Frequency Wave Canvas */}
      <motion.div
        style={{ scale: curtainScale, opacity: curtainOpacity }}
        className="w-full max-w-6xl px-4 flex justify-center"
      >
        <canvas
          ref={canvasRef}
          className="w-full h-[140px] sm:h-[180px] object-cover pointer-events-none"
        />
      </motion.div>

      {/* Floating Graphic Novel Narration Box */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-50px" }}
        onViewportEnter={() => triggerSoundEffect("transition")}
        transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        className="relative -mt-8 pointer-events-auto z-20 max-w-2xl px-4"
      >
        <div className="bg-white border-2 border-black shadow-[6px_6px_0px_#000000] p-4 text-center">
          <div className="flex items-center justify-center gap-2 mb-1.5 text-[10px] font-nikkei uppercase font-extrabold tracking-widest text-[#B91C1C]">
            <span>{fromAct}</span>
            <span className="text-black/40">→</span>
            <span>{toAct}</span>
          </div>
          <p className="font-mono text-black text-xs sm:text-[13px] font-bold uppercase tracking-wider leading-relaxed">
            {narration}
          </p>
        </div>
      </motion.div>
    </div>
  );
}
