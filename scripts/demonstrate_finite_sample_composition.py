#!/usr/bin/env python3
"""Synthetic finite-sample composition certificate demonstration.

No RAID data are loaded. The counts are deterministic illustrative validation
counts chosen to represent a fixed product gate with approximately 95% known
acceptance and 5% unknown acceptance.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cogniprint.stats.finite_sample_composition import (
    ProductGateCounts,
    fixed_product_gate_certificate,
    known_membership_risk,
)


def certificate_for(n: int, pi_upper: float) -> dict[str, float | int | bool]:
    known_accept = round(0.95 * n)
    unknown_accept = round(0.05 * n)
    certificate = fixed_product_gate_certificate(
        ProductGateCounts(
            name=f"n-{n}",
            known_accept_count=known_accept,
            known_total=n,
            unknown_accept_count=unknown_accept,
            unknown_total=n,
        ),
        pi_upper=pi_upper,
        alpha=0.05,
    )
    return {
        "n": n,
        "pi_upper": pi_upper,
        "known_accept_count": known_accept,
        "unknown_accept_count": unknown_accept,
        "known_accept_lower": certificate.known_accept_lower,
        "unknown_accept_upper": certificate.unknown_accept_upper,
        "risk_upper": certificate.risk_upper,
        "admissible_at_delta_0_10": certificate.risk_upper <= 0.10,
    }


def build_payload() -> dict[str, object]:
    pi_sweep = [
        certificate_for(500, pi)
        for pi in (0.10, 0.30, 0.50, 0.70, 0.90, 1.00)
    ]
    n_sweep = [
        certificate_for(n, 0.50)
        for n in (50, 100, 200, 500, 1000, 2000)
    ]

    structural_floor = known_membership_risk(
        pi=0.50,
        known_accept_rate=0.95,
        unknown_accept_rate=0.05,
    )
    if structural_floor is None:
        raise RuntimeError("expected positive accepted mass")

    return {
        "status": "synthetic_finite_sample_composition_only",
        "raid_stage_a_used": False,
        "alpha": 0.05,
        "delta": 0.10,
        "illustrative_true_rates": {
            "known_accept_rate": 0.95,
            "unknown_accept_rate": 0.05,
        },
        "pi_sweep_n_500": pi_sweep,
        "n_sweep_pi_upper_0_50": n_sweep,
        "structural_floor_at_pi_0_50": structural_floor,
        "interpretation": [
            "Increasing validation sample size contracts the confidence contribution.",
            "The risk bound approaches the structural floor implied by pi_upper and component acceptance rates; it need not approach zero.",
            "If pi_upper=1, robust known-membership certification is vacuous for any gate that can accept unknown observations.",
        ],
    }


def line_svg(
    title: str,
    subtitle: str,
    x_label: str,
    rows: list[tuple[float, float]],
    x_formatter,
    output_width: int = 900,
    output_height: int = 500,
    horizontal_reference: float | None = 0.10,
    floor: float | None = None,
) -> str:
    left, right = 100, 825
    top, bottom = 80, 395
    y_max = max(0.20, max(y for _, y in rows) * 1.12)

    x_values = [x for x, _ in rows]
    x_min, x_max = min(x_values), max(x_values)

    def px(x: float) -> float:
        if x_max == x_min:
            return (left + right) / 2
        return left + (right - left) * (x - x_min) / (x_max - x_min)

    def py(y: float) -> float:
        return bottom - (bottom - top) * y / y_max

    pts = " ".join(f"{px(x):.1f},{py(y):.1f}" for x, y in rows)
    labels = []
    for x, y in rows:
        labels.append(
            f'<circle cx="{px(x):.1f}" cy="{py(y):.1f}" r="5" fill="#4f46e5"/>'
            f'<text x="{px(x):.1f}" y="{py(y)-12:.1f}" text-anchor="middle" '
            f'font-family="Arial" font-size="12">{y:.3f}</text>'
            f'<text x="{px(x):.1f}" y="{bottom+28}" text-anchor="middle" '
            f'font-family="Arial" font-size="12">{x_formatter(x)}</text>'
        )

    refs = ""
    if horizontal_reference is not None:
        yref = py(horizontal_reference)
        refs += (
            f'<line x1="{left}" y1="{yref:.1f}" x2="{right}" y2="{yref:.1f}" '
            f'stroke="#b42318" stroke-dasharray="7 6"/>'
            f'<text x="{right}" y="{yref-8:.1f}" text-anchor="end" '
            f'font-family="Arial" font-size="12" fill="#b42318">delta = {horizontal_reference:.2f}</text>'
        )
    if floor is not None:
        yf = py(floor)
        refs += (
            f'<line x1="{left}" y1="{yf:.1f}" x2="{right}" y2="{yf:.1f}" '
            f'stroke="#0f766e" stroke-dasharray="4 5"/>'
            f'<text x="{right}" y="{yf+16:.1f}" text-anchor="end" '
            f'font-family="Arial" font-size="12" fill="#0f766e">structural floor = {floor:.3f}</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{output_width}" height="{output_height}" viewBox="0 0 {output_width} {output_height}">
<rect width="100%" height="100%" fill="#ffffff"/>
<text x="450" y="32" text-anchor="middle" font-family="Arial" font-size="23" font-weight="700">{title}</text>
<text x="450" y="56" text-anchor="middle" font-family="Arial" font-size="13" fill="#555">{subtitle}</text>
<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#222" stroke-width="2"/>
<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#222" stroke-width="2"/>
{refs}
<polyline points="{pts}" fill="none" stroke="#4f46e5" stroke-width="4"/>
{''.join(labels)}
<text x="462" y="470" text-anchor="middle" font-family="Arial" font-size="14">{x_label}</text>
<text x="25" y="245" transform="rotate(-90 25 245)" text-anchor="middle" font-family="Arial" font-size="14">95% upper risk certificate</text>
</svg>'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    payload = build_payload()
    print(json.dumps(payload, indent=2, sort_keys=True))

    if args.output_dir is None:
        return

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "finite-sample-composition.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    pi_rows = [
        (float(row["pi_upper"]), float(row["risk_upper"]))
        for row in payload["pi_sweep_n_500"]
    ]
    n_rows = [
        (float(row["n"]), float(row["risk_upper"]))
        for row in payload["n_sweep_pi_upper_0_50"]
    ]

    (args.output_dir / "finite-sample-pi-sweep.svg").write_text(
        line_svg(
            title="Finite-sample certificate vs unknown-prevalence bound",
            subtitle="Illustrative fixed product gate; n_known = n_unknown = 500",
            x_label="pi_upper",
            rows=pi_rows,
            x_formatter=lambda value: f"{value:.1f}",
        ),
        encoding="utf-8",
    )

    (args.output_dir / "finite-sample-n-sweep.svg").write_text(
        line_svg(
            title="Sampling uncertainty contracts toward a structural floor",
            subtitle="Illustrative rates: a_K=0.95, a_U=0.05, pi_upper=0.50",
            x_label="validation samples per component",
            rows=n_rows,
            x_formatter=lambda value: str(int(value)),
            floor=float(payload["structural_floor_at_pi_0_50"]),
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
