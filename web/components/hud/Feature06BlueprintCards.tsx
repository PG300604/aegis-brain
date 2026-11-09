"use client";

import React, { useState } from "react";
import {
  Cpu,
  Database,
  Scissors,
  ShieldAlert,
  Activity,
  CheckSquare,
  Terminal,
  ArrowRight,
  Copy,
  Check,
  Layers,
  Lock,
} from "lucide-react";

export interface Feature06BlueprintCardsProps {
  className?: string;
  initialBlueprintIndex?: number;
}

const BLUEPRINTS = [
  {
    id: "BP-01",
    shortTitle: "System Architecture",
    title: "Sovereign Tri-Tier System Topology",
    subtitle: "Deterministic Command & Dispatch Mesh",
    icon: Cpu,
    hierarchy: {
      coordinator: {
        name: "AegisRootOrchestrator",
        role: "Global DAG Scheduler & State Lock",
        latency: "0.4ms",
      },
      leader: {
        name: "DomainPlannerSubagent",
        role: "Context Partitioning & Subtree Routing",
        latency: "1.2ms",
      },
      engine: {
        name: "ZeroCopyWorkerPool[16]",
        role: "Isolated Sandboxed AST & Binary Execution",
        latency: "4.8ms",
      },
    },
    codeTitle: "aegis_topology.toml // RUNTIME MESH CONFIG",
    codeLang: "TOML / ARCH SPEC",
    codeContent: `[mesh.coordinator]
node_id        = "AEGIS_ROOT_01"
consensus_mode = "DETERMINISTIC_DAG"
max_fanout     = 16
heartbeat_ms   = 5

[mesh.subagent_leader]
partition_strategy = "STRICT_ISOLATION"
memory_arena_kb    = 2048
backpressure_limit = 0.85

[mesh.execution_engine]
worker_threads     = 16
zero_copy_ipc      = true
ring_buffer_bytes  = 65536
VerifyLock(mesh)   == "0x9A8F_LOCKED"`,
    metrics: [
      { label: "MESH HOP LATENCY", value: "0.42ms", sub: "ZERO-COPY IPC" },
      { label: "CONCURRENCY CAP", value: "16 NODES", sub: "LOCK-FREE RING" },
      { label: "STATE OVERHEAD", value: "12.4 KB", sub: "STATIC ARENA" },
      { label: "UPTIME SLA", value: "99.999%", sub: "BYZANTINE SAFE" },
    ],
    invariants: [
      {
        id: "INV-01.A",
        formula: "∀ Node ∈ Mesh : ParentCount(Node) == 1",
        desc: "Strict tree hierarchy prevents split-brain command contention.",
      },
      {
        id: "INV-01.B",
        formula: "T_ipc(Coordinator → Engine) ≤ 0.50ms",
        desc: "Shared-memory ring buffers bypass kernel socket serialization.",
      },
      {
        id: "INV-01.C",
        formula: "MemAlloc(Runtime) == StaticArena(2048KB)",
        desc: "Zero dynamic heap allocations after boot initialization.",
      },
      {
        id: "INV-01.D",
        formula: "DeadlockFree(DAG_Schedule) == TRUE",
        desc: "Topological sort enforces monotonic forward execution.",
      },
    ],
  },
  {
    id: "BP-02",
    shortTitle: "SQLite FTS5 Memory Bus",
    title: "SQLite WAL + FTS5 Vectorless Memory Bus",
    subtitle: "Sub-Millisecond Lexical & BM25 Episodic Recall",
    icon: Database,
    hierarchy: {
      coordinator: {
        name: "MemoryBusController",
        role: "WAL Checkpoint & Transaction Serializer",
        latency: "0.2ms",
      },
      leader: {
        name: "FTS5QueryPlanner",
        role: "BM25 Ranking & Prefix Token Expansion",
        latency: "0.9ms",
      },
      engine: {
        name: "MmapPageEngine",
        role: "Zero-Syscall Memory-Mapped B-Tree Scans",
        latency: "1.4ms",
      },
    },
    codeTitle: "memory_bus_fts5.sql // SCHEMA & PRAGMA",
    codeLang: "SQLITE3 / WAL",
    codeContent: `PRAGMA journal_mode = WAL;
PRAGMA synchronous  = NORMAL;
PRAGMA mmap_size    = 268435456; -- 256MB Zero-Syscall MMap
PRAGMA temp_store   = MEMORY;

CREATE VIRTUAL TABLE IF NOT EXISTS aegis_episodic_fts USING fts5(
  trace_id UNINDEXED,
  blueprint_rev,
  symbol_path,
  payload_ast,
  tokenize = 'porter unicode61 remove_diacritics 2'
);

SELECT trace_id, bm25(aegis_episodic_fts, 1.2, 0.75) AS rank
FROM aegis_episodic_fts
WHERE aegis_episodic_fts MATCH 'invariant NEAR/3 lock'
ORDER BY rank ASC LIMIT 8;`,
    metrics: [
      { label: "BM25 P99 QUERY", value: "1.40ms", sub: "100K DOC CORPUS" },
      { label: "MMAP WINDOW", value: "256 MB", sub: "RAM-RESIDENT" },
      { label: "WRITE THROUGHPUT", value: "48K/sec", sub: "WAL BATCHED" },
      { label: "EMBEDDING COST", value: "$0.00", sub: "PURE LEXICAL FTS5" },
    ],
    invariants: [
      {
        id: "INV-02.A",
        formula: "Readers(WAL) ⫽ Writers(WAL) == NonBlocking",
        desc: "Concurrent subagent reads never stall single-writer commits.",
      },
      {
        id: "INV-02.B",
        formula: "T_query(FTS5_BM25, N=10^5) < 2.0ms",
        desc: "Memory-mapped inverted indices guarantee sub-2ms retrieval.",
      },
      {
        id: "INV-02.C",
        formula: "ExternalVectorDB_Deps == 0",
        desc: "Eliminates network hops and floating-point drift entirely.",
      },
      {
        id: "INV-02.D",
        formula: "CRC32(WAL_Frame_i) == Verified",
        desc: "Every episodic memory frame is checksummed prior to commit.",
      },
    ],
  },
  {
    id: "BP-03",
    shortTitle: "Token Arbitrage & Pruning",
    title: "AST-Aware Token Arbitrage & Context Pruning",
    subtitle: "95.8% Compute Reduction via Structural Dead-Code Stripping",
    icon: Scissors,
    hierarchy: {
      coordinator: {
        name: "BudgetArbitrageGovernor",
        role: "Dynamic Context Window Quota Allocation",
        latency: "0.3ms",
      },
      leader: {
        name: "SemanticEntropyScorer",
        role: "Information Density & Salience Filtering",
        latency: "1.8ms",
      },
      engine: {
        name: "TreeSitterSlicer",
        role: "AST Signature Extraction & Body Elision",
        latency: "2.1ms",
      },
    },
    codeTitle: "pruner_arbitrage.rs // AST SLICER PASS",
    codeLang: "RUST / ENGINE",
    codeContent: `pub fn prune_context_plate(ast: &ModuleAST, budget_tk: usize) -> CompactPlate {
    let mut plate = CompactPlate::with_capacity(budget_tk);
    for node in ast.topological_defs() {
        if node.entropy_score() >= ENTROPY_THRESHOLD_0_82 {
            plate.push_signature_only(node.header_span());
        } else {
            plate.elide_with_hash(node.symbol_id(), node.sha256());
        }
    }
    assert!(plate.token_count() <= (ast.raw_tokens() * 42) / 1000);
    plate.seal_deterministic()
}`,
    metrics: [
      { label: "TOKEN REDUCTION", value: "95.8%", sub: "VS RAW REPO DUMP" },
      { label: "RETAINED RECALL", value: "99.4%", sub: "SIGNATURE GRAPH" },
      { label: "SLICER LATENCY", value: "2.1ms", sub: "INCREMENTAL AST" },
      { label: "COST PER RUN", value: "$0.0014", sub: "23.8x CHEAPER" },
    ],
    invariants: [
      {
        id: "INV-03.A",
        formula: "Tokens(Pruned) ≤ 0.042 × Tokens(Raw)",
        desc: "Hard upper bound on emitted context tokens per synthesis pass.",
      },
      {
        id: "INV-03.B",
        formula: "TypeGraph(Pruned) ⊆ TypeGraph(Raw)",
        desc: "All public interface contracts and types remain 100% intact.",
      },
      {
        id: "INV-03.C",
        formula: "Entropy(DroppedNode) < 0.18",
        desc: "Only boilerplate implementation bodies are replaced by hashes.",
      },
      {
        id: "INV-03.D",
        formula: "Reconstructable(ElidedHash, SQLiteBus) == TRUE",
        desc: "Any elided block can be hydrated in O(1) from FTS5 storage.",
      },
    ],
  },
  {
    id: "BP-04",
    shortTitle: "Win32 Keepalive Daemon",
    title: "Win32 JobObject & NamedPipe Keepalive Daemon",
    subtitle: "Zero-Orphan Process Supervision & Instant Crash Resurrection",
    icon: ShieldAlert,
    hierarchy: {
      coordinator: {
        name: "Win32ServiceSentinel",
        role: "JobObject Handle Owner & SCM Watchdog",
        latency: "0.1ms",
      },
      leader: {
        name: "IOCPHeartbeatMultiplexer",
        role: "NamedPipe Ping/Pong & Hang Detection",
        latency: "0.5ms",
      },
      engine: {
        name: "ProcessRespawnWorker",
        role: "Warm Snapshot Restore & Handle Inheritance",
        latency: "3.2ms",
      },
    },
    codeTitle: "win32_keepalive.c // JOB OBJECT & IOCP GUARD",
    codeLang: "C11 / WIN32 API",
    codeContent: `HANDLE hJob = CreateJobObjectW(NULL, L"Global\\\\AegisSovereignJob06");
JOBOBJECT_EXTENDED_LIMIT_INFORMATION jeli = {0};
jeli.BasicLimitInformation.LimitFlags =
    JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE |
    JOB_OBJECT_LIMIT_ACTIVE_PROCESS |
    JOB_OBJECT_LIMIT_JOB_MEMORY;
jeli.BasicLimitInformation.ActiveProcessLimit = 16;
jeli.JobMemoryLimit = 512 * 1024 * 1024; // Hard 512MB Ceiling

SetInformationJobObject(hJob, JobObjectExtendedLimitInformation, &jeli, sizeof(jeli));
AssignProcessToJobObject(hJob, hWorkerProc); // Zero zombie guarantee`,
    metrics: [
      { label: "RESPAWN TIME", value: "3.8ms", sub: "WARM HANDLE POOL" },
      { label: "ORPHAN PROCESSES", value: "0 EVER", sub: "KILL_ON_JOB_CLOSE" },
      { label: "MEMORY CEILING", value: "512 MB", sub: "KERNEL ENFORCED" },
      { label: "PING INTERVAL", value: "10.0ms", sub: "IOCP NAMED PIPE" },
    ],
    invariants: [
      {
        id: "INV-04.A",
        formula: "CloseHandle(hJob) ⟹ Terminate(∀ ChildProc)",
        desc: "Kernel guarantees zero zombie worker processes on daemon exit.",
      },
      {
        id: "INV-04.B",
        formula: "T_recover(CrashEvent) < 5.0ms",
        desc: "Pre-warmed suspended process slots resume immediately on fault.",
      },
      {
        id: "INV-04.C",
        formula: "RSS_Memory(JobGroup) ≤ 512 MB",
        desc: "Hard NT kernel limit prevents runaway memory leaks.",
      },
      {
        id: "INV-04.D",
        formula: "MissedHeartbeats(Worker) > 2 ⟹ Recycle(Worker)",
        desc: "Deterministic lockup recovery within 20ms of thread stall.",
      },
    ],
  },
  {
    id: "BP-05",
    shortTitle: "Telemetry Stream",
    title: "Lock-Free Ring Buffer Telemetry Stream",
    subtitle: "Nanosecond Binary Trace Emission with Zero Producer Stalls",
    icon: Activity,
    hierarchy: {
      coordinator: {
        name: "TelemetryAggregator",
        role: "Epoch Alignment & Anomaly Threshold Gate",
        latency: "0.2ms",
      },
      leader: {
        name: "SPSCChannelMux",
        role: "Cache-Line Padded Ring Buffer Multiplexing",
        latency: "0.4ms",
      },
      engine: {
        name: "BinaryFrameFlusher",
        role: "SIMD Wire Compression & Disk Append",
        latency: "0.8ms",
      },
    },
    codeTitle: "telemetry_ring.zig // CACHE-LINE ALIGNED SPSC",
    codeLang: "ZIG / LOCK-FREE",
    codeContent: `pub const TraceFrame = extern struct {
    timestamp_ns: u64 align(64),
    node_id:      u16,
    event_code:   u16,
    latency_us:   u32,
    token_delta:  u32,
    crc32_hash:   u32,
};

pub fn emitHotPath(ring: *RingBuffer, frame: TraceFrame) void {
    const write_idx = @atomicLoad(usize, &ring.head, .Monotonic);
    ring.slots[write_idx & RING_MASK] = frame;
    @atomicStore(usize, &ring.head, write_idx +% 1, .Release);
}`,
    metrics: [
      { label: "EMIT OVERHEAD", value: "42 ns", sub: "WAIT-FREE ATOMIC" },
      { label: "FRAME FOOTPRINT", value: "24 BYTES", sub: "PACKED BINARY" },
      { label: "RING CAPACITY", value: "65,536", sub: "POWER-OF-2 MASK" },
      { label: "PRODUCER STALLS", value: "0.00%", sub: "OVERWRITE OLDEST" },
    ],
    invariants: [
      {
        id: "INV-05.A",
        formula: "T_emit(TraceFrame) ≤ 50ns",
        desc: "Single atomic release store without mutex or syscall contention.",
      },
      {
        id: "INV-05.B",
        formula: "alignof(RingSlot) == 64 Bytes",
        desc: "Eliminates CPU L1/L2 false sharing between producer & consumer.",
      },
      {
        id: "INV-05.C",
        formula: "BlockingLocks(HotPath) == 0",
        desc: "Telemetry consumers never exert backpressure on neural execution.",
      },
      {
        id: "INV-05.D",
        formula: "Monotonic(timestamp_ns) == TRUE",
        desc: "RDTSC hardware counters enforce strict causal ordering.",
      },
    ],
  },
  {
    id: "BP-06",
    shortTitle: "Four-Stage Quality Gate",
    title: "286-Assertion Four-Stage Formal Quality Gate",
    subtitle: "AST Lint, Type-Check, SMT Invariant Proof & Determinism Audit",
    icon: CheckSquare,
    hierarchy: {
      coordinator: {
        name: "GatekeeperArbiter",
        role: "All-or-Nothing Cryptographic Release Seal",
        latency: "0.5ms",
      },
      leader: {
        name: "QuadStagePipelineRunner",
        role: "Parallel Verification Stage Orchestration",
        latency: "1.9ms",
      },
      engine: {
        name: "Z3TheoremVerifier",
        role: "286 Formal Invariant Assertions & Fuzzing",
        latency: "5.2ms",
      },
    },
    codeTitle: "quality_gate_286.sh // 4-STAGE VERIFICATION LOG",
    codeLang: "TERMINAL / VERIFIER",
    codeContent: `$ aegis-gate verify --blueprint BP-06 --strict-qed
[STAGE 1/4] AST_STRUCTURAL_LINT ........ PASS (0 warnings, 1.1ms)
[STAGE 2/4] STRICT_TYPE_BOUNDARIES ..... PASS (24/24 interfaces, 1.8ms)
[STAGE 3/4] SMT_FORMAL_INVARIANTS ...... PASS (286/286 theorems, 4.1ms)
[STAGE 4/4] BITWISE_DETERMINISM_AUDIT .. PASS (SHA3: 0x99F1C40B, 0.6ms)
------------------------------------------------------------------
VERDICT: Q.E.D. ENFORCED // ZERO REGRESSIONS // SEALED FOR DISPATCH`,
    metrics: [
      { label: "THEOREM SUITE", value: "286/286", sub: "100% REQUIRED PASS" },
      { label: "GATE LATENCY", value: "7.6ms", sub: "4 STAGES COMBINED" },
      { label: "FALSE POSITIVES", value: "0.00%", sub: "SOUND SMT PROOFS" },
      { label: "ESCAPE DEFECTS", value: "ZERO", sub: "HARD BLOCK ON FAIL" },
    ],
    invariants: [
      {
        id: "INV-06.A",
        formula: "∑ Pass(Stage_i) == 4 ⟹ EmitAllowed",
        desc: "Any single assertion failure immediately aborts artifact sealing.",
      },
      {
        id: "INV-06.B",
        formula: "PassCount(TheoremSuite) == 286",
        desc: "Zero skipped, mocked, or soft-failed tests permitted in production.",
      },
      {
        id: "INV-06.C",
        formula: "Hash(Run_1(Input)) == Hash(Run_N(Input))",
        desc: "Bitwise identical output across repeated synthesis executions.",
      },
      {
        id: "INV-06.D",
        formula: "CyclomaticComplexity(Fn) ≤ 10",
        desc: "Enforces Karpathy simplicity across all synthesized modules.",
      },
    ],
  },
  {
    id: "BP-07",
    shortTitle: "Quickstart Setup",
    title: "Zero-Dependency Single-Binary Quickstart",
    subtitle: "3-Command Cold Boot to Verified AegisBrain Runtime in 1.8s",
    icon: Terminal,
    hierarchy: {
      coordinator: {
        name: "BootstrapCLI",
        role: "Environment Checksum & Config Hydrator",
        latency: "0.3ms",
      },
      leader: {
        name: "MigrationInitializer",
        role: "SQLite FTS5 Provisioning & Key Generation",
        latency: "0.8ms",
      },
      engine: {
        name: "SelfTestIgnition",
        role: "286-Suite Cold Verification & Daemon Spawn",
        latency: "1.8s",
      },
    },
    codeTitle: "quickstart_ignition.sh // 3-STEP DEPLOYMENT",
    codeLang: "SHELL / IGNITION",
    codeContent: `# 1. Fetch static binary & verify Ed25519 sovereign signature
$ curl -fsSL https://aegisbrain.dev/install.sh | sh -s -- --verify-sig

# 2. Initialize SQLite FTS5 bus & lock Win32/POSIX keepalive daemon
$ aegis init --blueprint-rev 06.4 --mmap-mb 256 --strict

# 3. Execute 286-test formal self-check & launch blueprint engine
$ aegis ignite --verify-all
[OK] 286/286 Invariants Verified in 1.80s. Listening on ipc://aegis.sock`,
    metrics: [
      { label: "COLD BOOT TIME", value: "1.80s", sub: "INCLUDES 286 TESTS" },
      { label: "BINARY SIZE", value: "14.2 MB", sub: "STATICALLY LINKED" },
      { label: "EXTERNAL DEPS", value: "0 PACKAGES", sub: "NO NODE / DOCKER" },
      { label: "CONFIG LINES", value: "12 LINES", sub: "SANE DEFAULTS" },
    ],
    invariants: [
      {
        id: "INV-07.A",
        formula: "SharedLibDeps(aegis_bin) == ∅",
        desc: "Self-contained static executable runs on bare metal without Docker.",
      },
      {
        id: "INV-07.B",
        formula: "T_boot(ColdStart → Ready) ≤ 1.80s",
        desc: "Full database initialization and 286-test suite complete under 2s.",
      },
      {
        id: "INV-07.C",
        formula: "Idempotent(aegis init) == TRUE",
        desc: "Re-running initialization never corrupts existing episodic state.",
      },
      {
        id: "INV-07.D",
        formula: "Ed25519_Verify(Binary, PubKey) == VALID",
        desc: "Cryptographic provenance verified prior to first instruction.",
      },
    ],
  },
] as const;

