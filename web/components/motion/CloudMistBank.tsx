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
      <svg
        viewBox="0 0 1440 320"
        className="w-full h-auto block drop-shadow-[0_-12px_24px_rgba(0,0,0,0.65)]"
        preserveAspectRatio="none"
        fill="none"
      >
        {/* 
          ========================================================================
          3 ORGANIC FLOATING SMOKE DROPLETS (Directly above central smoke summit)
          ========================================================================
        */}
        {/* Droplet 1: Left wisp above shoulder (x=670, y=35) */}
        <motion.g
          animate={{ y: [-4, 4, -4], x: [-1.5, 1.5, -1.5] }}
          transition={{ duration: 4.2, repeat: Infinity, ease: "easeInOut" }}
        >
          <path
            d="M 664,35 C 663,28 669,23 675,25 C 681,27 685,32 683,38 C 681,43 673,46 668,44 C 664,42 664,39 664,35 Z"
            fill={fillColor}
            stroke="#000000"
            strokeWidth="2.5"
            strokeLinejoin="round"
          />
        </motion.g>

        {/* Droplet 2: Central summit droplet (x=720, y=15) */}
        <motion.g
          animate={{ y: [-5, 5, -5], x: [1, -1, 1] }}
          transition={{ duration: 5.0, repeat: Infinity, ease: "easeInOut", delay: 0.5 }}
        >
          <path
            d="M 712,15 C 711,7 718,2 726,4 C 733,6 738,12 736,19 C 734,25 726,28 719,26 C 713,24 712,19 712,15 Z"
            fill={fillColor}
            stroke="#000000"
            strokeWidth="2.5"
            strokeLinejoin="round"
          />
        </motion.g>

        {/* Droplet 3: Right wisp above shoulder (x=770, y=30) */}
        <motion.g
          animate={{ y: [-3.5, 3.5, -3.5], x: [-1, 1, -1] }}
          transition={{ duration: 4.6, repeat: Infinity, ease: "easeInOut", delay: 1.0 }}
        >
          <path
            d="M 764,30 C 763,24 768,20 774,21 C 780,22 784,27 782,32 C 780,37 773,39 768,38 C 764,36 764,33 764,30 Z"
            fill={fillColor}
            stroke="#000000"
            strokeWidth="2.5"
            strokeLinejoin="round"
          />
        </motion.g>

        {/* 
          ========================================================================
          MONUMENTAL ORGANIC CUMULUS CLOUD BANK (Graphic Novel Woodcut Contour)
          ========================================================================
        */}
        <path
          d="M 0,320 
             L 0,240 
             C 20,230 40,222 65,225 
             C 80,205 110,200 130,210 
             C 150,180 185,165 215,175 
             C 235,150 275,150 295,170 
             C 315,140 355,135 375,155 
             C 395,120 440,110 465,128 
             C 490,105 528,98 550,122 
             C 575,95 605,78 635,96 
             C 655,75 685,62 720,75 
             C 755,62 785,75 805,96 
             C 835,78 865,95 890,122 
             C 912,98 950,105 975,128 
             C 1000,110 1045,120 1065,155 
             C 1085,135 1125,140 1145,170 
             C 1165,150 1205,150 1225,175 
             C 1255,165 1290,180 1310,210 
             C 1330,200 1360,205 1375,225 
             C 1400,222 1420,230 1440,240 
             L 1440,320 Z"
          fill={fillColor}
          stroke="#000000"
          strokeWidth="2.5"
          strokeLinejoin="round"
        />

        {/* 
          ========================================================================
          GRAPHIC NOVEL INK OVERLAP CONTOURS (Black ink crevice creases)
          ========================================================================
        */}
        <g stroke="#000000" strokeWidth="2" strokeLinecap="round" fill="none">
          <path d="M 215,175 C 220,190 222,202 218,212" />
          <path d="M 295,170 C 302,185 304,196 300,206" />
          <path d="M 465,128 C 474,144 478,158 474,170" />
          <path d="M 550,122 C 556,138 558,150 554,162" />
          <path d="M 635,96 C 644,114 648,130 644,144" />
          <path d="M 696,88 C 714,79 732,84 744,95" />
          <path d="M 805,96 C 796,114 792,130 796,144" />
          <path d="M 890,122 C 884,138 882,150 886,162" />
          <path d="M 975,128 C 966,144 962,158 966,170" />
          <path d="M 1145,170 C 1138,185 1136,196 1140,206" />
          <path d="M 1225,175 C 1220,190 1218,202 1222,212" />
        </g>
      </svg>
    </div>
  );
}
