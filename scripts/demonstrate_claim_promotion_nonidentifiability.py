#!/usr/bin/env python3
"""Synthetic Claim Promotion non-transfer demonstration.

No RAID record is loaded, fitted, tuned, or relabelled here.

The script constructs two worlds with identical closed-channel observations but
different latent source truth. A closed-set Clopper-Pearson certificate is
computed on the known-only calibration world and is then deliberately shown to
be out-of-scope for the camouflaged unknown-mixture world.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cogniprint.stats.claim_promotion import (
    blackwell_garbling_counterexample,
    camouflaged_mixture_selective_risk,
)
from cogniprint.stats.evidence_bounded import clopper_pearson_upper


def build_payload() -> dict[str, object]:
    n_cal = 200
    known_errors = 4
    alpha = 0.05
    known_risk = known_errors / n_cal
    cp_upper = clopper_pearson_upper(known_errors, n_cal, alpha)
    if cp_upper is None:
        raise RuntimeError("expected a non-empty calibration certificate")

    pi = 0.30
    mixture_risk = camouflaged_mixture_selective_risk(pi, known_risk)
    blackwell = blackwell_garbling_counterexample()

    return {
        "status": "synthetic_identifiability_demonstration_only",
        "raid_stage_a_used": False,
        "closed_calibration_world_D0": {
            "accepted_count": n_cal,
            "error_count": known_errors,
            "empirical_selective_risk": known_risk,
            "cp_upper_95": cp_upper,
        },
        "camouflaged_world_Dpi": {
            "unknown_fraction": pi,
            "closed_channel_law_changed": False,
            "known_component_selective_risk": known_risk,
            "population_selective_risk": mixture_risk,
            "identity": "pi + (1-pi)*known_risk",
        },
        "interpretation": {
            "cp_certificate_is_violated": False,
            "cp_certificate_transfers_to_Dpi": False,
            "reason": (
                "The certificate was calibrated for D0. Dpi is a different "
                "world with latent unknown mass despite an identical closed "
                "evidence-channel law."
            ),
        },
        "blackwell_toy": {
            "full_tv": blackwell.full_tv,
            "compressed_channel_tv": blackwell.channel_tv,
            "full_equal_prior_bayes_error": blackwell.full_bayes_error,
            "compressed_equal_prior_bayes_error": blackwell.channel_bayes_error,
        },
    }


def render_svg(payload: dict[str, object]) -> str:
    d0 = payload["closed_calibration_world_D0"]
    dpi = payload["camouflaged_world_Dpi"]
    assert isinstance(d0, dict)
    assert isinstance(dpi, dict)
    empirical = float(d0["empirical_selective_risk"])
    bound = float(d0["cp_upper_95"])
    mixture = float(dpi["population_selective_risk"])

    width = 900
    height = 520
    chart_top = 90
    chart_bottom = 410
    chart_height = chart_bottom - chart_top
    max_y = max(0.40, mixture * 1.15)

    def y(value: float) -> float:
        return chart_bottom - chart_height * value / max_y

    def bar(x: int, value: float, label: str, fill: str) -> str:
        top = y(value)
        h = chart_bottom - top
        return (
            f'<rect x="{x}" y="{top:.1f}" width="120" height="{h:.1f}" '
            f'rx="10" fill="{fill}"/>'
            f'<text x="{x+60}" y="{top-12:.1f}" text-anchor="middle" '
            f'font-family="Arial" font-size="18">{value:.3f}</text>'
            f'<text x="{x+60}" y="450" text-anchor="middle" '
            f'font-family="Arial" font-size="15">{label}</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="#ffffff"/>
<text x="450" y="36" text-anchor="middle" font-family="Arial" font-size="24" font-weight="700">Closed-channel certificate does not transfer across observationally equivalent latent worlds</text>
<text x="450" y="62" text-anchor="middle" font-family="Arial" font-size="14" fill="#555">Synthetic construction; no RAID data used</text>
<line x1="90" y1="{chart_bottom}" x2="820" y2="{chart_bottom}" stroke="#222" stroke-width="2"/>
<line x1="90" y1="{chart_top}" x2="90" y2="{chart_bottom}" stroke="#222" stroke-width="2"/>
{bar(170, empirical, "D0 empirical risk", "#8aa4d8")}
{bar(390, bound, "D0 CP upper 95%", "#516fa7")}
{bar(610, mixture, "Dπ population risk", "#bd5b5b")}
<text x="450" y="490" text-anchor="middle" font-family="Arial" font-size="13" fill="#555">The D0 certificate remains valid for D0; Dπ is outside its target distribution.</text>
</svg>'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    payload = build_payload()
    print(json.dumps(payload, indent=2, sort_keys=True))

    if args.output_dir is not None:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "claim-promotion-demo.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (args.output_dir / "claim-promotion-non-transfer.svg").write_text(
            render_svg(payload),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