export function Feature06BlueprintCards({
  className = "",
  initialBlueprintIndex = 0,
}: Feature06BlueprintCardsProps) {
  const [selectedIdx, setSelectedIdx] = useState<number>(
    Math.min(Math.max(initialBlueprintIndex, 0), BLUEPRINTS.length - 1)
  );
  const [copied, setCopied] = useState<boolean>(false);

  const active = BLUEPRINTS[selectedIdx];
  const ActiveIcon = active.icon;

  const handleCopyCode = () => {
    if (typeof navigator !== "undefined" && navigator.clipboard) {
      navigator.clipboard.writeText(active.codeContent);
      setCopied(true);
      setTimeout(() => setCopied(false), 1600);
    }
  };

  return (
    <section
      className={`bg-[#070709] text-zinc-100 p-6 md:p-8 border-2 border-zinc-800 rounded-none font-sans selection:bg-[#B91C1C] selection:text-white ${className}`}
    >
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Graphic Novel Editorial Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b-2 border-zinc-800 pb-5">
          <div className="space-y-2">
            <h2 className="text-2xl md:text-4xl font-black tracking-tight uppercase text-[#FAF8F5]">
              7 Live Sovereign System Plates
            </h2>
          </div>

          <div className="bg-[#FAF8F5] text-[#0D0D11] border-2 border-black px-3.5 py-2 shadow-[4px_4px_0px_#B91C1C] self-start md:self-end">
            <div className="font-mono text-xs uppercase tracking-widest font-bold">
              ACTIVE PLATE: <span className="text-[#B91C1C]">{active.id}</span>{" "}
              // 0{selectedIdx + 1} OF 07
            </div>
            <div className="font-mono text-[11px] uppercase tracking-widest text-zinc-700 font-semibold">
              SPEED: 1.8S  SAVED: 95.8%  LATENCY: 24MS  286/286 PASS
            </div>
          </div>
        </div>

        {/* 7-Blueprint Interactive Tab Selector */}
        <div className="space-y-2">
          <div className="font-mono text-xs uppercase tracking-widest text-zinc-400">
            SELECT ARCHITECTURAL BLUEPRINT PLATE (01 — 07):
          </div>
          <div
            role="tablist"
            aria-label="Master Architectural Blueprints"
            className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-2.5"
          >
            {BLUEPRINTS.map((bp, idx) => {
              const Icon = bp.icon;
              const isSelected = idx === selectedIdx;
              return (
                <button
                  key={bp.id}
                  role="tab"
                  type="button"
                  aria-selected={isSelected}
                  onClick={() => {
                    setSelectedIdx(idx);
                    setCopied(false);
                  }}
                  className={`text-left p-3 border-2 rounded-none transition-transform duration-150 focus:outline-none flex flex-col justify-between ${
                    isSelected
                      ? "bg-[#FAF8F5] text-[#0D0D11] border-black shadow-[4px_4px_0px_#B91C1C] -translate-y-0.5"
                      : "bg-[#101116] text-zinc-300 border-zinc-800 hover:bg-[#FAF8F5] hover:text-[#0D0D11] hover:border-black shadow-[3px_3px_0px_#000000]"
                  }`}
                >
                  <div className="flex items-center justify-between gap-1 w-full mb-2">
                    <span
                      className={`font-mono text-[11px] uppercase tracking-widest font-bold px-1.5 py-0.5 border border-black ${
                        isSelected
                          ? "bg-[#B91C1C] text-white"
                          : "bg-black text-zinc-300"
                      }`}
                    >
                      {bp.id}
                    </span>
                    <Icon
                      className={`w-3.5 h-3.5 stroke-[2.5] shrink-0 ${
                        isSelected ? "text-[#B91C1C]" : "text-zinc-400"
                      }`}
                    />
                  </div>
                  <div className="font-bold text-xs uppercase tracking-tight leading-snug">
                    {bp.shortTitle}
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Main Active Blueprint Plate (#FAF8F5 Paper Plate Contrast) */}
        <div className="bg-[#FAF8F5] text-[#0D0D11] border-2 border-black shadow-[4px_4px_0px_#B91C1C] rounded-none">
          {/* Plate Title Bar */}
          <div className="bg-black text-[#FAF8F5] px-5 py-4 border-b-2 border-black flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div className="flex items-start md:items-center gap-3">
              <div className="bg-[#B91C1C] text-white p-2 border-2 border-black shrink-0">
                <ActiveIcon className="w-5 h-5 stroke-[2.5]" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs uppercase tracking-widest text-[#DC2626] font-bold">
                    {active.id} // ARCHITECTURAL SPECIFICATION
                  </span>
                </div>
                <h3 className="text-xl md:text-2xl font-black uppercase tracking-tight text-[#FAF8F5]">
                  {active.title}
                </h3>
                <p className="font-mono text-xs uppercase tracking-widest text-zinc-400 mt-0.5">
                  {active.subtitle}
                </p>
              </div>
            </div>

            <div className="inline-flex items-center gap-1.5 bg-[#101116] border border-zinc-700 px-3 py-1.5 self-start md:self-center">
              <Lock className="w-3.5 h-3.5 text-[#DC2626]" />
              <span className="font-mono text-xs uppercase tracking-widest text-zinc-200 font-bold">
                INVARIANT LOCKED
              </span>
            </div>
          </div>

          <div className="p-5 md:p-6 space-y-6">
            {/* 1) Three-Tier Node Hierarchy (Coordinator -> Subagent Leader -> Execution Engine) */}
            <div className="space-y-2.5">
              <div className="flex items-center justify-between border-b-2 border-black pb-1.5">
                <span className="font-mono text-xs uppercase tracking-widest font-bold text-black">
                  01 // THREE-TIER COMMAND & EXECUTION HIERARCHY
                </span>
                <span className="font-mono text-xs uppercase tracking-widest text-[#B91C1C] font-bold">
                  STRICT UNIDIRECTIONAL DISPATCH
                </span>
              </div>

              <div className="flex flex-col lg:flex-row items-stretch justify-between gap-3 pt-1">
                {/* Tier 1: Coordinator Node */}
                <div className="flex-1 bg-white border-2 border-black p-4 shadow-[4px_4px_0px_#000000] flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <span className="font-mono text-xs uppercase tracking-widest font-bold bg-black text-[#FAF8F5] px-2 py-0.5">
                        TIER 01 // COORDINATOR NODE
                      </span>
                      <span className="font-mono text-xs font-bold text-[#B91C1C]">
                        {active.hierarchy.coordinator.latency}
                      </span>
                    </div>
                    <div className="font-mono text-sm md:text-base font-black text-black break-all">
                      {active.hierarchy.coordinator.name}
                    </div>
                  </div>
                  <p className="text-xs font-semibold text-zinc-700 mt-2 pt-2 border-t border-zinc-300">
                    {active.hierarchy.coordinator.role}
                  </p>
                </div>

                {/* Connector Arrow */}
                <div className="flex lg:flex-col items-center justify-center py-1 lg:py-0 lg:px-1">
                  <div className="bg-black text-[#FAF8F5] p-1.5 border-2 border-black shadow-[2px_2px_0px_#B91C1C]">
                    <ArrowRight className="w-4 h-4 stroke-[2.5] rotate-90 lg:rotate-0" />
                  </div>
                </div>

                {/* Tier 2: Subagent Leader */}
                <div className="flex-1 bg-white border-2 border-black p-4 shadow-[4px_4px_0px_#000000] flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <span className="font-mono text-xs uppercase tracking-widest font-bold bg-[#B91C1C] text-white px-2 py-0.5 border border-black">
                        TIER 02 // SUBAGENT LEADER
                      </span>
                      <span className="font-mono text-xs font-bold text-[#B91C1C]">
                        {active.hierarchy.leader.latency}
                      </span>
                    </div>
                    <div className="font-mono text-sm md:text-base font-black text-black break-all">
                      {active.hierarchy.leader.name}
                    </div>
                  </div>
                  <p className="text-xs font-semibold text-zinc-700 mt-2 pt-2 border-t border-zinc-300">
                    {active.hierarchy.leader.role}
                  </p>
                </div>

                {/* Connector Arrow */}
                <div className="flex lg:flex-col items-center justify-center py-1 lg:py-0 lg:px-1">
                  <div className="bg-black text-[#FAF8F5] p-1.5 border-2 border-black shadow-[2px_2px_0px_#B91C1C]">
                    <ArrowRight className="w-4 h-4 stroke-[2.5] rotate-90 lg:rotate-0" />
                  </div>
                </div>

                {/* Tier 3: Execution Engine */}
                <div className="flex-1 bg-[#070709] text-[#FAF8F5] border-2 border-black p-4 shadow-[4px_4px_0px_#B91C1C] flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <span className="font-mono text-xs uppercase tracking-widest font-bold bg-[#FAF8F5] text-black px-2 py-0.5 border border-black">
                        TIER 03 // EXECUTION ENGINE
                      </span>
                      <span className="font-mono text-xs font-bold text-[#DC2626]">
                        {active.hierarchy.engine.latency}
                      </span>
                    </div>
                    <div className="font-mono text-sm md:text-base font-black text-[#FAF8F5] break-all">
                      {active.hierarchy.engine.name}
                    </div>
                  </div>
                  <p className="text-xs font-semibold text-zinc-300 mt-2 pt-2 border-t border-zinc-800">
                    {active.hierarchy.engine.role}
                  </p>
                </div>
              </div>
            </div>

            {/* Middle Split: 2) Interactive Code/Terminal Preview & 3) Four Key Telemetry Metrics */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
              {/* 2) Interactive Code / Terminal Preview */}
              <div className="lg:col-span-7 flex flex-col border-2 border-black bg-[#070709] text-zinc-100 shadow-[4px_4px_0px_#000000]">
                <div className="bg-[#101116] border-b-2 border-black px-4 py-2.5 flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className="w-2.5 h-2.5 bg-[#DC2626] border border-black inline-block" />
                    <span className="font-mono text-xs uppercase tracking-widest font-bold text-[#FAF8F5]">
                      02 // {active.codeTitle}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-[11px] uppercase tracking-widest text-zinc-400 px-2 py-0.5 bg-black border border-zinc-800">
                      {active.codeLang}
                    </span>
                    <button
                      type="button"
                      onClick={handleCopyCode}
                      className="inline-flex items-center gap-1.5 font-mono text-xs uppercase tracking-widest font-bold px-2.5 py-1 bg-[#FAF8F5] text-black border border-black hover:bg-[#B91C1C] hover:text-white transition-colors"
                    >
                      {copied ? (
                        <>
                          <Check className="w-3.5 h-3.5 stroke-[2.5]" />
                          COPIED
                        </>
                      ) : (
                        <>
                          <Copy className="w-3.5 h-3.5 stroke-[2.5]" />
                          COPY SPEC
                        </>
                      )}
                    </button>
                  </div>
                </div>

                <div className="p-4 overflow-x-auto flex-1 flex items-center">
                  <pre className="font-mono text-xs md:text-[13px] leading-relaxed w-full">
                    {active.codeContent.split("\n").map((line, i) => {
                      const isComment =
                        line.trim().startsWith("#") ||
                        line.trim().startsWith("--") ||
                        line.trim().startsWith("//");
                      const isCommand =
                        line.trim().startsWith("$") ||
                        line.trim().startsWith("[STAGE") ||
                        line.trim().startsWith("VERDICT:") ||
                        line.trim().startsWith("[OK]");

                      return (
                        <div key={i} className="table-row">
                          <span className="table-cell pr-4 select-none text-zinc-600 text-right w-7">
                            {String(i + 1).padStart(2, "0")}
                          </span>
                          <span
                            className={`table-cell whitespace-pre ${
                              isComment
                                ? "text-zinc-400 italic"
                                : isCommand
                                ? "text-[#DC2626] font-bold"
                                : "text-[#FAF8F5]"
                            }`}
                          >
                            {line}
                          </span>
                        </div>
                      );
                    })}
                  </pre>
                </div>
              </div>

              {/* 3) Four Key Telemetry Metrics */}
              <div className="lg:col-span-5 flex flex-col justify-between space-y-2.5">
                <div className="flex items-center justify-between border-b-2 border-black pb-1.5">
                  <span className="font-mono text-xs uppercase tracking-widest font-bold text-black">
                    03 // LIVE TELEMETRY BENCHMARKS
                  </span>
                  <span className="font-mono text-xs uppercase tracking-widest text-[#B91C1C] font-bold">
                    4 KEY METRICS
                  </span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 flex-1">
                  {active.metrics.map((m, mIdx) => (
                    <div
                      key={m.label}
                      className={`border-2 border-black p-3.5 flex flex-col justify-between ${
                        mIdx === 0
                          ? "bg-white shadow-[4px_4px_0px_#B91C1C]"
                          : "bg-white shadow-[4px_4px_0px_#000000]"
                      }`}
                    >
                      <div className="flex items-center justify-between gap-1 border-b border-zinc-300 pb-1.5">
                        <span className="font-mono text-[11px] uppercase tracking-widest font-bold text-zinc-700">
                          {m.label}
                        </span>
                        <span
                          className={`w-2 h-2 border border-black ${
                            mIdx === 0 ? "bg-[#B91C1C]" : "bg-black"
                          }`}
                        />
                      </div>

                      <div
                        className={`font-mono text-2xl md:text-3xl font-black tracking-tight my-1.5 ${
                          mIdx === 0 ? "text-[#B91C1C]" : "text-[#0D0D11]"
                        }`}
                      >
                        {m.value}
                      </div>

                      <div className="font-mono text-[11px] uppercase tracking-widest font-bold text-zinc-600 bg-zinc-100 px-2 py-0.5 border border-black self-start">
                        {m.sub}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* 4) Four Verifiable Mathematical System Invariants */}
            <div className="border-2 border-black bg-white shadow-[4px_4px_0px_#000000]">
              <div className="bg-black text-[#FAF8F5] px-4 py-2.5 border-b-2 border-black flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 bg-[#DC2626] inline-block" />
                  <span className="font-mono text-xs uppercase tracking-widest font-bold">
                    04 // FOUR VERIFIABLE MATHEMATICAL SYSTEM INVARIANTS (
                    {active.id})
                  </span>
                </div>
                <span className="font-mono text-xs uppercase tracking-widest text-zinc-400">
                  FORMAL SMT PROOF GATE: ENFORCED
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 divide-y-2 md:divide-y-0 md:divide-x-2 divide-black">
                {active.invariants.map((inv, idx) => (
                  <div
                    key={inv.id}
                    className={`p-4 flex flex-col justify-between gap-2 ${
                      idx >= 2 ? "md:border-t-2 md:border-black" : ""
                    }`}
                  >
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <span className="font-mono text-xs uppercase tracking-widest font-bold px-2 py-0.5 bg-black text-[#FAF8F5] border border-black">
                        {inv.id}
                      </span>
                      <code className="font-mono text-xs md:text-sm font-bold text-[#B91C1C] bg-[#FAF8F5] px-2.5 py-0.5 border border-black break-all">
                        {inv.formula}
                      </code>
                    </div>
                    <p className="text-xs md:text-sm font-semibold text-zinc-800 leading-snug mt-1">
                      {inv.desc}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Feature06BlueprintCards;
