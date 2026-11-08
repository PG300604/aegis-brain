"use client";

import React, { useState } from "react";
import { motion } from "motion/react";
import {
  Terminal,
  FileCode,
  Search,
  CheckCircle2,
  AlertTriangle,
  RotateCw,
  Clock,
  Sparkles,
} from "lucide-react";
import "./CallChip.css";

export type CallStatus = "running" | "done" | "error";

interface CallChipProps {
  toolName?: string;
  command?: string;
  duration?: string;
  status?: CallStatus;
  progress?: number; // 0 to 100
  onRetry?: () => void;
  className?: string;
}

export function CallChip({
  toolName = "aegis recall",
  command = "sqlite3 brain.db 'SELECT * FROM memories...'",
  duration = "21 ms",
  status = "done",
  progress = 100,
  onRetry,
  className = "",
}: CallChipProps) {
  const [currentStatus, setCurrentStatus] = useState<CallStatus>(status);
  const [currentProgress, setCurrentProgress] = useState<number>(progress);

  const handleSimulateRetry = () => {
    setCurrentStatus("running");
    setCurrentProgress(25);
    setTimeout(() => setCurrentProgress(75), 200);
    setTimeout(() => {
      setCurrentProgress(100);
      setCurrentStatus("done");
      if (onRetry) onRetry();
    }, 450);
  };

  const getToolIcon = () => {
    if (toolName.includes("recall") || toolName.includes("search")) return Search;
    if (toolName.includes("pipeline") || toolName.includes("gate")) return FileCode;
    return Terminal;
  };

  const ToolIcon = getToolIcon();

  return (
    <div className={`call-chip-container ${currentStatus} px-3 py-1.5 gap-2 text-xs font-mono ${className}`}>
      {/* Wipe Fill Progress */}
      <div
        className="wipe-fill-progress"
        style={{
          width: `${currentProgress}%`,
          background:
            currentStatus === "error"
              ? "rgba(239, 68, 68, 0.2)"
              : currentStatus === "running"
              ? "rgba(0, 240, 255, 0.25)"
              : "rgba(16, 185, 129, 0.2)",
        }}
      />

      {/* Tool Icon with status indicator */}
      <div className="flex items-center gap-1.5 shrink-0 z-10">
        {currentStatus === "running" ? (
          <RotateCw className="w-3.5 h-3.5 text-cyan-400 animate-spin" />
        ) : currentStatus === "error" ? (
          <AlertTriangle className="w-3.5 h-3.5 text-red-400" />
        ) : (
          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
        )}

        <span className="font-bold text-white tracking-wide">{toolName}</span>
      </div>

      {/* Command detail snippet */}
      <div className="hidden sm:inline-block text-[11px] text-zinc-400 truncate max-w-[200px] z-10">
        {command}
      </div>

      {/* Execution duration / latency */}
      <div className="flex items-center gap-1 text-[10px] text-cyan-400 px-1.5 py-0.5 rounded bg-zinc-900/90 border border-zinc-800 z-10 shrink-0">
        <Clock className="w-2.5 h-2.5" />
        <span>{duration}</span>
      </div>

      {/* Retry Action */}
      {currentStatus === "error" && (
        <button
          type="button"
          onClick={handleSimulateRetry}
          className="p-1 rounded hover:bg-zinc-800 text-zinc-400 hover:text-white transition-colors z-10 cursor-pointer"
          title="Retry tool execution"
        >
          <RotateCw className="w-3 h-3" />
        </button>
      )}
    </div>
  );
}
