#!/usr/bin/env python3
"""Exact identified-set demonstration for known-membership claims.

No bootstrap and no RAID data are used. The curves are analytic consequences
of declared mixture and acceptance-rate assumptions.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cogniprint.stats.identified_sets import (
    critical_unknown_fraction,
    identified_unknown_risk_interval,
    posterior_unknown_risk,
    robust_claim_admissible,
)


def curve(known_accept: float, unknown_accept: float, points: int = 101):
    rows = []
    for i in range(points):
        pi = i / (points - 1)
        risk = posterior_unknown_risk(pi, known_accept, unknown_accept)
        rows.append((pi, risk))
    return rows


def build_payload() -> dict[str, object]:
    delta = 0.10

    closed = identified_unknown_risk_interval(
        0.0,
        0.5,
        known_accept_rate=0.50,
        unknown_accept_rate=0.50,
    )
    refined = identified_unknown_risk_interval(
        0.0,
        0.5,
        known_accept_rate=0.95,
        unknown_accept_rate=0.05,
    )
    if closed is None or refined is None:
        raise RuntimeError("expected non-empty accepted populations")

    return {
        "status": "synthetic_identified_set_demonstration_only",
        "raid_stage_a_used": False,
        "delta": delta,
        "world_class": {"unknown_fraction_bounds": [0.0, 0.5]},
        "closed_channel": {
            "known_accept_rate": 0.50,
            "unknown_accept_rate": 0.50,
            "identified_risk_interval": [closed.lower, closed.upper],
            "admissible": robust_claim_admissible(closed, delta),
            "interpretation": "pure camouflage: posterior unknown risk equals pi",
        },
        "illustrative_refinement_channel": {
            "known_accept_rate": 0.95,
            "unknown_accept_rate": 0.05,
            "identified_risk_interval": [refined.lower, refined.upper],
            "admissible": robust_claim_admissible(refined, delta),
            "critical_pi": critical_unknown_fraction(delta, 0.95, 0.05),
            "measured_on_real_data": False,
        },
        "important_nonclaim": (
            "The refinement-channel rates are illustrative assumptions, not "
            "measured CogniPrint OOD performance."
        ),
    }


def render_svg(payload: dict[str, object]) -> str:
    width, height = 920, 560
    left, right = 92, 850
    top, bottom = 80, 440
    delta = float(payload["delta"])

    closed_curve = curve(0.50, 0.50)
    refined_curve = curve(0.95, 0.05)

    def xy(pi: float, risk: float) -> tuple[float, float]:
        x = left + (right - left) * pi
        y = bottom - (bottom - top) * risk
        return x, y

    def path(rows):
        pts = []
        for pi, risk in rows:
            if risk is None:
                continue
            x, y = xy(pi, risk)
            pts.append(f"{x:.1f},{y:.1f}")
        return " ".join(pts)

    _, delta_y = xy(0.0, delta)
    critical = critical_unknown_fraction(delta, 0.95, 0.05)
    critical_x = None
    if critical is not None:
        critical_x, _ = xy(critical, 0.0)

    vertical = ""
    if critical_x is not None:
        vertical = (
            f'<line x1="{critical_x:.1f}" y1="{top}" x2="{critical_x:.1f}" '
            f'y2="{bottom}" stroke="#0f766e" stroke-dasharray="5 5"/>'
            f'<text x="{critical_x-8:.1f}" y="{top+18}" text-anchor="end" '
            f'font-family="Arial" font-size="13" fill="#0f766e">'
            f'critical π ≈ {critical:.3f}</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="#ffffff"/>
<text x="460" y="34" text-anchor="middle" font-family="Arial" font-size="24" font-weight="700">Identified risk set for a known-membership claim</text>
<text x="460" y="58" text-anchor="middle" font-family="Arial" font-size="14" fill="#555">Synthetic assumptions only; no RAID data used</text>
<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#222" stroke-width="2"/>
<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#222" stroke-width="2"/>
<line x1="{left}" y1="{delta_y:.1f}" x2="{right}" y2="{delta_y:.1f}" stroke="#b42318" stroke-dasharray="7 6"/>
<text x="{right-4}" y="{delta_y-8:.1f}" text-anchor="end" font-family="Arial" font-size="13" fill="#b42318">δ = {delta:.2f}</text>
<polyline points="{path(closed_curve)}" fill="none" stroke="#4f46e5" stroke-width="4"/>
<polyline points="{path(refined_curve)}" fill="none" stroke="#0f766e" stroke-width="4"/>
{vertical}
<text x="500" y="210" font-family="Arial" font-size="15" fill="#4f46e5">closed channel / exact camouflage</text>
<text x="570" y="385" font-family="Arial" font-size="15" fill="#0f766e">illustrative refining channel</text>
<text x="470" y="510" text-anchor="middle" font-family="Arial" font-size="15">π = prior fraction of unknown sources</text>
<text x="24" y="265" transform="rotate(-90 24 265)" text-anchor="middle" font-family="Arial" font-size="15">P(unknown | accepted)</text>
</svg>'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    payload = build_payload()
    print(json.dumps(payload, indent=2, sort_keys=True))

    if args.output_dir is not None:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "identified-set-admissibility.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (args.output_dir / "identified-set-admissibility.svg").write_text(
            render_svg(payload),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
