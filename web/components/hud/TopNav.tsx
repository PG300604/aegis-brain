"use client";

import React, { useState, useEffect } from "react";
import { Shield, Star, Menu, X, Terminal, ExternalLink } from "lucide-react";

export function TopNav() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const navLinks = [
    { label: "Architecture", href: "#architecture" },
    { label: "Benchmarks", href: "#benchmarks" },
    { label: "Token Arbitrage", href: "#arbitrage" },
    { label: "Telegram Bot", href: "#mobile" },
    { label: "Quality Gates", href: "#quality-gates" },
    { label: "Install", href: "#install" },
  ];

  return (
    <header className="fixed top-0 left-0 right-0 z-50 pt-4 px-4 sm:px-6 transition-all duration-300">
      <div
        className={`glass-panel rounded-full max-w-6xl mx-auto px-5 sm:px-7 py-3 flex items-center justify-between transition-all duration-300 ${
          scrolled ? "shadow-[0_10px_35px_rgba(0,0,0,0.8)] border-cyan-500/20" : ""
        }`}
      >
        {/* Brand / Logo + Daemon Status */}
        <div className="flex items-center gap-3">
          <a href="#" className="flex items-center gap-2 group">
            <div className="relative flex items-center justify-center w-8 h-8 rounded-lg bg-cyan-950/60 border border-cyan-500/30 group-hover:border-cyan-400 transition-colors">
              <Shield className="w-4 h-4 text-cyan-400 group-hover:scale-110 transition-transform" />
              <div className="absolute inset-0 bg-cyan-400/10 rounded-lg blur-xs" />
            </div>
            <div className="flex flex-col">
              <div className="flex items-center gap-1.5">
                <span className="font-bold tracking-wider text-sm sm:text-base text-white font-mono">
                  AEGIS<span className="text-cyan-400">BRAIN</span>
                </span>
                <span className="hidden sm:inline-block text-[10px] uppercase font-mono px-1.5 py-0.5 rounded border border-white/10 bg-white/5 text-zinc-400">
                  v0.4.0
                </span>
              </div>
            </div>
          </a>

          {/* Daemon 24/7 Active Pulse Badge */}
          <div className="hidden lg:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-950/40 border border-emerald-500/20">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span className="font-mono text-[11px] text-emerald-400 tracking-tight font-medium">
              DAEMON :8765 ACTIVE
            </span>
          </div>
        </div>

        {/* Desktop Navigation Links */}
        <nav className="hidden md:flex items-center gap-6 text-xs sm:text-sm text-zinc-300 font-medium">
          {navLinks.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="hover:text-cyan-400 transition-colors duration-150 relative py-1 text-zinc-400 hover:text-white"
            >
              {link.label}
            </a>
          ))}
        </nav>

        {/* Action Buttons: GitHub Star + Install CLI */}
        <div className="hidden sm:flex items-center gap-3">
          <a
            href="https://github.com/PG300604/aegis-brain"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 text-xs font-medium px-3.5 py-1.5 rounded-full bg-zinc-900/80 hover:bg-zinc-800 text-zinc-300 hover:text-white border border-white/10 transition-all hover:border-amber-400/40 group"
          >
            <Star className="w-3.5 h-3.5 text-amber-400 fill-amber-400/20 group-hover:fill-amber-400 transition-all" />
            <span>Star on GitHub</span>
          </a>

          <a
            href="#install"
            className="flex items-center gap-1.5 text-xs font-semibold px-4 py-1.5 rounded-full bg-gradient-to-r from-cyan-500 to-blue-600 text-black hover:opacity-95 shadow-[0_0_15px_rgba(0,240,255,0.3)] hover:shadow-[0_0_22px_rgba(0,240,255,0.5)] transition-all font-mono"
          >
            <Terminal className="w-3.5 h-3.5" />
            <span>Install CLI</span>
          </a>
        </div>

        {/* Mobile menu button */}
        <div className="flex md:hidden items-center gap-2">
          <a
            href="#install"
            className="text-[11px] font-mono font-semibold px-3 py-1 rounded-full bg-cyan-500 text-black"
          >
            Install
          </a>
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-1.5 rounded-lg border border-white/10 text-zinc-400 hover:text-white"
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden mt-2 mx-auto max-w-sm glass-panel rounded-2xl p-4 border border-cyan-500/20 space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-white/10">
            <span className="font-mono text-xs text-emerald-400 flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
              DAEMON :8765 ACTIVE
            </span>
            <span className="font-mono text-[10px] text-zinc-400">v0.4.0</span>
          </div>

          <div className="flex flex-col space-y-2">
            {navLinks.map((link) => (
              <a
                key={link.href}
                href={link.href}
                onClick={() => setMobileMenuOpen(false)}
                className="px-3 py-2 rounded-lg text-sm text-zinc-300 hover:text-cyan-400 hover:bg-white/5 font-medium transition-colors"
              >
                {link.label}
              </a>
            ))}
          </div>

          <div className="pt-2 border-t border-white/10 flex flex-col gap-2">
            <a
              href="https://github.com/PG300604/aegis-brain"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-center gap-2 py-2 rounded-lg bg-zinc-900 border border-white/10 text-xs text-zinc-300"
            >
              <Star className="w-3.5 h-3.5 text-amber-400 fill-amber-400" />
              <span>Star on GitHub</span>
              <ExternalLink className="w-3 h-3 text-zinc-500" />
            </a>
          </div>
        </div>
      )}
    </header>
  );
}

export default TopNav;
