"use client";

import React, { useEffect, useRef } from "react";
import * as THREE from "three";

/**
 * Procedural circular soft radial glow texture for token particles.
 * Eliminates external texture asset dependencies while ensuring high-performance additive blending.
 */
function createParticleTexture(): THREE.CanvasTexture | null {
  if (typeof document === "undefined") return null;
  const canvas = document.createElement("canvas");
  canvas.width = 64;
  canvas.height = 64;
  const ctx = canvas.getContext("2d");
  if (!ctx) return null;

  const gradient = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
  gradient.addColorStop(0, "rgba(255, 255, 255, 1.0)");
  gradient.addColorStop(0.25, "rgba(0, 240, 255, 0.85)");
  gradient.addColorStop(0.65, "rgba(168, 85, 247, 0.35)");
  gradient.addColorStop(1, "rgba(0, 0, 0, 0)");

  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, 64, 64);

  const texture = new THREE.CanvasTexture(canvas);
  texture.generateMipmaps = false;
  texture.minFilter = THREE.LinearFilter;
  return texture;
}

export default function NeuralMonolithCanvas() {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const container = containerRef.current;
    const canvas = canvasRef.current;
    if (!container || !canvas) return;

    // --- 1. Scene, Camera & Renderer ---
    const width = container.clientWidth || window.innerWidth;
    const height = container.clientHeight || window.innerHeight;

    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x030305, 0.035);

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    camera.position.set(0, 0, 9.5);

    const renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      alpha: true,
      powerPreference: "high-performance",
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.25;

    // --- 2. Lighting ---
    const ambientLight = new THREE.AmbientLight(0x080914, 1.4);
    scene.add(ambientLight);

    const keyLight = new THREE.DirectionalLight(0x00f0ff, 2.8);
    keyLight.position.set(7, 9, 6);
    scene.add(keyLight);

    const rimLight = new THREE.DirectionalLight(0xa855f7, 2.2);
    rimLight.position.set(-7, -5, -4);
    scene.add(rimLight);

    const fillLight = new THREE.DirectionalLight(0x00e5ff, 1.2);
    fillLight.position.set(0, -6, 5);
    scene.add(fillLight);

    // --- 3. Procedural Obsidian Monolith Group ---
    const monolithGroup = new THREE.Group();
    scene.add(monolithGroup);

    // Monolith Body (Octahedron scaled to imposing luxury obelisk proportions)
    const monolithGeo = new THREE.OctahedronGeometry(2.35, 0);
    monolithGeo.scale(1.0, 1.48, 1.0);

    const monolithMat = new THREE.MeshPhysicalMaterial({
      color: 0x050508,
      metalness: 0.94,
      roughness: 0.07,
      clearcoat: 1.0,
      clearcoatRoughness: 0.09,
      reflectivity: 0.95,
      flatShading: true,
    });
    const monolithMesh = new THREE.Mesh(monolithGeo, monolithMat);
    monolithGroup.add(monolithMesh);

    // Cyan Neon Edge Lattice Overlay
    const wireframeGeo = new THREE.WireframeGeometry(monolithGeo);
    const wireframeMat = new THREE.LineBasicMaterial({
      color: 0x00f0ff,
      transparent: true,
      opacity: 0.72,
      blending: THREE.AdditiveBlending,
      linewidth: 1,
    });
    const wireframeMesh = new THREE.LineSegments(wireframeGeo, wireframeMat);
    monolithGroup.add(wireframeMesh);

    // Internal Pulsating Reactor Core
    const coreGeo = new THREE.IcosahedronGeometry(0.85, 1);
    const coreMat = new THREE.MeshBasicMaterial({
      color: 0xa855f7,
      wireframe: true,
      transparent: true,
      opacity: 0.65,
      blending: THREE.AdditiveBlending,
    });
    const coreMesh = new THREE.Mesh(coreGeo, coreMat);
    monolithGroup.add(coreMesh);

    const reactorLight = new THREE.PointLight(0x00f0ff, 3.2, 14, 2);
    monolithGroup.add(reactorLight);

    const reactorPurpleLight = new THREE.PointLight(0xa855f7, 2.0, 8, 2);
    monolithGroup.add(reactorPurpleLight);

    // --- 4. Token Fluid Particle Vortex ---
    const particleCount = 1600;
    const particleGeo = new THREE.BufferGeometry();

    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);
    const radii = new Float32Array(particleCount);
    const angles = new Float32Array(particleCount);
    const heights = new Float32Array(particleCount);
    const baseSpeeds = new Float32Array(particleCount);
    const turbulences = new Float32Array(particleCount);

    const palette = [
      new THREE.Color(0x00f0ff), // Cyan
      new THREE.Color(0xa855f7), // Purple
      new THREE.Color(0x00e5ff), // Teal
      new THREE.Color(0x10b981), // Emerald
    ];

    for (let i = 0; i < particleCount; i++) {
      const r = 2.6 + Math.random() * 5.6;
      const angle = Math.random() * Math.PI * 2;
      const h = (Math.random() - 0.5) * 8.5;

      radii[i] = r;
      angles[i] = angle;
      heights[i] = h;
      baseSpeeds[i] = (0.25 + Math.random() * 0.75) * (Math.random() > 0.15 ? 1 : -0.5);
      turbulences[i] = Math.random() * Math.PI * 2;

      positions[i * 3] = Math.cos(angle) * r;
      positions[i * 3 + 1] = h;
      positions[i * 3 + 2] = Math.sin(angle) * r;

      const color = palette[Math.floor(Math.random() * palette.length)];
      colors[i * 3] = color.r;
      colors[i * 3 + 1] = color.g;
      colors[i * 3 + 2] = color.b;
    }

    particleGeo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
    particleGeo.setAttribute("color", new THREE.BufferAttribute(colors, 3));

    const particleTexture = createParticleTexture();
    const particleMat = new THREE.PointsMaterial({
      size: 0.12,
      vertexColors: true,
      transparent: true,
      opacity: 0.85,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      map: particleTexture ?? undefined,
    });

    const particleSystem = new THREE.Points(particleGeo, particleMat);
    scene.add(particleSystem);

    // --- 5. Interactive Motion State Tracking ---
    const mouseState = {
      x: 0,
      y: 0,
      targetX: 0,
      targetY: 0,
      vx: 0,
      vy: 0,
      lastClientX: 0,
      lastClientY: 0,
    };

    const scrollState = {
      current: 0,
      target: 0,
    };

    const onMouseMove = (e: MouseEvent) => {
      const nx = (e.clientX / window.innerWidth) * 2 - 1;
      const ny = -(e.clientY / window.innerHeight) * 2 + 1;
      mouseState.targetX = nx;
      mouseState.targetY = ny;

      const dx = e.clientX - mouseState.lastClientX;
      const dy = e.clientY - mouseState.lastClientY;
      mouseState.vx = dx * 0.003;
      mouseState.vy = dy * 0.003;
      mouseState.lastClientX = e.clientX;
      mouseState.lastClientY = e.clientY;
    };

    const onMouseLeave = () => {
      mouseState.targetX = 0;
      mouseState.targetY = 0;
      mouseState.vx = 0;
      mouseState.vy = 0;
    };

    const onScroll = () => {
      const maxScroll = Math.max(
        document.documentElement.scrollHeight - window.innerHeight,
        1
      );
      scrollState.target = Math.min(Math.max(window.scrollY / maxScroll, 0), 1);
    };

    window.addEventListener("mousemove", onMouseMove, { passive: true });
    window.addEventListener("mouseleave", onMouseLeave, { passive: true });
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    // --- 6. Resize Observer ---
    const resizeRenderer = () => {
      if (!container || !canvas) return;
      const w = container.clientWidth || window.innerWidth;
      const h = container.clientHeight || window.innerHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };

    const resizeObserver = new ResizeObserver(() => {
      resizeRenderer();
    });
    resizeObserver.observe(container);

    // --- 7. Animation Loop ---
    let animationFrameId: number;
    let clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);

      const delta = clock.getDelta();
      const time = clock.getElapsedTime();

      // Smooth mouse damping
      mouseState.x += (mouseState.targetX - mouseState.x) * 0.05;
      mouseState.y += (mouseState.targetY - mouseState.y) * 0.05;
      mouseState.vx *= 0.94;
      mouseState.vy *= 0.94;

      // Smooth scroll interpolation
      scrollState.current += (scrollState.target - scrollState.current) * 0.06;

      // Camera dolly and vertical track reacting to scroll
      camera.position.z = 9.5 - scrollState.current * 2.8;
      camera.position.y = -scrollState.current * 1.8 + mouseState.y * 0.35;
      camera.position.x = mouseState.x * 0.45;
      camera.lookAt(0, -scrollState.current * 0.5, 0);

      // Monolith rotation and fluid tilt
      monolithGroup.rotation.y += (0.003 + Math.abs(mouseState.vx) * 0.04 + scrollState.current * 0.006);
      monolithGroup.rotation.x = 0.18 + mouseState.y * 0.28 + scrollState.current * 0.5;
      monolithGroup.rotation.z = -mouseState.x * 0.22;

      // Reactor pulsation
      const pulse = 1.0 + Math.sin(time * 3.2) * 0.12;
      coreMesh.scale.set(pulse, pulse, pulse);
      coreMesh.rotation.y -= 0.012;
      coreMesh.rotation.x += 0.008;

      reactorLight.intensity = 3.2 + Math.sin(time * 4.0) * 1.2;
      reactorPurpleLight.intensity = 2.0 + Math.cos(time * 3.5) * 0.8;

      // Token fluid particle vortex advection
      const posAttr = particleGeo.attributes.position as THREE.BufferAttribute;
      const posArray = posAttr.array as Float32Array;
      const swirlImpulse = (mouseState.vx * 2.5 + 0.004) * delta * 60;

      for (let i = 0; i < particleCount; i++) {
        const i3 = i * 3;
        angles[i] += (baseSpeeds[i] * 0.008) + swirlImpulse;
        heights[i] += Math.sin(time * 0.8 + turbulences[i]) * 0.008;

        // Wrap particles within bounds
        if (heights[i] > 5.5) heights[i] = -5.5;
        if (heights[i] < -5.5) heights[i] = 5.5;

        const currentR = radii[i] + Math.sin(time * 1.5 + turbulences[i]) * 0.25;

        posArray[i3] = Math.cos(angles[i]) * currentR;
        posArray[i3 + 1] = heights[i] + mouseState.y * 0.4;
        posArray[i3 + 2] = Math.sin(angles[i]) * currentR;
      }
      posAttr.needsUpdate = true;

      // Slowly rotate particle field
      particleSystem.rotation.y += 0.0015;

      renderer.render(scene, camera);
    };

    animate();

    // --- 8. Comprehensive Cleanup ---
    return () => {
      cancelAnimationFrame(animationFrameId);
      resizeObserver.disconnect();
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseleave", onMouseLeave);
      window.removeEventListener("scroll", onScroll);

      monolithGeo.dispose();
      monolithMat.dispose();
      wireframeGeo.dispose();
      wireframeMat.dispose();
      coreGeo.dispose();
      coreMat.dispose();
      particleGeo.dispose();
      particleMat.dispose();
      particleTexture?.dispose();

      renderer.dispose();
    };
  }, []);

  return (
    <div
      ref={containerRef}
      className="fixed inset-0 pointer-events-none z-0 overflow-hidden"
      aria-hidden="true"
    >
      <canvas ref={canvasRef} className="w-full h-full block" />
      {/* Subtle vignette radial mask to blend canvas into background */}
      <div className="absolute inset-0 bg-radial-gradient from-transparent via-[#030305]/40 to-[#030305] pointer-events-none" />
    </div>
  );
}
