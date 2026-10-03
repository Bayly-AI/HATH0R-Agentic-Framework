# Hath0r CLI Standalone Executable & Package Releases

This directory contains pre-compiled, zero-dependency standalone binaries, Python packages, and fileset archives of the **Hath0r CLI Operator** (`hath0r`).

The Hath0r CLI is the single, definitive tool required to initialize, govern, audit, and orchestrate autonomous AI multi-agent workflows across any repository or codebase.

---

## 📦 Available Release Artifacts

### Standalone Executable Binaries (Zero Dependencies)

| Platform | Architecture | Binary File |
| :--- | :--- | :--- |
| **macOS** | Apple Silicon (`arm64`) | [`release/python/cli/hath0r-darwin-arm64`](hath0r-darwin-arm64) |
| **macOS** | Intel (`x86_64`) | [`release/python/cli/hath0r-darwin-x86_64`](hath0r-darwin-x86_64) |
| **Linux** | ARM64 (`aarch64`) | [`release/python/cli/hath0r-linux-arm64`](hath0r-linux-arm64) |
| **Linux** | x86_64 (`amd64`) | [`release/python/cli/hath0r-linux-x86_64`](hath0r-linux-x86_64) |
| **Windows**| x64 | [`release/python/cli/hath0r-windows-x64.cmd`](hath0r-windows-x64.cmd) |

### Python Package & Fileset Distributions

| Distribution | Type | File |
| :--- | :--- | :--- |
| **Python Wheel** | Pip Wheel (`.whl`) | [`release/python/cli/hath0r_cli-0.3.0-py3-none-any.whl`](hath0r_cli-0.3.0-py3-none-any.whl) |
| **Source Tarball** | Source (`.tar.gz`) | [`release/python/cli/hath0r_cli-0.3.0.tar.gz`](hath0r_cli-0.3.0.tar.gz) |
| **Hath0r Fileset** | Member Template Archive | [`release/python/cli/hath0r-fileset-0.3.0.tar.gz`](hath0r-fileset-0.3.0.tar.gz) |

---

## 🚀 Quick Start (Zero Setup Required)

### 1. Verify and Make Executable (macOS / Linux)
```bash
chmod +x release/python/cli/hath0r-darwin-arm64   # macOS Apple Silicon
# or
chmod +x release/python/cli/hath0r-linux-x86_64   # Linux x86_64
```

### 2. Verify Health & Environment
```bash
./release/python/cli/hath0r-darwin-arm64 doctor
```

### 3. Initialize Any Repository with Hath0r
```bash
cd /path/to/target-project
/path/to/hath0r-framework/release/python/cli/hath0r-darwin-arm64 init
```

---

## 🔒 Verification & Checksums

Integrity checksums for all binary and package artifacts are recorded in [`release/python/cli/CHECKSUMS.sha256`](CHECKSUMS.sha256).

Verify with:
```bash
shasum -a 256 -c release/python/cli/CHECKSUMS.sha256
```

