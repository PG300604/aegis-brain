"use client";

import React, { useState } from "react";
import {
  FileCode2,
  GitMerge,
  Cpu,
  ShieldAlert,
  Lock,
  ArrowRight,
  Terminal,
  Activity,
  CheckCircle2,
  Layers,
} from "lucide-react";

export interface Feature06PipelineFlowProps {
  className?: string;
  initialStepIndex?: number;
}

const PIPELINE_STEPS = [
  {
    id: "STEP-01",
    code: "INGEST_AST",
    title: "Lexical Spec Ingestion",
    latency: "2.1ms",
    tokens: "148 TK",
    icon: FileCode2,
    invariant: "∀ S ∈ Spec : ValidUTF8(S) ∧ SchemaConformant(S, v6.4)",
    summary:
      "Parses raw domain requirements into a canonical, ambiguity-free Abstract Syntax Tree.",
    inputShape: `{
  raw_spec: string;      // Markdown / DSL input
  strict_mode: true;     // Rejects unbounded wildcards
  context_hash: "0x8F9A";
}`,
    outputShape: `{
  ast_root: ASTNode;     // 42 normalized primitives
  symbol_table: Map<ID, Type>;
  ambiguity_score: 0.000;
}`,
    telemetry: [
      { key: "AST DEPTH", val: "6 LEVELS" },
      { key: "PRUNED NODES", val: "14 REDUNDANT" },
      { key: "HASH VERIFIED", val: "SHA3-256" },
    ],
  },
  {
    id: "STEP-02",
    code: "TOPO_DAG",
    title: "Topological Graph Solve",
    latency: "4.6ms",
    tokens: "312 TK",
    icon: GitMerge,
    invariant: "∀ (u, v) ∈ Edges : ¬Path(v, u) — Strict Acyclic Guarantee",
    summary:
      "Resolves module dependencies into a deterministic Directed Acyclic Graph with zero circular locks.",
    inputShape: `{
  ast_root: ASTNode;
  symbol_table: Map<ID, Type>;
  max_fanout: 8;
}`,
    outputShape: `{
  dag_matrix: AdjacencyMatrix[18x18];
  execution_tiers: Tier[4];
  critical_path_ms: 11.4;
}`,
    telemetry: [
      { key: "GRAPH EDGES", val: "38 DIRECTED" },
      { key: "CYCLE CHECK", val: "0 DETECTED" },
      { key: "PARALLELISM", val: "4.2x SPEEDUP" },
    ],
  },
  {
    id: "STEP-03",
    code: "SYNTH_BLUEPRINT",
    title: "Neural Blueprint Synthesis",
    latency: "9.8ms",
    tokens: "640 TK",
    icon: Cpu,
    invariant: "Cost(Blueprint) ≤ 0.042 · Cost(Baseline_Monolith)",
    summary:
      "Synthesizes memory-aligned architectural plates, interface contracts, and state boundaries.",
    inputShape: `{
  dag_matrix: AdjacencyMatrix[18x18];
  target_runtime: "AegisVM-x64";
  memory_budget_kb: 512;
}`,
    outputShape: `{
  blueprint_ir: PlateIR[12];
  contract_stubs: Interface[24];
  compute_saved: "95.8%";
}`,
    telemetry: [
      { key: "IR PLATES", val: "12 GENERATED" },
      { key: "MEM FOOTPRINT", val: "184 KB" },
      { key: "CACHE HIT", val: "99.4%" },
    ],
  },
  {
    id: "STEP-04",
    code: "FORMAL_PROVE",
    title: "Invariant Proof Gate",
    latency: "5.2ms",
    tokens: "190 TK",
    icon: ShieldAlert,
    invariant: "∑ Pass(Theorem_i) / 286 = 1.000 — Zero Unchecked States",
    summary:
      "Executes SMT solver passes across all 286 formal safety and latency theorems prior to emission.",
    inputShape: `{
  blueprint_ir: PlateIR[12];
  theorem_suite: "AegisCore_286";
  timeout_ms: 10;
}`,
    outputShape: `{
  proof_certificate: QED_Cert;
  passed_assertions: 286;
  failed_assertions: 0;
}`,
    telemetry: [
      { key: "SMT SOLVER", val: "Z3-DETERMINISTIC" },
      { key: "ASSERTIONS", val: "286 / 286 PASS" },
      { key: "RACE CONDITIONS", val: "0 POSSIBLE" },
    ],
  },
  {
    id: "STEP-05",
    code: "SEAL_EMIT",
    title: "Cryptographic Plate Lock",
    latency: "2.3ms",
    tokens: "64 TK",
    icon: Lock,
    invariant: "VerifySig(Blueprint, SovereignKey) = TRUE",
    summary:
      "Seals the verified architectural blueprint into an immutable binary plate ready for zero-copy dispatch.",
    inputShape: `{
  blueprint_ir: PlateIR[12];
  proof_certificate: QED_Cert;
  signing_key: "AEGIS_SOVEREIGN_06";
}`,
    outputShape: `{
  artifact_id: "PLATE-06-A86";
  immutable_digest: "0x99F1...C40B";
  total_pipeline_ms: 24.0;
}`,
    telemetry: [
      { key: "ARTIFACT SIZE", val: "48.2 KB" },
      { key: "SIGNATURE", val: "ED25519-LOCKED" },
      { key: "DISPATCH STATE", val: "READY" },
    ],
  },
] as const;

