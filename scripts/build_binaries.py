#!/usr/bin/env python3
"""Build and bundle standalone binary releases and checksums for Hath0r."""

from __future__ import annotations

import argparse
import hashlib
import platform
import subprocess
import sys
from pathlib import Path


def compute_sha256(filepath: Path) -> str:
    """Compute SHA256 hex digest of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def get_target_binary_name() -> str:
    """Determine binary artifact name based on operating system and architecture."""
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == "darwin":
        arch = "arm64" if machine in ("arm64", "aarch64") else "x86_64"
        return f"hath0r-darwin-{arch}"
    elif system == "linux":
        arch = "arm64" if machine in ("arm64", "aarch64") else "x86_64"
        return f"hath0r-linux-{arch}"
    elif system == "windows":
        return "hath0r-windows-x64.exe"
    return f"hath0r-{system}-{machine}"


def generate_checksums(release_dir: Path) -> Path:
    """Generate CHECKSUMS.sha256 for all artifacts in release_dir."""
    checksums_file = release_dir / "CHECKSUMS.sha256"
    lines = []

    for item in sorted(release_dir.iterdir()):
        if item.is_file() and item.name not in ("CHECKSUMS.sha256", "README.md", ".DS_Store"):
            digest = compute_sha256(item)
            lines.append(f"{digest}  {item.name}")

    checksums_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return checksums_file


def build_standalone_binary(output_dir: Path, dry_run: bool = False) -> Path:
    """Build single-file executable using PyInstaller."""
    output_dir.mkdir(parents=True, exist_ok=True)
    binary_name = get_target_binary_name()
    target_path = output_dir / binary_name

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--onefile",
        "--name",
        binary_name,
        "--distpath",
        str(output_dir),
        "--hidden-import=click",
        "--hidden-import=rich",
        "--hidden-import=yaml",
        "--entry-point",
        "hath0r_cli.cli:main",
    ]

    print(f"Building standalone binary {binary_name} -> {target_path}...")
    if not dry_run:
        subprocess.run(cmd, check=True)
        target_path.chmod(0o755)

    return target_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Hath0r standalone release builder")
    parser.add_argument("--out-dir", default="release", help="Output directory for binaries")
    parser.add_argument("--checksums-only", action="store_true", help="Regenerate CHECKSUMS.sha256 only")
    parser.add_argument("--dry-run", action="store_true", help="Simulate build without executing PyInstaller")
    args = parser.parse_args()

    release_dir = Path(args.out_dir).resolve()
    release_dir.mkdir(parents=True, exist_ok=True)

    if args.checksums_only:
        chk = generate_checksums(release_dir)
        print(f"Updated checksums at {chk}")
        return

    binary = build_standalone_binary(release_dir, dry_run=args.dry_run)
    chk = generate_checksums(release_dir)
    print(f"Build complete. Binary: {binary}, Checksums: {chk}")


if __name__ == "__main__":
    main()
