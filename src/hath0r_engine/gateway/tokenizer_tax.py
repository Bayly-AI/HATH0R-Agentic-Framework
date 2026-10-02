"""FinOps Tokenizer Tax Auditor and Multi-Lingual Cost Disparity Analyzer.

Calculates subword token expansion ratios (BPE/WordPiece) across languages and
structured 2D formats, models vocabulary VRAM parameter overhead, and compares
inference costs against continuous visual patch budgets.
Zero external runtime dependencies (pure Python standard library).
"""

from __future__ import annotations

import math
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List

# Standard subword tokenization density: characters per token by script family
SCRIPT_CHARS_PER_TOKEN: Dict[str, float] = {
    "LATIN": 4.0,       # English, French, Spanish, German, etc.
    "CYRILLIC": 1.8,    # Russian, Ukrainian, Bulgarian, etc.
    "GREEK": 1.9,       # Greek
    "ARABIC": 1.1,      # Arabic, Persian, Urdu
    "HEBREW": 1.2,      # Hebrew
    "DEVANAGARI": 0.8,  # Hindi, Sanskrit, Marathi
    "BENGALI": 0.85,    # Bengali
    "TAMIL": 0.75,      # Tamil
    "CJK": 1.5,         # Chinese, Japanese Kanji, Korean Hanja
    "HIRAGANA": 1.3,    # Japanese Hiragana
    "KATAKANA": 1.3,    # Japanese Katakana
    "HANGUL": 1.4,      # Korean Hangul
    "CODE_OR_PUNCT": 2.5, # Source code syntax, punctuation, whitespace
    "OTHER": 2.0,       # Fallback
}

# Industry pricing benchmarks (USD per 1M input tokens)
PROVIDER_PRICING_PER_M_TOKENS: Dict[str, Dict[str, float]] = {
    "light": {"input": 0.15, "output": 0.60},        # e.g., GPT-4o-mini / Claude 3.5 Haiku
    "standard": {"input": 3.00, "output": 15.00},    # e.g., Claude 3.5 Sonnet / GPT-4o
    "reasoning": {"input": 15.00, "output": 60.00},  # e.g., OpenAI o3 / Claude Opus
}


@dataclass
class ScriptBreakdown:
    """Script-level character distribution and token inflation."""

    script_name: str
    char_count: int
    percentage: float
    estimated_tokens: int
    expansion_factor: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class VocabVRAMFootprint:
    """Memory overhead of vocabulary embedding matrices and unembedding heads."""

    vocab_size: int
    hidden_dim: int
    precision_bytes: int
    parameters_count: int
    vram_bytes: int
    vram_gb: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TaxAuditReport:
    """Comprehensive Tokenizer Tax audit report."""

    raw_text_length: int
    primary_script: str
    script_breakdowns: List[ScriptBreakdown]
    total_estimated_tokens: int
    baseline_latin_tokens: int
    token_inflation_factor: float
    equivalent_visual_patches: int
    vocab_vram_overhead: VocabVRAMFootprint
    cost_comparison: Dict[str, Dict[str, float]]
    summary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "raw_text_length": self.raw_text_length,
            "primary_script": self.primary_script,
            "script_breakdowns": [sb.to_dict() for sb in self.script_breakdowns],
            "total_estimated_tokens": self.total_estimated_tokens,
            "baseline_latin_tokens": self.baseline_latin_tokens,
            "token_inflation_factor": round(self.token_inflation_factor, 3),
            "equivalent_visual_patches": self.equivalent_visual_patches,
            "vocab_vram_overhead": self.vocab_vram_overhead.to_dict(),
            "cost_comparison": self.cost_comparison,
            "summary": self.summary,
        }


