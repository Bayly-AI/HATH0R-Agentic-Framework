"""Tests for standalone binary release matrix and packaging automation."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

# Import build helper from scripts
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build_binaries  # type: ignore # noqa: E402


def test_checksum_computation(tmp_path: Path) -> None:
    test_file = tmp_path / "test_bin"
    test_file.write_bytes(b"hello hath0r binary")
    digest = build_binaries.compute_sha256(test_file)
    assert len(digest) == 64

    # Test checksum file generation
    chk_file = build_binaries.generate_checksums(tmp_path)
    assert chk_file.is_file()
    content = chk_file.read_text(encoding="utf-8")
    assert f"{digest}  test_bin" in content


def test_target_binary_name_resolution() -> None:
    name = build_binaries.get_target_binary_name()
    assert "hath0r-" in name


def test_release_workflow_yaml_validity() -> None:
    wf_path = Path(__file__).resolve().parent.parent / ".github" / "workflows" / "release-binaries.yml"
    assert wf_path.is_file()

    data = yaml.safe_load(wf_path.read_text(encoding="utf-8"))
    assert data["name"] == "Build and Release Standalone Binaries"

    jobs = data.get("jobs", {})
    assert "build-binaries" in jobs
    assert "package-and-publish" in jobs

    matrix = jobs["build-binaries"]["strategy"]["matrix"]["include"]
    os_list = [m["os"] for m in matrix]
    assert "macos-14" in os_list
    assert "macos-13" in os_list
    assert "ubuntu-latest" in os_list
    assert "windows-latest" in os_list
