from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "web" / "index.html"


def require(text: str, marker: str) -> None:
    if marker not in text:
        raise SystemExit(f"reviewer web contract missing: {marker}")


def main() -> None:
    text = HOME.read_text(encoding="utf-8")

    required = [
        'id="origin"',
        'id="theory"',
        'id="results"',
        'data-evidence-chart="stage-a-macro-f1"',
        'id="multi-agent"',
        'id="boundary"',
        "φ(T) = [f₁(T), f₂(T), …, f₁₂(T)]",
        "H(X) = −Σ p(x) log₂ p(x)",
        "0.5973",
        "0.5952",
        "0.5369",
        "0.5359",
        "Portable Evidence Capsules",
        "Optional third-party model API integration.",
        "Roman Adriashkin — Independent Researcher-Engineer",
        "descriptive_only",
    ]
    for marker in required:
        require(text, marker)

    ordered = [
        'id="origin"',
        'id="theory"',
        'id="results"',
        'id="multi-agent"',
        'id="boundary"',
    ]
    positions = [text.index(marker) for marker in ordered]
    if positions != sorted(positions):
        raise SystemExit("reviewer web contract order regressed")

    if "311" in text or "0/1" in text:
        raise SystemExit("internal readiness counters leaked into reviewer homepage")

    if text.index("Not established") < text.index('id="results"'):
        raise SystemExit("scientific limitations appear before empirical evidence")

    print("REVIEWER_WEB_CONTRACT=PASS")


if __name__ == "__main__":
    main()
