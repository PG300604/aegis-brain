"use client";

import React, { useState, useEffect } from "react";
import { Star, Menu, X, Terminal, ExternalLink, ArrowRight } from "lucide-react";

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
    { label: "Features", href: "#features" },
    { label: "Memory Core", href: "#memory" },
    { label: "Arbitrage", href: "#arbitrage" },
    { label: "Blueprints", href: "#blueprints" },
    { label: "Install", href: "#install" },
  ];

  return (
    <header className="fixed top-0 left-0 right-0 z-50 pt-4 px-4 sm:px-8 transition-all duration-300">
      <div
        className={`max-w-7xl mx-auto px-5 sm:px-8 py-3.5 flex items-center justify-between transition-all duration-300 rounded-lg border-2 border-black bg-[#101116]/95 backdrop-blur-md ${
          scrolled ? "shadow-[6px_6px_0px_#000000] border-white/20" : "shadow-[4px_4px_0px_#000000]"
        }`}
      >
        {/* Brand Lockup: Clean Minimal Aesthetic */}
        <div className="flex items-center gap-4">
          <a href="#" className="flex flex-col group select-none">
            <div className="flex items-baseline">
              <span className="font-extrabold text-xl sm:text-2xl text-white tracking-tight group-hover:text-zinc-200 transition-colors">
                AegisBrain
              </span>
              <span className="font-extrabold text-xl sm:text-2xl text-[#B91C1C]">.</span>
            </div>
          </a>

          {/* Daemon Active Badge */}
          <div className="hidden xl:flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#0A3320] border border-emerald-500/30">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
            </span>
            <span className="font-mono text-[10px] text-emerald-400 tracking-tight font-bold">
              DAEMON :8765 ACTIVE
            </span>
          </div>
        </div>

        {/* Desktop Navigation Links */}
        <nav className="hidden md:flex items-center gap-5 text-xs font-nikkei uppercase tracking-wider text-zinc-300 font-bold">
          {navLinks.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="hover:text-[#D4AF37] transition-colors duration-150 py-1"
            >
              {link.label}
            </a>
          ))}
          <a
            href="https://github.com/PG300604/aegis-brain"
            target="_blank"
            rel="noopener noreferrer"
            className="text-[#B91C1C] hover:underline flex items-center gap-1"
          >
            GitHub <ArrowRight className="w-3 h-3" />
          </a>
        </nav>

        {/* Action Buttons: Star + Install */}
        <div className="hidden sm:flex items-center gap-3">
          <a
            href="https://github.com/PG300604/aegis-brain"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 text-xs font-bold px-3.5 py-1.5 rounded bg-[#FAF8F5] text-black border-2 border-black shadow-[3px_3px_0px_#000000] hover:bg-neutral-100 transition-transform hover:-translate-y-0.5 font-nikkei uppercase"
          >
            <Star className="w-3.5 h-3.5 text-[#B91C1C] fill-[#B91C1C]" />
            <span>Star</span>
          </a>

          <a
            href="#install"
            className="flex items-center gap-1.5 text-xs font-bold px-4 py-1.5 rounded bg-black text-white border-2 border-black shadow-[3px_3px_0px_#B91C1C] hover:bg-zinc-900 transition-transform hover:-translate-y-0.5 font-nikkei uppercase"
          >
            <Terminal className="w-3.5 h-3.5 text-[#D4AF37]" />
            <span>Install CLI</span>
          </a>
        </div>

        {/* Mobile Menu Toggle */}
        <div className="flex md:hidden items-center gap-2">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 rounded bg-black border border-white/20 text-white"
            aria-label="Toggle Navigation Menu"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden mt-2 p-4 bg-[#101116] border-2 border-black rounded-lg shadow-[6px_6px_0px_#000000] space-y-2 text-white font-nikkei uppercase text-xs">
          {navLinks.map((link) => (
            <a
              key={link.href}
              href={link.href}
              onClick={() => setMobileMenuOpen(false)}
              className="block py-2 px-3 rounded hover:bg-white/5"
            >
              {link.label}
            </a>
          ))}
          <a
            href="https://github.com/PG300604/aegis-brain"
            target="_blank"
            rel="noopener noreferrer"
            className="block py-2 px-3 rounded text-[#B91C1C] font-bold"
          >
            GitHub Repository →
          </a>
        </div>
      )}
    </header>
  );
}
