#!/usr/bin/env python3
"""Build, package, and generate checksums for both Node CLI and Node Plugin release packages."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Hath0r Node release package builder")
    parser.add_argument("--cli-only", action="store_true", help="Build hath0r-agentic-cli only")
    parser.add_argument("--plugin-only", action="store_true", help="Build hath0r-cli-node-plugin only")
    args = parser.parse_args()

    if not args.plugin_only:
        print("\n=== Building hath0r-agentic-cli (Node CLI) ===")
        subprocess.run([sys.executable, str(ROOT_DIR / "scripts" / "build_node_cli.py")], check=True)

    if not args.cli_only:
        print("\n=== Building hath0r-cli-node-plugin (Node Plugin) ===")
        subprocess.run([sys.executable, str(ROOT_DIR / "scripts" / "build_node_plugin.py")], check=True)

    print("\n[Hath0r Node Build Complete] All Node packages built and verified successfully.")


if __name__ == "__main__":
    main()
