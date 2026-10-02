#!/usr/bin/env python3
"""Build and bundle standalone binary releases and checksums for Hath0r."""

from __future__ import annotations

import argparse
import hashlib
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


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
        if item.is_file() and item.name not in ("CHECKSUMS.sha256", "README.md", ".DS_Store", ".gitkeep"):
            digest = compute_sha256(item)
            lines.append(f"{digest}  {item.name}")

    if lines:
        checksums_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return checksums_file


def rotate_previous_release(
    release_dir: Path,
    previous_dir: Path,
    current_version: str,
    dry_run: bool = False,
) -> Optional[Path]:
    """Rotate existing active release artifacts into previous/<version>/ archive."""
    release_dir.mkdir(parents=True, exist_ok=True)
    previous_dir.mkdir(parents=True, exist_ok=True)

    artifacts = [
        item for item in release_dir.iterdir()
        if item.is_file() and item.name not in ("README.md", ".DS_Store", ".gitkeep")
    ]
    if not artifacts:
        return None

    version_pattern = re.compile(r"[-_](\d+\.\d+\.\d+(?:[-.][0-9A-Za-z]+)?)\.(?:tar\.gz|whl)")
    prev_ver = None
    for f in artifacts:
        m = version_pattern.search(f.name)
        if m:
            prev_ver = m.group(1)
            break
    if not prev_ver or prev_ver == current_version:
        prev_ver = f"{current_version}-prev"

    archive_target = previous_dir / prev_ver
    print(f"Rotating existing release artifacts into archive: {archive_target}")

    if not dry_run:
        archive_target.mkdir(parents=True, exist_ok=True)
        for art in artifacts:
            target_file = archive_target / art.name
            shutil.move(str(art), str(target_file))
        generate_checksums(archive_target)

    return archive_target


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
    parser.add_argument("--previous-dir", default=None, help="Directory for previous version archives")
    parser.add_argument("--rotate", action="store_true", help="Rotate existing release files to previous archive")
    parser.add_argument("--checksums-only", action="store_true", help="Regenerate CHECKSUMS.sha256 only")
    parser.add_argument("--dry-run", action="store_true", help="Simulate build without executing PyInstaller")
    args = parser.parse_args()

    release_dir = Path(args.out_dir).resolve()
    release_dir.mkdir(parents=True, exist_ok=True)
    prev_dir = Path(args.previous_dir).resolve() if args.previous_dir else (release_dir / "previous")
    prev_dir.mkdir(parents=True, exist_ok=True)

    if args.rotate:
        ver_file = release_dir.parent / "VERSION"
        ver = ver_file.read_text(encoding="utf-8").strip() if ver_file.is_file() else "1.0.0"
        rotate_previous_release(release_dir, prev_dir, ver, dry_run=args.dry_run)

    if args.checksums_only:
        chk = generate_checksums(release_dir)
        print(f"Updated checksums at {chk}")
        if prev_dir.exists():
            for sub in prev_dir.iterdir():
                if sub.is_dir():
                    generate_checksums(sub)
        return

    binary = build_standalone_binary(release_dir, dry_run=args.dry_run)
    chk = generate_checksums(release_dir)
    print(f"Build complete. Binary: {binary}, Checksums: {chk}")


if __name__ == "__main__":
    main()
