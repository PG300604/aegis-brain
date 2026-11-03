# Security Policy 🛡️

AegisBrain takes security, privacy, and memory isolation seriously.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

---

## 🔒 Private Stealth Mode

AegisBrain includes a native `private` mode designed to guarantee zero disk logging:
- When private mode is active (`aegis mode private`), sessions, decisions, and tracked PRs are strictly excluded from SQLite writes and FTS5 indexing.
- No tokens, code snippets, or user queries are written to disk while in private mode.

---

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability within AegisBrain, please do **NOT** open a public issue. Instead, report it privately to the maintainer via GitHub Security Advisories or email `priyanshughosh97@gmail.com`.

We will acknowledge receipt within 48 hours and work with you to patch and disclose the issue responsibly.
