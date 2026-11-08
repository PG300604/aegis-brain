"use client";

import React, { useState } from "react";
import {
  Terminal,
  FileCode,
  Search,
  CheckCircle2,
  AlertTriangle,
  RotateCw,
  Clock,
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
    if (toolName.includes("pipeline") || toolName.includes("gate") || toolName.includes("ast")) return FileCode;
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
              ? "rgba(185, 28, 28, 0.15)"
              : currentStatus === "running"
              ? "rgba(212, 175, 55, 0.2)"
              : "rgba(16, 185, 129, 0.15)",
        }}
      />

      {/* Tool Icon with status indicator */}
      <div className="flex items-center gap-1.5 shrink-0 z-10">
        {currentStatus === "running" ? (
          <RotateCw className="w-3.5 h-3.5 text-[#D4AF37] animate-spin" />
        ) : currentStatus === "error" ? (
          <AlertTriangle className="w-3.5 h-3.5 text-[#B91C1C]" />
        ) : (
          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-700" />
        )}

        <span className="font-nikkei font-bold uppercase tracking-wider text-black">{toolName}</span>
      </div>

      {/* Command detail snippet */}
      <div className="hidden sm:inline-block text-[11px] text-black/60 truncate max-w-[200px] z-10 font-mono">
        {command}
      </div>

      {/* Execution duration / latency */}
      <div className="flex items-center gap-1 text-[10px] text-black font-bold px-1.5 py-0.5 rounded bg-white border border-black shadow-[1px_1px_0px_#000000] z-10 shrink-0">
        <Clock className="w-2.5 h-2.5 text-[#B91C1C]" />
        <span>{duration}</span>
      </div>

      {/* Retry Action */}
      {currentStatus === "error" && (
        <button
          type="button"
          onClick={handleSimulateRetry}
          className="ml-auto text-[10px] font-nikkei uppercase px-1.5 py-0.5 rounded bg-[#B91C1C] text-white hover:bg-red-800 z-10 cursor-pointer border border-black shadow-[1px_1px_0px_#000000]"
        >
          RETRY
        </button>
      )}
    </div>
  );
}
