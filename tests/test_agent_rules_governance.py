"""Unit tests verifying Agent Rules, Governance Subsystem files, and RAG/CLI specifications."""

from pathlib import Path
import pytest


def test_root_agents_md_governance():
    repo_root = Path(__file__).resolve().parent.parent
    agents_file = repo_root / "AGENTS.md"
    assert agents_file.exists(), "Root AGENTS.md must exist"

    content = agents_file.read_text(encoding="utf-8")
    assert "CR-CLI-ENTRY-001" in content
    assert "CR-RAG-RETRIEVAL-001" in content
    assert "CR-SUBSTRATE-001" in content
    assert "hath0r" in content
    assert "src/hath0r_engine/AGENTS.md" in content


def test_subsystem_agents_md_files():
    repo_root = Path(__file__).resolve().parent.parent
    expected_subsystems = [
        repo_root / "src/hath0r_engine/AGENTS.md",
        repo_root / "docs/AGENTS.md",
        repo_root / "contracts/AGENTS.md",
        repo_root / "tests/AGENTS.md",
        repo_root / "cfg/AGENTS.md",
        repo_root / "lib/AGENTS.md",
        repo_root / "archive/AGENTS.md",
    ]

    for sub_agents in expected_subsystems:
        assert sub_agents.exists(), f"Subsystem AGENTS.md missing at {sub_agents}"
        text = sub_agents.read_text(encoding="utf-8")
        assert "CR-CLI-ENTRY-001" in text
        assert "CR-RAG-RETRIEVAL-001" in text or "cr-branch-gov-001" in text


def test_governance_strategy_and_playbook_existence():
    repo_root = Path(__file__).resolve().parent.parent
    strategy = repo_root / "docs/governance/strategies/agent-rules-rag-cli-first-strategy.md"
    playbook = repo_root / "docs/governance/playbooks/agent-rules-rag-cli-first-playbook.md"

    assert strategy.exists(), "Strategy file missing"
    assert playbook.exists(), "Playbook file missing"

    strat_text = strategy.read_text(encoding="utf-8")
    assert "Tri-Graph Hybrid RAG Retrieval" in strat_text

    playbook_text = playbook.read_text(encoding="utf-8")
    assert "hath0r memory search" in playbook_text
