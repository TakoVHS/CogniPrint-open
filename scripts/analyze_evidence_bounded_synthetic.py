#!/usr/bin/env python3
"""Synthetic demonstrations for Evidence-Bounded Inference v0.1.

This script intentionally does not train on or tune the exposed RAID Stage A
records. It demonstrates the algebraic certificates on finite synthetic spaces.
"""

from __future__ import annotations

import json

from cogniprint.stats.evidence_bounded import (
    conformal_singleton_risk_upper_bound,
    finite_space_selective_summary,
    threshold_for_target_risk,
)


def main() -> None:
    finite = finite_space_selective_summary(
        weights=[0.20, 0.25, 0.25, 0.30],
        confidences=[0.96, 0.91, 0.76, 0.52],
        correctness_probabilities=[0.93, 0.88, 0.73, 0.55],
        threshold=0.90,
    )

    target_rows = []
    for delta in (0.05, 0.10, 0.15, 0.20):
        target_rows.append(
            {
                "delta": delta,
                "epsilon": finite.calibration_defect,
                "sufficient_threshold": threshold_for_target_risk(
                    delta,
                    finite.calibration_defect,
                ),
            }
        )

    conformal_rows = []
    for coverage in (0.10, 0.25, 0.50, 0.75, 1.00):
        conformal_rows.append(
            {
                "alpha": 0.10,
                "singleton_coverage": coverage,
                "selective_risk_upper_bound": (
                    conformal_singleton_risk_upper_bound(0.10, coverage)
                ),
            }
        )

    payload = {
        "status": "synthetic_theory_demonstration_only",
        "raid_stage_a_retrained": False,
        "finite_space": {
            "coverage": finite.coverage,
            "selective_risk": finite.selective_risk,
            "calibration_defect": finite.calibration_defect,
            "theorem_bound": finite.theorem_bound,
        },
        "target_risk_thresholds": target_rows,
        "conformal_singleton_bounds": conformal_rows,
        "interpretation": [
            "The finite-space example satisfies the algebraic selective-risk certificate.",
            "A certificate requiring threshold > 1 is infeasible, but that is not an impossibility theorem about actual risk.",
            "Marginal conformal validity yields alpha/kappa, not alpha, for singleton selective risk.",
        ],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
