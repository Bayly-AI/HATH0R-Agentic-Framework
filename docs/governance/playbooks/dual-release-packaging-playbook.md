# Dual-Language Release & Packaging Playbook

> **Rule:** CR-CLI-ENTRY-001 (Docs before code)  
> **Target Release Directory Structure:**  
> - Python CLI: `./release/python/cli`  
> - Node/JS Package: `./release/javascript/node`  
> **Updated:** October 2026  

---

## 1. Objective & Scope

This playbook defines the canonical release operational procedures for building, packaging, testing, and publishing both the **Python CLI** (`./release/python/cli`) and **Node/JS Package** (`./release/javascript/node`) within the Hath0r Agentic Framework.

---

## 2. Directory Layout & Artifact Taxonomy

```text
release/
├── python/
│   └── cli/
│       ├── CHECKSUMS.sha256
│       ├── README.md                          # Standalone Python CLI usage guide
│       ├── hath0r-darwin-arm64               # Standalone PyInstaller binaries
│       ├── hath0r-darwin-x86_64
│       ├── hath0r-linux-arm64
│       ├── hath0r-linux-x86_64
│       ├── hath0r-windows-x64.cmd
│       ├── hath0r_cli-*.whl                   # Python Wheel
│       ├── hath0r_cli-*.tar.gz                # Source tarball
│       └── previous/                          # Previous release archives
└── javascript/
    └── node/
        ├── CHECKSUMS.sha256
        ├── README.md                          # Node/JS plugin & SDK guide
        ├── package.json                       # Package manifest
        ├── hath0r-node-*.tgz                  # Packaged NPM tarball
        ├── dist/                              # Compiled JS & TypeScript definitions
        │   ├── index.js
        │   ├── index.mjs
        │   └── index.d.ts
        └── previous/                          # Previous release archives
```

---

## 3. Operational Steps

### Step 1: Pre-Release Validation
Before initiating a release build, verify SemVer alignment and quality gates:
```sh
hath0r release validate
hath0r quality
```

### Step 2: Build Release Artifacts
Build binaries and packages for both Python CLI and Node/JS:
```sh
# Build Python standalone binaries & wheels
python3 scripts/build_binaries.py --out-dir release/python/cli --rotate

# Build Node package & TypeScript bundles
python3 scripts/build_node_release.py --out-dir release/javascript/node --rotate
```

### Step 3: Run Testing Suites
Execute test suites across both ecosystems:
```sh
# Python test suite
pytest tests/

# Node/JS test suite with coverage
npm --prefix release/javascript/node test
npm --prefix release/javascript/node run test:coverage
```

### Step 4: Verify Integrity Checksums
Ensure `CHECKSUMS.sha256` files are correctly generated in both release directories:
```sh
shasum -a 256 -c release/python/cli/CHECKSUMS.sha256
shasum -a 256 -c release/javascript/node/CHECKSUMS.sha256
```

---

## 4. CI/CD Integration & Promotion Path

Per **CR-BAI-001**, release branches (`release/x.x.x`) promote strictly along:
`local → development → testing → staging → master (Production)`

The `.github/workflows/release-binaries.yml` workflow automatically builds both `./release/python/cli` and `./release/javascript/node` artifacts and attaches them to official GitHub releases upon tag creation.
