#!/usr/bin/env python3
"""Build, package, and generate checksums for the @hath0r/node release package."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
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


def rotate_previous_release(
    release_dir: Path,
    previous_dir: Path,
    current_version: str,
    dry_run: bool = False,
) -> Path | None:
    """Rotate existing active release artifacts into previous/<version>/ archive."""
    release_dir.mkdir(parents=True, exist_ok=True)
    previous_dir.mkdir(parents=True, exist_ok=True)

    artifacts = [
        item for item in release_dir.iterdir()
        if item.is_file() and item.name.endswith(".tgz")
    ]
    if not artifacts:
        return None

    archive_target = previous_dir / f"{current_version}-prev"
    print(f"Rotating existing Node release artifacts into archive: {archive_target}")

    if not dry_run:
        archive_target.mkdir(parents=True, exist_ok=True)
        for art in artifacts:
            target_file = archive_target / art.name
            shutil.move(str(art), str(target_file))
        generate_checksums(archive_target)

    return archive_target


def main() -> None:
    parser = argparse.ArgumentParser(description="Hath0r Node release package builder")
    parser.add_argument("--out-dir", default="release/javascript/node", help="Output directory for Node package")
    parser.add_argument("--previous-dir", default=None, help="Directory for previous version archives")
    parser.add_argument("--rotate", action="store_true", help="Rotate existing release files to previous archive")
    parser.add_argument("--checksums-only", action="store_true", help="Regenerate CHECKSUMS.sha256 only")
    parser.add_argument("--dry-run", action="store_true", help="Simulate build without modifying files")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    release_dir = (repo_root / args.out_dir).resolve() if not Path(args.out_dir).is_absolute() else Path(args.out_dir)
    release_dir.mkdir(parents=True, exist_ok=True)
    
    prev_dir = Path(args.previous_dir).resolve() if args.previous_dir else (release_dir / "previous")
    prev_dir.mkdir(parents=True, exist_ok=True)

    ver_file = repo_root / "VERSION"
    ver = ver_file.read_text(encoding="utf-8").strip() if ver_file.is_file() else "0.3.0"

    if args.rotate:
        rotate_previous_release(release_dir, prev_dir, ver, dry_run=args.dry_run)

    if args.checksums_only:
        chk = generate_checksums(release_dir)
        print(f"Updated checksums at {chk}")
        return

    print(f"Building @hath0r/node package in {release_dir}...")
    if not args.dry_run:
        subprocess.run(["node", "scripts/build.mjs"], cwd=release_dir, check=True)
        subprocess.run(["npm", "pack"], cwd=release_dir, check=True)
        subprocess.run(["node", "--test", "tests/index.test.js"], cwd=release_dir, check=True)

    chk = generate_checksums(release_dir)
    print(f"Node release build complete. Checksums generated at {chk}")


if __name__ == "__main__":
    main()
