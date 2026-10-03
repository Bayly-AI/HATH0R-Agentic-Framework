#!/usr/bin/env python3
"""Build script for Node.js hath0r-agentic-cli releases in ./release/javascript/node/cli."""

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
NODE_CLI_DIR = ROOT_DIR / "packages" / "node-cli"
RELEASE_NODE_DIR = ROOT_DIR / "release" / "javascript" / "node" / "cli"


def compute_sha256(filepath: Path) -> str:
    """Compute SHA256 hex digest of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def generate_checksums(release_dir: Path) -> Path:
    """Generate CHECKSUMS.sha256 for all artifacts in release_dir."""
    checksums_file = release_dir / "CHECKSUMS.sha256"
    lines = []

    for item in sorted(release_dir.iterdir()):
        if item.is_file() and item.name not in ("CHECKSUMS.sha256", ".DS_Store", ".gitkeep"):
            digest = compute_sha256(item)
            lines.append(f"{digest}  {item.name}")

    if lines:
        checksums_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return checksums_file


def clean_release_dir() -> None:
    print("[Hath0r Node Build] Cleaning release directory...")
    if RELEASE_NODE_DIR.exists():
        shutil.rmtree(RELEASE_NODE_DIR)
    RELEASE_NODE_DIR.mkdir(parents=True, exist_ok=True)


def build_node_package() -> None:
    print(f"[Hath0r Node Build] Copying hath0r-agentic-cli package to {RELEASE_NODE_DIR}...")
    for item in ["package.json", "README.md", "API_REFERENCE.md"]:
        if (NODE_CLI_DIR / item).exists():
            shutil.copy2(NODE_CLI_DIR / item, RELEASE_NODE_DIR / item)

    shutil.copytree(NODE_CLI_DIR / "src", RELEASE_NODE_DIR / "src", dirs_exist_ok=True)
    shutil.copytree(NODE_CLI_DIR / "test", RELEASE_NODE_DIR / "test", dirs_exist_ok=True)

    dist_dir = RELEASE_NODE_DIR / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(NODE_CLI_DIR / "src", dist_dir, dirs_exist_ok=True)

    rel_docs_dir = RELEASE_NODE_DIR / "docs"
    if (ROOT_DIR / "docs").exists():
        shutil.copytree(ROOT_DIR / "docs", rel_docs_dir, dirs_exist_ok=True)

    for doc_file in ["README.md", "README.TECHNICAL.md", "AGENTS.md", "LICENSE"]:
        if (ROOT_DIR / doc_file).exists():
            shutil.copy2(ROOT_DIR / doc_file, rel_docs_dir / doc_file)

    print("[Hath0r Node Build] Packing npm tarball...")
    subprocess.run(["npm", "pack"], cwd=RELEASE_NODE_DIR, check=True)


def run_node_tests() -> None:
    print("[Hath0r Node Build] Running Node plugin test suite in release directory...")
    cmd = ["node", "--experimental-strip-types", "--test", "test/*.test.ts"]
    subprocess.run(cmd, cwd=RELEASE_NODE_DIR, check=True)


def main() -> None:
    clean_release_dir()
    build_node_package()
    run_node_tests()
    chk = generate_checksums(RELEASE_NODE_DIR)

    print(f"\n[Hath0r Node Build Success] Artifacts created in {RELEASE_NODE_DIR}:")
    for f in sorted(RELEASE_NODE_DIR.rglob("*")):
        if f.is_file():
            size_kb = f.stat().st_size / 1024
            rel_name = f.relative_to(RELEASE_NODE_DIR)
            print(f"  - {rel_name} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