class TokenizerTaxAuditor:
    """Audits subword token expansion and financial premiums against continuous visual patch representations."""

    @staticmethod
    def identify_script(char: str) -> str:
        """Classify a Unicode character into its primary script family."""
        if char.isspace() or char in "{}[]():;.,'\"`~!@#$%^&*-_=+/\\|<>?0123456789":
            return "CODE_OR_PUNCT"

        code = ord(char)
        if 0x0000 <= code <= 0x024F or 0x1E00 <= code <= 0x1EFF:
            return "LATIN"
        if 0x0400 <= code <= 0x04FF or 0x0500 <= code <= 0x052F:
            return "CYRILLIC"
        if 0x0370 <= code <= 0x03FF:
            return "GREEK"
        if 0x0600 <= code <= 0x06FF or 0x0750 <= code <= 0x077F or 0x08A0 <= code <= 0x08FF:
            return "ARABIC"
        if 0x0590 <= code <= 0x05FF:
            return "HEBREW"
        if 0x0900 <= code <= 0x097F:
            return "DEVANAGARI"
        if 0x0980 <= code <= 0x09FF:
            return "BENGALI"
        if 0x0B80 <= code <= 0x0BFF:
            return "TAMIL"
        if 0x4E00 <= code <= 0x9FFF or 0x3400 <= code <= 0x4DBF:
            return "CJK"
        if 0x3040 <= code <= 0x309F:
            return "HIRAGANA"
        if 0x30A0 <= code <= 0x30FF:
            return "KATAKANA"
        if 0xAC00 <= code <= 0xD7AF or 0x1100 <= code <= 0x11FF:
            return "HANGUL"

        name = unicodedata.name(char, "")
        for script_key in SCRIPT_CHARS_PER_TOKEN:
            if script_key in name:
                return script_key

        return "OTHER"

    @classmethod
    def calculate_vocab_vram_overhead(
        cls,
        vocab_size: int = 256000,
        hidden_dim: int = 4096,
        precision_bytes: int = 2,
    ) -> VocabVRAMFootprint:
        """Compute the VRAM locked by input embedding matrices and output LM heads.

        Args:
            vocab_size: Total tokens in vocabulary (e.g. 128k, 256k).
            hidden_dim: Model hidden dimension (e.g. 4096 for 8B-70B models).
            precision_bytes: 2 for FP16/BF16, 4 for FP32.
        """
        # Two matrices: input embeddings (vocab x dim) and output unembedding head (dim x vocab)
        total_parameters = 2 * vocab_size * hidden_dim
        vram_bytes = total_parameters * precision_bytes
        vram_gb = vram_bytes / 1e9

        return VocabVRAMFootprint(
            vocab_size=vocab_size,
            hidden_dim=hidden_dim,
            precision_bytes=precision_bytes,
            parameters_count=total_parameters,
            vram_bytes=vram_bytes,
            vram_gb=round(vram_gb, 2),
        )

    @classmethod
    def calculate_visual_patch_budget(
        cls,
        text_length: int,
        chars_per_line: int = 80,
        lines_per_page: int = 50,
        resolution: int = 1024,
        patch_size: int = 16,
    ) -> int:
        """Calculate continuous visual patches required to represent text rendered as pages.

        Args:
            text_length: Number of characters in text.
            chars_per_line: Average glyphs per rendered document line.
            lines_per_page: Standard document page lines capacity (~4000 chars/page).
            resolution: Rendered raster resolution (1024x1024).
            patch_size: ViT patch size (16x16).
        """
        chars_per_page = chars_per_line * lines_per_page
        pages = max(1, math.ceil(text_length / max(chars_per_page, 1)))
        patches_per_page = (resolution // patch_size) ** 2
        return pages * patches_per_page

    @classmethod
    def audit_text(
        cls,
        text: str,
        vocab_size: int = 256000,
        hidden_dim: int = 4096,
    ) -> TaxAuditReport:
        """Audit subword token expansion, multilingual inflation, and FinOps costs for a text payload."""
        total_chars = len(text)
        if total_chars == 0:
            return TaxAuditReport(
                raw_text_length=0,
                primary_script="EMPTY",
                script_breakdowns=[],
                total_estimated_tokens=0,
                baseline_latin_tokens=0,
                token_inflation_factor=1.0,
                equivalent_visual_patches=0,
                vocab_vram_overhead=cls.calculate_vocab_vram_overhead(vocab_size, hidden_dim),
                cost_comparison={},
                summary="Empty text payload.",
            )

        # Count character frequencies by script
        counts: Dict[str, int] = {}
        for char in text:
            script = cls.identify_script(char)
            counts[script] = counts.get(script, 0) + 1

        latin_density = SCRIPT_CHARS_PER_TOKEN["LATIN"]
        baseline_latin_tokens = max(1, math.ceil(total_chars / latin_density))

        script_breakdowns: List[ScriptBreakdown] = []
        total_tokens = 0

        for script, count in counts.items():
            density = SCRIPT_CHARS_PER_TOKEN.get(script, SCRIPT_CHARS_PER_TOKEN["OTHER"])
            tokens = math.ceil(count / density)
            total_tokens += tokens
            pct = (count / total_chars) * 100.0
            expansion = (latin_density / density) if density > 0 else 1.0

            script_breakdowns.append(
                ScriptBreakdown(
                    script_name=script,
                    char_count=count,
                    percentage=round(pct, 2),
                    estimated_tokens=tokens,
                    expansion_factor=round(expansion, 2),
                )
            )

        # Sort breakdowns by char count descending
        script_breakdowns.sort(key=lambda s: s.char_count, reverse=True)
        primary_script = script_breakdowns[0].script_name if script_breakdowns else "LATIN"
        token_inflation = total_tokens / baseline_latin_tokens

        # Financial cost projection across tiers
        cost_comparison: Dict[str, Dict[str, float]] = {}
        for tier, rates in PROVIDER_PRICING_PER_M_TOKENS.items():
            actual_input_cost = (total_tokens / 1_000_000.0) * rates["input"]
            baseline_input_cost = (baseline_latin_tokens / 1_000_000.0) * rates["input"]
            cost_tax = max(0.0, actual_input_cost - baseline_input_cost)
            cost_comparison[tier] = {
                "estimated_cost_usd": round(actual_input_cost, 6),
                "baseline_latin_cost_usd": round(baseline_input_cost, 6),
                "tokenizer_tax_usd": round(cost_tax, 6),
                "tax_percentage": round((token_inflation - 1.0) * 100.0, 1),
            }

        visual_patches = cls.calculate_visual_patch_budget(total_chars)
        vram_overhead = cls.calculate_vocab_vram_overhead(vocab_size, hidden_dim)

        summary = (
            f"Analyzed {total_chars} characters ({primary_script}). "
            f"Produced ~{total_tokens} subword tokens (Expansion: {token_inflation:.2f}x vs Latin). "
            f"Vocabulary consumes {vram_overhead.vram_gb:.2f} GB VRAM ({vram_overhead.parameters_count / 1e9:.2f}B parameters)."
        )

        return TaxAuditReport(
            raw_text_length=total_chars,
            primary_script=primary_script,
            script_breakdowns=script_breakdowns,
            total_estimated_tokens=total_tokens,
            baseline_latin_tokens=baseline_latin_tokens,
            token_inflation_factor=token_inflation,
            equivalent_visual_patches=visual_patches,
            vocab_vram_overhead=vram_overhead,
            cost_comparison=cost_comparison,
            summary=summary,
        )

    @classmethod
    def audit_file(
        cls,
        file_path: Path | str,
        vocab_size: int = 256000,
        hidden_dim: int = 4096,
    ) -> TaxAuditReport:
        """Audit text contents of a file."""
        p = Path(file_path)
        if not p.is_file():
            raise FileNotFoundError(f"File not found: {p}")
        text = p.read_text(encoding="utf-8", errors="replace")
        return cls.audit_text(text, vocab_size=vocab_size, hidden_dim=hidden_dim)

    @classmethod
    def compare_payloads(
        cls,
        source_text: str,
        target_text: str,
    ) -> Dict[str, Any]:
        """Directly compare tokenization expansion between two equivalent texts (e.g. English vs Arabic translation)."""
        source_audit = cls.audit_text(source_text)
        target_audit = cls.audit_text(target_text)

        ratio = (
            target_audit.total_estimated_tokens / max(1, source_audit.total_estimated_tokens)
        )
        return {
            "source_tokens": source_audit.total_estimated_tokens,
            "target_tokens": target_audit.total_estimated_tokens,
            "expansion_ratio": round(ratio, 2),
            "source_script": source_audit.primary_script,
            "target_script": target_audit.primary_script,
            "is_taxed": ratio > 1.2,
        }
