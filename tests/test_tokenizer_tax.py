"""Tests for FinOps Tokenizer Tax Auditor and Multi-Lingual Cost Disparity Analyzer."""

import pytest
from pathlib import Path

from hath0r_engine.gateway.tokenizer_tax import (
    ScriptBreakdown,
    TaxAuditReport,
    TokenizerTaxAuditor,
    VocabVRAMFootprint,
)


class TestScriptIdentification:
    """Test Unicode script detection across diverse language families."""

    @pytest.mark.parametrize("char,expected_script", [
        ("a", "LATIN"),
        ("Z", "LATIN"),
        ("é", "LATIN"),
        ("д", "CYRILLIC"),
        ("Ω", "GREEK"),
        ("م", "ARABIC"),
        ("ش", "ARABIC"),
        ("ש", "HEBREW"),
        ("क", "DEVANAGARI"),
        ("ব", "BENGALI"),
        ("த", "TAMIL"),
        ("汉", "CJK"),
        ("字", "CJK"),
        ("あ", "HIRAGANA"),
        ("ア", "KATAKANA"),
        ("한", "HANGUL"),
        (" ", "CODE_OR_PUNCT"),
        ("{", "CODE_OR_PUNCT"),
        ("4", "CODE_OR_PUNCT"),
    ])
    def test_identify_script_families(self, char: str, expected_script: str):
        assert TokenizerTaxAuditor.identify_script(char) == expected_script


class TestVocabVRAMFootprint:
    """Mathematical verification of vocabulary matrix parameter and VRAM calculations."""

    def test_256k_vocab_vram_calculation(self):
        # 256k vocab * 4096 dim * 2 (input + output matrices) = ~2.097B parameters
        # In FP16 (2 bytes/param) = ~4.19 GB
        footprint = TokenizerTaxAuditor.calculate_vocab_vram_overhead(
            vocab_size=256000,
            hidden_dim=4096,
            precision_bytes=2,
        )
        assert footprint.parameters_count == 2 * 256000 * 4096
        assert footprint.parameters_count == 2_097_152_000
        assert 4.18 <= footprint.vram_gb <= 4.20
        assert footprint.to_dict()["vram_gb"] == footprint.vram_gb

    def test_128k_vocab_vram_calculation(self):
        # 128k vocab * 4096 dim * 2 = 1.048B parameters -> ~2.10 GB VRAM
        footprint = TokenizerTaxAuditor.calculate_vocab_vram_overhead(
            vocab_size=128000,
            hidden_dim=4096,
            precision_bytes=2,
        )
        assert footprint.parameters_count == 1_048_576_000
        assert 2.05 <= footprint.vram_gb <= 2.15


class TestVisualPatchBudget:
    """Test continuous visual patch budget calculation for rendered documents."""

    def test_single_page_patch_budget(self):
        # 1024x1024 page at 16x16 patch size = (64 * 64) = 4096 patches
        patches = TokenizerTaxAuditor.calculate_visual_patch_budget(
            text_length=1500,
            resolution=1024,
            patch_size=16,
        )
        assert patches == 4096

    def test_multi_page_patch_budget(self):
        # 10,000 chars exceeds 4000 chars/page -> 3 pages -> 3 * 4096 = 12288 patches
        patches = TokenizerTaxAuditor.calculate_visual_patch_budget(
            text_length=10000,
            chars_per_line=80,
            lines_per_page=50,
            resolution=1024,
            patch_size=16,
        )
        assert patches == 12288


class TestTokenizerTaxAuditor:
    """Test comprehensive text auditing and inflation metrics."""

    def test_latin_baseline_inflation(self):
        english_text = "The quick brown fox jumps over the lazy dog in modern enterprise software architecture."
        report = TokenizerTaxAuditor.audit_text(english_text)

        assert isinstance(report, TaxAuditReport)
        assert report.primary_script == "LATIN"
        # Pure Latin should have an inflation factor very close to 1.0 (within punctuation variance)
        assert 0.9 <= report.token_inflation_factor <= 1.5
        assert report.total_estimated_tokens > 0

    def test_arabic_token_inflation(self):
        # Arabic script has much lower character density per token (~1.1 chars/token vs 4.0 for Latin)
        arabic_text = "تعتبر محولات الرؤية الموحدة خطوة استراتيجية لخفض تكاليف الذكاء الاصطناعي في المؤسسات العالمية"
        report = TokenizerTaxAuditor.audit_text(arabic_text)

        assert report.primary_script == "ARABIC"
        # Arabic inflation should be between 2.5x and 4.0x relative to Latin baseline
        assert report.token_inflation_factor >= 2.5
        assert report.total_estimated_tokens > report.baseline_latin_tokens

        # Check FinOps pricing report
        standard_cost = report.cost_comparison["standard"]
        assert standard_cost["tokenizer_tax_usd"] > 0.0
        assert standard_cost["tax_percentage"] > 150.0

    def test_devanagari_token_inflation(self):
        hindi_text = "एंटरप्राइज एआई में टोकनाइज़र टैक्स को समाप्त करने के लिए विज़न ट्रांसफार्मर एक नया दृष्टिकोण प्रदान करते हैं।"
        report = TokenizerTaxAuditor.audit_text(hindi_text)

        assert report.primary_script == "DEVANAGARI"
        # Indic scripts suffer ~3.5x to 5.0x token expansion
        assert report.token_inflation_factor >= 3.0

    def test_cjk_token_inflation(self):
        chinese_text = "统一视觉转换器为企业级人工智能提供了一种消除分词器税并降低多语言成本的全新路径。"
        report = TokenizerTaxAuditor.audit_text(chinese_text)

        assert report.primary_script == "CJK"
        assert report.token_inflation_factor >= 1.8

    def test_empty_payload_safe(self):
        report = TokenizerTaxAuditor.audit_text("")
        assert report.raw_text_length == 0
        assert report.total_estimated_tokens == 0
        assert report.token_inflation_factor == 1.0

    def test_compare_payloads(self):
        en = "Unified Vision Transformers lower enterprise AI costs and simplify multimodal workflows."
        ar = "محولات الرؤية الموحدة تخفض تكاليف الذكاء الاصطناعي للمؤسسات وتبسط مهام العمل متعددة الوسائط."
        comparison = TokenizerTaxAuditor.compare_payloads(en, ar)

        assert comparison["source_script"] == "LATIN"
        assert comparison["target_script"] == "ARABIC"
        assert comparison["expansion_ratio"] > 1.5
        assert comparison["is_taxed"] is True

    def test_audit_file(self, tmp_path: Path):
        test_file = tmp_path / "sample_doc.txt"
        test_file.write_text("Enterprise AI architecture benchmark test payload.", encoding="utf-8")

        report = TokenizerTaxAuditor.audit_file(test_file)
        assert report.raw_text_length == len("Enterprise AI architecture benchmark test payload.")
        assert report.primary_script == "LATIN"

    def test_audit_nonexistent_file_raises(self):
        with pytest.raises(FileNotFoundError):
            TokenizerTaxAuditor.audit_file("nonexistent_path_404.txt")