export function Feature06PipelineFlow({
  className = "",
  initialStepIndex = 2,
}: Feature06PipelineFlowProps) {
  const [activeIdx, setActiveIdx] = useState<number>(
    Math.min(Math.max(initialStepIndex, 0), PIPELINE_STEPS.length - 1)
  );

  const activeStep = PIPELINE_STEPS[activeIdx];
  const ActiveIcon = activeStep.icon;

  return (
    <section
      className={`bg-[#070709] text-zinc-100 p-6 md:p-8 border-2 border-zinc-800 rounded-none font-sans selection:bg-[#B91C1C] selection:text-white ${className}`}
    >
      <style>{`
        @keyframes aegisSignalPulse {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(250%); }
        }
        .animate-aegis-pulse {
          animation: aegisSignalPulse 1.6s cubic-bezier(0.4, 0, 0.2, 1) infinite;
        }
      `}</style>

      <div className="max-w-6xl mx-auto space-y-6">
        {/* Top Comic Plate Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b-2 border-zinc-800 pb-5">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 bg-[#B91C1C] text-white px-2.5 py-1 border-2 border-black shadow-[3px_3px_0px_#000000]">
              <Layers className="w-3.5 h-3.5 stroke-[2.5]" />
              <span className="font-mono text-xs uppercase tracking-widest font-bold">
                FEATURE 06 // EXECUTION PIPELINE
              </span>
            </div>
            <h2 className="text-2xl md:text-4xl font-black tracking-tight uppercase text-[#FAF8F5]">
              5-Stage Deterministic Node Flow
            </h2>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <div className="bg-[#101116] border-2 border-zinc-800 px-3 py-1.5">
              <span className="font-mono text-xs uppercase tracking-widest text-zinc-400">
                TOTAL LATENCY:{" "}
                <strong className="text-[#FAF8F5]">24.0ms</strong>
              </span>
            </div>
            <div className="bg-[#FAF8F5] text-black border-2 border-black px-3 py-1.5 shadow-[3px_3px_0px_#B91C1C]">
              <span className="font-mono text-xs uppercase tracking-widest font-bold">
                TOTAL TOKENS: <span className="text-[#B91C1C]">1,354 TK</span>
              </span>
            </div>
          </div>
        </div>

        {/* Interactive 5-Node Chain */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="font-mono text-xs uppercase tracking-widest text-zinc-400">
              SELECT ANY ARCHITECTURAL NODE TO INSPECT TELEMETRY & INVARIANTS
            </span>
            <span className="font-mono text-xs uppercase tracking-widest text-[#DC2626] font-bold">
              ACTIVE: {activeStep.id} ({activeStep.code})
            </span>
          </div>

          <div className="flex flex-col lg:flex-row items-stretch justify-between gap-0 pt-2">
            {PIPELINE_STEPS.map((step, idx) => {
              const Icon = step.icon;
              const isSelected = idx === activeIdx;
              const isCompleted = idx <= activeIdx;

              return (
                <React.Fragment key={step.id}>
                  {/* Node Card */}
                  <button
                    type="button"
                    onClick={() => setActiveIdx(idx)}
                    aria-pressed={isSelected}
                    className={`group relative flex-1 text-left p-4 border-2 border-black rounded-none transition-all duration-150 focus:outline-none cursor-pointer ${
                      isSelected
                        ? "bg-[#FAF8F5] text-[#0D0D11] shadow-[4px_4px_0px_#B91C1C] -translate-y-1 z-10"
                        : "bg-[#101116] text-zinc-100 border-zinc-700 hover:bg-[#FAF8F5] hover:text-[#0D0D11] hover:border-black shadow-[4px_4px_0px_#000000]"
                    }`}
                  >
                    {/* Top Row: Step Badge + Icon */}
                    <div
                      className={`flex items-center justify-between pb-2 mb-2.5 border-b-2 ${
                        isSelected
                          ? "border-black"
                          : "border-zinc-800 group-hover:border-black"
                      }`}
                    >
                      <span
                        className={`font-mono text-xs uppercase tracking-widest font-bold px-1.5 py-0.5 border border-black ${
                          isSelected
                            ? "bg-[#B91C1C] text-white"
                            : isCompleted
                            ? "bg-black text-[#FAF8F5]"
                            : "bg-zinc-900 text-zinc-400"
                        }`}
                      >
                        {step.id}
                      </span>
                      <Icon
                        className={`w-4 h-4 stroke-[2.5] ${
                          isSelected
                            ? "text-[#B91C1C]"
                            : "text-zinc-400 group-hover:text-black"
                        }`}
                      />
                    </div>

                    {/* Node Code & Title */}
                    <div className="font-mono text-[11px] uppercase tracking-widest text-[#B91C1C] font-bold">
                      {step.code}
                    </div>
                    <div className="font-black text-sm uppercase tracking-tight leading-snug mt-0.5">
                      {step.title}
                    </div>

                    {/* Live Latency & Token Footers */}
                    <div
                      className={`mt-4 pt-2 border-t flex items-center justify-between font-mono text-[11px] uppercase tracking-wider ${
                        isSelected
                          ? "border-zinc-300 text-zinc-800"
                          : "border-zinc-800 text-zinc-400 group-hover:border-zinc-300 group-hover:text-zinc-800"
                      }`}
                    >
                      <span className="font-bold">{step.latency}</span>
                      <span>{step.tokens}</span>
                    </div>
                  </button>

                  {/* Animated Signal Conduit Between Nodes */}
                  {idx < PIPELINE_STEPS.length - 1 && (
                    <div className="flex lg:flex-col items-center justify-center py-2 lg:py-0 lg:px-1.5 select-none">
                      <div className="relative w-12 lg:w-8 h-2.5 bg-[#101116] border-2 border-black overflow-hidden flex items-center">
                        <div
                          className={`w-1/2 h-full animate-aegis-pulse ${
                            idx < activeIdx ? "bg-[#B91C1C]" : "bg-zinc-500"
                          }`}
                        />
                      </div>
                      <ArrowRight
                        className={`hidden lg:block w-3.5 h-3.5 mt-1 stroke-[2.5] ${
                          idx < activeIdx ? "text-[#DC2626]" : "text-zinc-600"
                        }`}
                      />
                    </div>
                  )}
                </React.Fragment>
              );
            })}
          </div>
        </div>

        {/* Active Node Inspection Plate (#FAF8F5 Paper Contrast) */}
        <div className="bg-[#FAF8F5] text-[#0D0D11] border-2 border-black shadow-[4px_4px_0px_#B91C1C] rounded-none">
          {/* Inspector Banner */}
          <div className="bg-black text-[#FAF8F5] px-4 py-3 border-b-2 border-black flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div className="flex items-center gap-2.5">
              <span className="bg-[#B91C1C] text-white font-mono text-xs uppercase tracking-widest font-bold px-2 py-0.5 border border-black">
                {activeStep.id} INSPECTOR
              </span>
              <span className="font-mono text-xs uppercase tracking-widest font-bold text-[#FAF8F5]">
                {"//"} {activeStep.code} — {activeStep.title}
              </span>
            </div>

            <div className="flex items-center gap-3 font-mono text-xs uppercase tracking-widest">
              <span className="flex items-center gap-1 text-zinc-300">
                <Activity className="w-3.5 h-3.5 text-[#DC2626]" />
                {activeStep.latency}
              </span>
              <span className="text-zinc-600">|</span>
              <span className="text-[#FAF8F5] font-bold">
                {activeStep.tokens}
              </span>
            </div>
          </div>

          <div className="p-5 md:p-6 space-y-6">
            {/* Summary + Mathematical Invariant Box */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 items-stretch">
              <div className="lg:col-span-5 flex flex-col justify-between bg-white border-2 border-black p-4 shadow-[3px_3px_0px_#000000]">
                <div className="flex items-center gap-2 font-mono text-xs uppercase tracking-widest font-bold text-zinc-600 mb-2">
                  <ActiveIcon className="w-4 h-4 text-[#B91C1C] stroke-[2.5]" />
                  <span>OPERATIONAL SPECIFICATION</span>
                </div>
                <p className="text-sm font-semibold text-[#0D0D11] leading-relaxed">
                  {activeStep.summary}
                </p>
              </div>

              <div className="lg:col-span-7 flex flex-col justify-between bg-[#070709] text-[#FAF8F5] border-2 border-black p-4 shadow-[3px_3px_0px_#B91C1C]">
                <div className="flex items-center justify-between gap-2 mb-2">
                  <span className="font-mono text-xs uppercase tracking-widest font-bold text-[#DC2626]">
                    STEP MATHEMATICAL INVARIANT
                  </span>
                  <span className="inline-flex items-center gap-1 font-mono text-[11px] uppercase tracking-widest bg-[#B91C1C] text-white px-2 py-0.5 font-bold">
                    <CheckCircle2 className="w-3 h-3" /> ENFORCED
                  </span>
                </div>
                <code className="font-mono text-xs md:text-sm font-bold text-[#FAF8F5] bg-[#101116] p-2.5 border border-zinc-800 block break-all">
                  {activeStep.invariant}
                </code>
              </div>
            </div>

            {/* Input / Output Data Shapes */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Input Payload */}
              <div className="border-2 border-black bg-[#070709] text-zinc-100 shadow-[4px_4px_0px_#000000]">
                <div className="bg-zinc-900 border-b-2 border-black px-3.5 py-2 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Terminal className="w-3.5 h-3.5 text-zinc-400" />
                    <span className="font-mono text-xs uppercase tracking-widest font-bold text-zinc-200">
                      INPUT DATA SHAPE
                    </span>
                  </div>
                  <span className="font-mono text-[11px] uppercase tracking-widest text-zinc-400">
                    READ-ONLY
                  </span>
                </div>
                <pre className="p-4 font-mono text-xs leading-relaxed text-zinc-200 overflow-x-auto">
                  <code>{activeStep.inputShape}</code>
                </pre>
              </div>

              {/* Output Payload */}
              <div className="border-2 border-black bg-[#070709] text-zinc-100 shadow-[4px_4px_0px_#B91C1C]">
                <div className="bg-[#B91C1C] border-b-2 border-black px-3.5 py-2 flex items-center justify-between text-white">
                  <div className="flex items-center gap-2">
                    <Terminal className="w-3.5 h-3.5" />
                    <span className="font-mono text-xs uppercase tracking-widest font-bold">
                      OUTPUT DATA SHAPE
                    </span>
                  </div>
                  <span className="font-mono text-[11px] uppercase tracking-widest font-bold bg-black px-1.5 py-0.5">
                    VERIFIED EMIT
                  </span>
                </div>
                <pre className="p-4 font-mono text-xs leading-relaxed text-[#FAF8F5] overflow-x-auto">
                  <code>{activeStep.outputShape}</code>
                </pre>
              </div>
            </div>

            {/* Live Node Telemetry Strip */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-1">
              {activeStep.telemetry.map((metric) => (
                <div
                  key={metric.key}
                  className="bg-white border-2 border-black px-3.5 py-2.5 flex items-center justify-between shadow-[3px_3px_0px_#000000]"
                >
                  <span className="font-mono text-xs uppercase tracking-widest text-zinc-600 font-bold">
                    {metric.key}
                  </span>
                  <span className="font-mono text-xs uppercase tracking-widest font-black text-[#0D0D11] bg-zinc-200 px-2 py-0.5 border border-black">
                    {metric.val}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Feature06PipelineFlow;
