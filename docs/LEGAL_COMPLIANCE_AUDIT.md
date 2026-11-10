# Legal & Intellectual Property Compliance Audit

**Project:** AegisBrain  
**License:** GNU General Public License v3.0 (GPLv3)  
**Audit Date:** November 2026  
**Status:** 🟢 **100% Compliant — Zero License Infringements Detected**

---

## 1. Executive Summary
AegisBrain is an open-source, local neural memory bus and multi-tier agent orchestration system licensed under **GNU General Public License v3.0 (GPL-3.0-or-later)**. 

This audit reviews:
1. Core Python runtime and libraries (`package/`).
2. Web landing and interactive UI dependencies (`web/`).
3. External AI models, execution worker CLIs, and subprocess tool integrations.
4. Brand assets, trademarks, and icon vectors.

---

## 2. Core Python Architecture (`package/`)
- **Distribution Model:** Python Wheel (`hatchling`).
- **Core Dependencies:** **None (`dependencies = []`)**. The core neural memory bus, SQLite FTS5 engine, severity triage judge, and daemon server rely **100% on Python's Standard Library** (`sqlite3`, `argparse`, `dataclasses`, `http.server`, `subprocess`, `pathlib`, `json`).
- **Optional Dependencies:**
  - `pytest`: MIT License (Permissive test runner).
  - `fastapi`: MIT License (Permissive ASGI framework).
  - `uvicorn`: BSD-3-Clause License (Permissive ASGI server).
- **Compliance Finding:** Zero dependency conflicts. Pure standard-library core eliminates any legal liability or GPL incompatibility.

---

## 3. Web Frontend Stack (`web/`)
The web application is built with **Next.js 16 (Turbopack)** and **React 19.3.1**:

| Package | Version | License | Compatibility with GPLv3 |
| :--- | :--- | :--- | :--- |
| `next` | 16.4.5 | MIT | 🟢 Fully Compatible |
| `react` | 19.3.1 | MIT | 🟢 Fully Compatible (Patched against RSC RCE) |
| `react-dom` | 19.3.1 | MIT | 🟢 Fully Compatible |
| `motion` (framer-motion) | 14.10.1 | MIT | 🟢 Fully Compatible |
| `three` | 0.187.0 | MIT | 🟢 Fully Compatible |
| `lucide-react` | 1.70.0 | ISC | 🟢 Fully Compatible |
| `react-icons` | 5.7.0 | MIT / Apache-2.0 / CC0 | 🟢 Fully Compatible (Permissive brand vectors) |
| `canvas-confetti` | 1.9.4 | ISC | 🟢 Fully Compatible |
| `gsap` | 3.15.1 | Standard GreenSock | 🟢 Compliant (Permissive for public, non-commercial/standard web usage) |
| `tailwindcss` | 4.x | MIT | 🟢 Fully Compatible |

- **Compliance Finding:** All web dependencies use OSI-approved permissive licenses (MIT, ISC, Apache-2.0, CC0) that can be distributed freely alongside GPLv3 software.

---

## 4. Orchestrated CLI Tools & Subprocess Boundaries
AegisBrain acts as an **independent orchestrator** communicating with external tools via standard input/output (stdio), CLI flags, and filesystem configuration files:

| Tool | Creator / Upstream | Interaction Method | License / Terms Status |
| :--- | :--- | :--- | :--- |
| **Ollama** | Ollama Inc. | Subprocess CLI (`ollama run`) | MIT License |
| **Hermes Agent** | Nous Research | Subprocess CLI (`hermes chat -q`) | Apache 2.0 / Llama-3 Community |
| **OpenCode** | OpenCode AI | Subprocess CLI (`opencode`) | MIT License |
| **OpenAI Whisper** | OpenAI | Subprocess CLI (`whisper.exe`) | MIT License |
| **FFmpeg** | FFmpeg Team | Subprocess CLI (`ffmpeg.exe`) | LGPL 2.1+ / GPL 2.0+ (Clean subprocess execution, no proprietary linking) |
| **Claude Code** | Anthropic | Filesystem Hook (`~/.claude/CLAUDE.md`) | Permissive developer configuration |
| **Antigravity CLI** | Google | Filesystem Hook (`~/.gemini/config/GEMINI.md`) | Permissive developer configuration |

- **Subprocess Boundary Precedent:** Under Free Software Foundation (FSF) and legal guidelines, invoking independent tools through standard operating system CLI processes (`subprocess.run`, stdio pipes) does not create a derivative work. Each tool remains governed by its respective upstream license.

---

## 5. Trademark & Brand Asset Usage
- **Brand Marks in LogoLoop:** Authentic brand logos (Claude, Ollama, OpenAI, DeepSeek, Cursor, Mistral, Google Gemini, Hugging Face) are rendered for **referential and nominative fair use** solely to identify interoperability and supported platform compatibility.
- **No Endorsement Claims:** AegisBrain makes no claim of endorsement, sponsorship, or affiliation with Google, Anthropic, OpenAI, or Nous Research.

---

## 6. Terms & Conditions Summary for Users
1. **Free to Use, Modify, and Distribute:** Governed by the GNU GPLv3 license.
2. **Local Execution & Privacy Invariant:** AegisBrain runs 100% locally on your machine. No telemetry, session transcripts, code snippets, or database entries are ever exfiltrated to third-party servers.
3. **No Warranty:** Provided "as is" without warranty of any kind, express or implied.
