"""Cached analyzer facade for the local CogniPrint feature pipeline."""

from __future__ import annotations

from dataclasses import asdict
from functools import lru_cache
from typing import Any

from cogniprint.analysis import analyze_text


class CogniPrintAnalyzer:
    """Small cached analyzer facade.

    The current workstation uses deterministic stdlib feature extraction, so
    there are no external model weights to load. This class gives CLI and
    batch code a stable analyzer interface while preserving that lightweight
    baseline. If future optional models are added, they should be cached here.
    """

    def analyze(self, text: str) -> dict[str, Any]:
        profile = analyze_text(text)
        payload = asdict(profile)
        payload["disclaimer"] = (
            "CogniPrint outputs are research signals for profile analysis and comparison. "
            "They are not legal conclusions, source guarantees, or final judgments about a text."
        )
        return payload

    def analyze_batch(self, texts: list[str]) -> list[dict[str, Any]]:
        return [self.analyze(text) for text in texts]


@lru_cache(maxsize=1)
def get_analyzer() -> CogniPrintAnalyzer:
    """Return the process-local analyzer instance."""

    return CogniPrintAnalyzer()
