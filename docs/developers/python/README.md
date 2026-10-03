# Python CLI & Engine Developer Guide

> **Canonical Release Directory:** `./release/python/cli`  
> **Package / Binary:** `hath0r_cli` / `hath0r`  

This document provides complete developer documentation for the Python CLI and `hath0r_engine` distribution.

---

## 1. Installation & Distribution

### Standalone Executable Binaries
Standalone single-file executables compiled with PyInstaller are published in `./release/python/cli`:

- 🍏 **macOS (Apple Silicon):** `release/python/cli/hath0r-darwin-arm64`
- 🍏 **macOS (Intel):** `release/python/cli/hath0r-darwin-x86_64`
- 🐧 **Linux (x86_64):** `release/python/cli/hath0r-linux-x86_64`
- 🐧 **Linux (ARM64):** `release/python/cli/hath0r-linux-arm64`
- 🪟 **Windows (x64):** `release/python/cli/hath0r-windows-x64.cmd`

### Python Wheel & PyPI Package
```sh
pip install release/python/cli/hath0r_cli-0.3.0-py3-none-any.whl
# or via pipx
pipx install hath0r-cli
```

---

## 2. CLI Command Tree

```text
hath0r
├── doctor          # Check paths, control tower, member repos, and KB
├── init            # Initialize enterprise governance in any repo
├── preflight       # Pre-PR quality gates check
├── quality         # Comprehensive quality gate aggregator
├── agentgraph      # Query unified quad-graph substrate & route role RBAC
├── memory          # Local memory space search & paging
├── finops          # Tokenizer tax auditor & cost telemetry
└── release         # Version + release notes + GitHub tag/release bot
```

---

## 3. Building & Packaging

To rebuild standalone Python CLI binaries and generate checksums:

```sh
python3 scripts/build_binaries.py --out-dir release/python/cli --rotate
```

Verify SHA256 integrity:

```sh
shasum -a 256 -c release/python/cli/CHECKSUMS.sha256
```
