"use client";

import React, { useEffect, useRef, useState, useCallback } from "react";
import { useScroll } from "motion/react";

interface FlowCloudCanvasProps {
  fillColor?: string;
  className?: string;
}

const TOTAL_FRAMES = 190;
const FRAME_PATH = (idx: number) =>
  `/flow-cloud/cloud_${String(idx + 1).padStart(4, "0")}.jpg`;

export function FlowCloudCanvas({
  fillColor = "#FAF8F5",
  className = "",
}: FlowCloudCanvasProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [imagesLoaded, setImagesLoaded] = useState(false);
  const imagesRef = useRef<HTMLImageElement[]>([]);
  const currentFrameRef = useRef(0);
  const animFrameIdRef = useRef<number | null>(null);

  // Bind strictly to window scroll progress through the hero container
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start end", "end start"],
  });

  // Preload all 190 high-res cropped frames
  useEffect(() => {
    let isCancelled = false;
    const loadedImages: HTMLImageElement[] = new Array(TOTAL_FRAMES);
    let loadedCount = 0;

    const loadRange = (start: number, end: number) => {
      for (let i = start; i < end && i < TOTAL_FRAMES; i++) {
        const img = new Image();
        img.src = FRAME_PATH(i);
        img.onload = () => {
          if (isCancelled) return;
          loadedImages[i] = img;
          loadedCount++;
          // Enable display as soon as initial cluster is available
          if (loadedCount >= 20 && !imagesLoaded) {
            imagesRef.current = loadedImages;
            setImagesLoaded(true);
          }
        };
      }
    };

    // Load initial 30 frames instantly
    loadRange(0, 30);

    // Stagger remaining frames smoothly
    const t = setTimeout(() => {
      if (!isCancelled) {
        loadRange(30, TOTAL_FRAMES);
      }
    }, 200);

    return () => {
      isCancelled = true;
      clearTimeout(t);
    };
  }, [imagesLoaded]);

  // Draw current frame on canvas strictly on scroll
  const drawFrame = useCallback(
    (frameIdx: number) => {
      const canvas = canvasRef.current;
      if (!canvas) return;
      const ctx = canvas.getContext("2d", { alpha: true });
      if (!ctx) return;

      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const width = canvas.clientWidth;
      const height = canvas.clientHeight;

      if (canvas.width !== width * dpr || canvas.height !== height * dpr) {
        canvas.width = width * dpr;
        canvas.height = height * dpr;
      }

      ctx.save();
      ctx.scale(dpr, dpr);
      ctx.clearRect(0, 0, width, height);

      // Find nearest loaded frame if current isn't ready yet
      let img = imagesRef.current[frameIdx];
      if (!img || !img.complete || img.naturalWidth === 0) {
        for (let offset = 1; offset < 20; offset++) {
          const prev = imagesRef.current[Math.max(0, frameIdx - offset)];
          if (prev && prev.complete && prev.naturalWidth > 0) {
            img = prev;
            break;
          }
        }
      }

      if (img && img.complete && img.naturalWidth > 0) {
        // High-res cover math across entire canvas width
        const imgAspect = img.naturalWidth / img.naturalHeight;
        const canvasAspect = width / height;

        let drawW = width;
        let drawH = height;
        let offsetX = 0;
        let offsetY = 0;

        if (canvasAspect > imgAspect) {
          drawW = width;
          drawH = width / imgAspect;
          offsetY = 0; // Anchor top half
        } else {
          drawH = height;
          drawW = height * imgAspect;
          offsetX = (width - drawW) / 2;
        }

        // Draw cloud frame
        ctx.globalAlpha = 0.96;
        ctx.drawImage(img, offsetX, offsetY, drawW, drawH);

        // Soft lateral transparency feathering to eliminate harsh side cutoff on full screen
        const fadeW = Math.min(width * 0.14, 180);

        // Left fade
        const leftGrad = ctx.createLinearGradient(0, 0, fadeW, 0);
        leftGrad.addColorStop(0, "#070709");
        leftGrad.addColorStop(1, "rgba(7, 7, 9, 0)");
        ctx.fillStyle = leftGrad;
        ctx.fillRect(0, 0, fadeW, height);

        // Right fade
        const rightGrad = ctx.createLinearGradient(width - fadeW, 0, width, 0);
        rightGrad.addColorStop(0, "rgba(7, 7, 9, 0)");
        rightGrad.addColorStop(1, "#070709");
        ctx.fillStyle = rightGrad;
        ctx.fillRect(width - fadeW, 0, fadeW, height);

        // Top transparency feathering
        const topGrad = ctx.createLinearGradient(0, 0, 0, 60);
        topGrad.addColorStop(0, "#070709");
        topGrad.addColorStop(1, "rgba(7, 7, 9, 0)");
        ctx.fillStyle = topGrad;
        ctx.fillRect(0, 0, width, 60);

        // Soft bottom transparency fade into deep black background (no harsh white bar)
        const botGrad = ctx.createLinearGradient(0, height - 80, 0, height);
        botGrad.addColorStop(0, "rgba(7, 7, 9, 0)");
        botGrad.addColorStop(1, "#070709");
        ctx.fillStyle = botGrad;
        ctx.fillRect(0, height - 80, width, 80);
      }

      ctx.restore();
    },
    []
  );

  // Subscribe strictly to scroll progress: ONLY moves on scroll wheel
  useEffect(() => {
    const unsubscribe = scrollYProgress.on("change", (latest) => {
      // Clamp strictly to frame count
      const clamped = Math.max(0, Math.min(1, latest));
      const targetFrame = Math.min(
        TOTAL_FRAMES - 1,
        Math.floor(clamped * (TOTAL_FRAMES - 1))
      );
      if (targetFrame !== currentFrameRef.current) {
        currentFrameRef.current = targetFrame;
        if (animFrameIdRef.current) {
          cancelAnimationFrame(animFrameIdRef.current);
        }
        animFrameIdRef.current = requestAnimationFrame(() => {
          drawFrame(targetFrame);
        });
      }
    });

    // Initial render
    drawFrame(0);

    return () => {
      unsubscribe();
      if (animFrameIdRef.current) {
        cancelAnimationFrame(animFrameIdRef.current);
      }
    };
  }, [drawFrame, scrollYProgress]);

  // Handle window resize cleanly
  useEffect(() => {
    const handleResize = () => {
      drawFrame(currentFrameRef.current);
    };
    window.addEventListener("resize", handleResize, { passive: true });
    return () => window.removeEventListener("resize", handleResize);
  }, [drawFrame]);

  return (
    <div
      ref={containerRef}
      className={`relative w-screen left-1/2 -translate-x-1/2 overflow-visible pointer-events-none select-none ${className}`}
      aria-hidden="true"
    >
      <div className="relative w-full flex flex-col items-center">
        {/* Full-Bleed High-DPI Cloud Canvas with Lateral and Bottom Transparency Feathering */}
        <canvas
          ref={canvasRef}
          className="relative z-10 w-full h-[360px] sm:h-[480px] md:h-[580px] lg:h-[680px] block"
          style={{
            imageRendering: "auto",
            WebkitMaskImage:
              "linear-gradient(to bottom, black 82%, transparent 100%)",
            maskImage:
              "linear-gradient(to bottom, black 82%, transparent 100%)",
          }}
        />
      </div>
    </div>
  );
}
