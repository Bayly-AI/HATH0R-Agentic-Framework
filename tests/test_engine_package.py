"""Unit and contract tests for hath0r_engine package distribution and exports."""



def test_hath0r_engine_top_level_exports():
    """Verify top-level package exposes all cognitive substrate and safety classes."""
    import hath0r_engine

    assert hath0r_engine.__version__ == "1.0.0"
    assert hasattr(hath0r_engine, "KnowledgeGraph")
    assert hasattr(hath0r_engine, "KnowledgeNode")
    assert hasattr(hath0r_engine, "KnowledgeEdge")
    assert hasattr(hath0r_engine, "KnowledgeGraphExtractor")
    assert hasattr(hath0r_engine, "ContextGraph")
    assert hasattr(hath0r_engine, "ContextNode")
    assert hasattr(hath0r_engine, "ContextEdge")
    assert hasattr(hath0r_engine, "MemoryGraph")
    assert hasattr(hath0r_engine, "MemoryNode")
    assert hasattr(hath0r_engine, "MemoryEdge")
    assert hasattr(hath0r_engine, "JevClient")
    assert hasattr(hath0r_engine, "JevToolGuard") or hasattr(hath0r_engine, "is_guarded_tool")
    assert hasattr(hath0r_engine, "VoiceEngine")
    assert hasattr(hath0r_engine, "VoiceConfig")


def test_hath0r_engine_submodule_imports():
    """Verify clean importing from submodules."""
    from hath0r_engine.context import ContextGraph
    from hath0r_engine.graph import KnowledgeGraph
    from hath0r_engine.memory import MemoryGraph

    kg = KnowledgeGraph()
    assert kg.schema_version.startswith("hath0r.knowledgegraph")

    cg = ContextGraph()
    assert cg.schema_version.startswith("hath0r.contextgraph")

    mg = MemoryGraph(graph_id="test-engine-mem")
    assert mg.graph_id == "test-engine-mem"


def test_backward_compatibility_lib_imports():
    """Verify legacy lib.* import paths still function seamlessly."""
    from lib.context.context_graph import ContextGraph
    from lib.graph.knowledge_graph import KnowledgeGraph
    from lib.jev.jev_client import JevClient
    from lib.memory.memory_graph import MemoryGraph
    from lib.voice.voice_engine import VoiceEngine

    assert KnowledgeGraph is not None
    assert ContextGraph is not None
    assert MemoryGraph is not None
    assert JevClient is not None
    assert VoiceEngine is not None
