"use client";

import React, { useEffect, useRef, useState } from "react";
import { motion, useScroll, useTransform } from "motion/react";

interface FlowCloudCanvasProps {
  fillColor?: string;
  className?: string;
  frameCount?: number;
}

const TOTAL_FRAMES = 190;
const FRAME_PATH = (idx: number) =>
  `/flow-cloud/cloud_${String(idx + 1).padStart(4, "0")}.jpg`;

export function FlowCloudCanvas({
  fillColor = "#FAF8F5",
  className = "",
  frameCount = TOTAL_FRAMES,
}: FlowCloudCanvasProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);

  const [imagesLoaded, setImagesLoaded] = useState(false);
  const [useVideoFallback, setUseVideoFallback] = useState(true);
  const imagesRef = useRef<HTMLImageElement[]>([]);
  const currentFrameRef = useRef(0);
  const animFrameIdRef = useRef<number | null>(null);

  // Bind to page scroll
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start end", "end start"],
  });

  // Preload frames in chunks
  useEffect(() => {
    let isCancelled = false;
    const loadedImages: HTMLImageElement[] = new Array(frameCount);
    let loadedCount = 0;

    // Load first 24 frames immediately for instant interactive responsiveness
    const loadBatch = (start: number, end: number) => {
      for (let i = start; i < end && i < frameCount; i++) {
        const img = new Image();
        img.src = FRAME_PATH(i);
        img.onload = () => {
          if (isCancelled) return;
          loadedImages[i] = img;
          loadedCount++;
          if (loadedCount >= Math.min(30, frameCount)) {
            imagesRef.current = loadedImages;
            setImagesLoaded(true);
            setUseVideoFallback(false);
          }
        };
      }
    };

    // Immediate first batch
    loadBatch(0, 30);

    // Stagger remaining frames to prevent network thread saturation
    const timer = setTimeout(() => {
      if (!isCancelled) {
        loadBatch(30, frameCount);
      }
    }, 350);

    return () => {
      isCancelled = true;
      clearTimeout(timer);
    };
  }, [frameCount]);

  // Canvas drawing loop with scroll-scrubbing + idle ambient billowing
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d", { alpha: true });
    if (!ctx) return;

    let lastTime = performance.now();
    let ambientPhase = 0;

    const render = (time: number) => {
      const dt = (time - lastTime) / 1000;
      lastTime = time;

      // Handle High-DPI
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const width = canvas.clientWidth;
      const height = canvas.clientHeight;

      if (canvas.width !== width * dpr || canvas.height !== height * dpr) {
        canvas.width = width * dpr;
        canvas.height = height * dpr;
      }

      ctx.save();
      ctx.scale(dpr, dpr);

      // Current scroll progress (0 to 1)
      const scrollVal = scrollYProgress.get() || 0;

      // Ambient breathing offset when idle
      ambientPhase += dt * 0.8;
      const ambientFrameOffset = Math.round(Math.sin(ambientPhase) * 6);

      // Determine target frame index
      const baseFrame = Math.floor(scrollVal * (frameCount - 1));
      const targetFrame = Math.max(
        0,
        Math.min(frameCount - 1, baseFrame + ambientFrameOffset)
      );

      currentFrameRef.current = targetFrame;
      const currentImg = imagesRef.current[targetFrame];

      if (currentImg && currentImg.complete && currentImg.naturalWidth > 0) {
        ctx.clearRect(0, 0, width, height);

        // Aspect fit / cover
        const imgAspect = currentImg.naturalWidth / currentImg.naturalHeight;
        const canvasAspect = width / height;

        let drawW = width;
        let drawH = height;
        let offsetX = 0;
        let offsetY = 0;

        if (canvasAspect > imgAspect) {
          drawW = width;
          drawH = width / imgAspect;
          offsetY = height - drawH; // Anchor to bottom
        } else {
          drawH = height;
          drawW = height * imgAspect;
          offsetX = (width - drawW) / 2; // Center horizontally
        }

        ctx.drawImage(currentImg, offsetX, offsetY, drawW, drawH);

        // Graphic novel contrast & bottom bleed gradient into fillColor
        const gradient = ctx.createLinearGradient(0, height - 70, 0, height);
        gradient.addColorStop(0, "rgba(250, 248, 245, 0)");
        gradient.addColorStop(1, fillColor);
        ctx.fillStyle = gradient;
        ctx.fillRect(0, height - 70, width, 70);
      }

      ctx.restore();
      animFrameIdRef.current = requestAnimationFrame(render);
    };

    animFrameIdRef.current = requestAnimationFrame(render);

    return () => {
      if (animFrameIdRef.current) {
        cancelAnimationFrame(animFrameIdRef.current);
      }
    };
  }, [fillColor, frameCount, imagesLoaded, scrollYProgress]);

  return (
    <div
      ref={containerRef}
      className={`relative w-full overflow-hidden pointer-events-none select-none ${className}`}
      aria-hidden="true"
    >
      <div className="relative w-full flex flex-col items-center">
        {/* Layer 1: Instant Hardware Video Fallback & Ambient Atmosphere */}
        <div
          className={`absolute inset-0 w-full h-full transition-opacity duration-700 ${
            useVideoFallback ? "opacity-100" : "opacity-0"
          }`}
        >
          <video
            ref={videoRef}
            autoPlay
            loop
            muted
            playsInline
            preload="auto"
            className="w-full h-full object-cover object-bottom brightness-105 contrast-125"
          >
            <source src="/cumulus_cloud.mp4" type="video/mp4" />
          </video>
          {/* Subtle bottom fade for video */}
          <div
            className="absolute bottom-0 inset-x-0 h-16 pointer-events-none"
            style={{
              background: `linear-gradient(to bottom, transparent, ${fillColor})`,
            }}
          />
        </div>

        {/* Layer 2: Interactive High-DPI Scrubbed Cloud Canvas */}
        <canvas
          ref={canvasRef}
          className={`relative z-10 w-full h-[320px] sm:h-[440px] md:h-[540px] lg:h-[620px] block transition-opacity duration-500 ${
            imagesLoaded ? "opacity-100" : "opacity-0"
          }`}
          style={{ imageRendering: "auto" }}
        />

        {/* Layer 3: Architectural Graphic Novel Line Accent */}
        <div className="relative z-20 w-full flex items-center justify-between px-6 -mt-3">
          <div className="h-[2px] w-24 bg-black/40" />
          <div className="font-mono text-[10px] uppercase tracking-widest text-black/50 bg-[#FAF8F5] px-2 py-0.5 border border-black/20">
            ATMOSPHERIC BUFFER // DETERMINISTIC PARALLAX
          </div>
          <div className="h-[2px] w-24 bg-black/40" />
        </div>

        {/* Seamless Ivory Base Extension to anchor into Feature Cards */}
        <div
          className="w-full h-8 sm:h-14 -mt-[1px]"
          style={{ backgroundColor: fillColor }}
        />
      </div>
    </div>
  );
}
