#!/usr/bin/env python3
"""Synthetic sharp-composition demonstration.

No RAID data are used. The finite worlds instantiate the exact population
criterion: product evidence is useful only when its observed conditional
signature eliminates claim-unsafe worlds from the coarse evidence fiber.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cogniprint.stats.evidence_composition import (
    FiniteCompositionWorld,
    composition_report,
    delta_separating,
    robustly_admissible,
)


def build_payload() -> dict[str, object]:
    delta = 0.10

    informative = [
        FiniteCompositionWorld("safe", 0.04, "z", "k_obs"),
        FiniteCompositionWorld("unsafe-a", 0.35, "z", "k_a"),
        FiniteCompositionWorld("unsafe-b", 0.60, "z", "k_b"),
    ]
    redundant = [
        FiniteCompositionWorld("safe", 0.04, "z", "same"),
        FiniteCompositionWorld("unsafe-a", 0.35, "z", "same"),
        FiniteCompositionWorld("unsafe-b", 0.60, "z", "same"),
    ]

    informative_report = composition_report(informative, "z", "k_obs")
    redundant_report = composition_report(redundant, "z", "same")

    return {
        "status": "synthetic_sharp_composition_demonstration_only",
        "raid_stage_a_used": False,
        "delta": delta,
        "informative_refinement": {
            "coarse_risks": informative_report.coarse_risks,
            "product_risks": informative_report.product_risks,
            "coarse_upper": informative_report.coarse_upper,
            "product_upper": informative_report.product_upper,
            "coarse_admissible": robustly_admissible(
                informative_report.coarse_upper,
                delta,
            ),
            "product_admissible": robustly_admissible(
                informative_report.product_upper,
                delta,
            ),
            "delta_separating": delta_separating(
                informative,
                "z",
                "k_obs",
                delta,
            ),
        },
        "redundant_refinement": {
            "coarse_risks": redundant_report.coarse_risks,
            "product_risks": redundant_report.product_risks,
            "coarse_upper": redundant_report.coarse_upper,
            "product_upper": redundant_report.product_upper,
            "strict_shrink": redundant_report.strict_shrink,
        },
        "nonclaim": (
            "The finite signatures illustrate the theorem. They are not "
            "measured OOD/provenance channels and establish no CogniPrint "
            "deployment performance."
        ),
    }


def render_svg(payload: dict[str, object]) -> str:
    info = payload["informative_refinement"]
    red = payload["redundant_refinement"]
    assert isinstance(info, dict)
    assert isinstance(red, dict)

    rows = [
        ("E only", float(info["coarse_upper"])),
        ("E + claim-relevant F", float(info["product_upper"])),
        ("E + redundant F", float(red["product_upper"])),
    ]
    delta = float(payload["delta"])
    width, height = 900, 500
    left, right = 110, 820
    top, bottom = 75, 390
    ymax = 0.70

    def y(v: float) -> float:
        return bottom - (bottom - top) * v / ymax

    bars = []
    xs = [180, 400, 620]
    fills = ["#4f46e5", "#0f766e", "#687083"]
    for (label, value), x, fill in zip(rows, xs, fills):
        yy = y(value)
        bars.append(
            f'<rect x="{x}" y="{yy:.1f}" width="120" height="{bottom-yy:.1f}" '
            f'rx="10" fill="{fill}"/>'
            f'<text x="{x+60}" y="{yy-10:.1f}" text-anchor="middle" '
            f'font-family="Arial" font-size="18">{value:.2f}</text>'
            f'<text x="{x+60}" y="430" text-anchor="middle" '
            f'font-family="Arial" font-size="14">{label}</text>'
        )

    dy = y(delta)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="#ffffff"/>
<text x="450" y="34" text-anchor="middle" font-family="Arial" font-size="24" font-weight="700">Sharp evidence-channel composition</text>
<text x="450" y="58" text-anchor="middle" font-family="Arial" font-size="14" fill="#555">Synthetic finite worlds; lower worst-case risk requires elimination of unsafe worlds</text>
<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#222" stroke-width="2"/>
<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#222" stroke-width="2"/>
<line x1="{left}" y1="{dy:.1f}" x2="{right}" y2="{dy:.1f}" stroke="#b42318" stroke-dasharray="7 6"/>
<text x="{right-2}" y="{dy-8:.1f}" text-anchor="end" font-family="Arial" font-size="13" fill="#b42318">δ = {delta:.2f}</text>
{''.join(bars)}
<text x="24" y="235" transform="rotate(-90 24 235)" text-anchor="middle" font-family="Arial" font-size="15">Worst-case identified claim risk</text>
<text x="450" y="476" text-anchor="middle" font-family="Arial" font-size="13" fill="#555">A new channel is claim-relevant only if its joint/conditional law excludes risk-compatible worlds.</text>
</svg>'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    payload = build_payload()
    print(json.dumps(payload, indent=2, sort_keys=True))

    if args.output_dir is not None:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "sharp-composition.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (args.output_dir / "sharp-composition.svg").write_text(
            render_svg(payload),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
