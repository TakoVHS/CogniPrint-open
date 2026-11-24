#!/usr/bin/env python3
"""Finite-world Certificate Scope Judgment demonstration.

The examples are synthetic and do not use RAID Stage A data.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cogniprint.stats.certificate_scope import (
    FiniteCertificate,
    FiniteClaim,
    compose_same_target,
    composed_confidence_budget,
    direct_static_compatible,
    find_heterogeneous_composition_witness,
    find_nonpromotion_witness,
    runtime_direct_promotion_allowed,
    sharp_finite_claim_bound_under_certificates,
)


def build_payload() -> dict[str, object]:
    same_risk = {"safe": 0.03, "edge": 0.08}
    direct_certificate = FiniteCertificate(
        name="direct-risk-certificate",
        target="known-family-error",
        scope=frozenset(same_risk),
        risk_by_world=same_risk,
        bound=0.09,
        alpha=0.05,
    )
    direct_claim = FiniteClaim(
        name="direct-claim",
        target="known-family-error",
        scope=frozenset(same_risk),
        risk_by_world=same_risk,
        delta=0.10,
    )

    closed_certificate = FiniteCertificate(
        name="closed-set-certificate",
        target="known-family-error",
        scope=frozenset({"d0", "dpi"}),
        risk_by_world={"d0": 0.05, "dpi": 0.05},
        bound=0.08,
        alpha=0.05,
    )
    membership_claim = FiniteClaim(
        name="known-membership",
        target="unknown-contamination",
        scope=frozenset({"d0", "dpi"}),
        risk_by_world={"d0": 0.00, "dpi": 0.35},
        delta=0.10,
    )

    same_a = FiniteCertificate(
        name="same-a",
        target="shared-risk",
        scope=frozenset({"w"}),
        risk_by_world={"w": 0.07},
        bound=0.10,
        alpha=0.02,
    )
    same_b = FiniteCertificate(
        name="same-b",
        target="shared-risk",
        scope=frozenset({"w"}),
        risk_by_world={"w": 0.07},
        bound=0.08,
        alpha=0.03,
    )
    same_composed = compose_same_target(same_a, same_b)

    family = FiniteCertificate(
        name="family",
        target="family-risk",
        scope=frozenset({"w1", "w2"}),
        risk_by_world={"w1": 0.02, "w2": 0.02},
        bound=0.05,
        alpha=0.02,
    )
    ood = FiniteCertificate(
        name="ood",
        target="ood-risk",
        scope=frozenset({"w1", "w2"}),
        risk_by_world={"w1": 0.03, "w2": 0.03},
        bound=0.05,
        alpha=0.03,
    )
    provenance = FiniteClaim(
        name="provenance",
        target="provenance-risk",
        scope=frozenset({"w1", "w2"}),
        risk_by_world={"w1": 0.04, "w2": 0.40},
        delta=0.10,
    )
    provenance_warranted = FiniteClaim(
        name="provenance-warranted-finite",
        target="provenance-risk",
        scope=frozenset({"w1", "w2"}),
        risk_by_world={"w1": 0.04, "w2": 0.09},
        delta=0.10,
    )

    return {
        "status": "candidate_interface_synthetic_demo_only",
        "raid_stage_a_used": False,
        "direct": {
            "static_compatible": direct_static_compatible(
                direct_certificate,
                direct_claim,
            ),
            "runtime_promotion_allowed": runtime_direct_promotion_allowed(
                direct_certificate,
                direct_claim,
            ),
        },
        "target_mismatch": {
            "static_compatible": direct_static_compatible(
                closed_certificate,
                membership_claim,
            ),
            "witness": find_nonpromotion_witness(
                closed_certificate,
                membership_claim,
            ),
        },
        "same_target_composition": {
            "bound": same_composed.bound,
            "alpha": same_composed.alpha,
        },
        "heterogeneous_composition_without_warrant": {
            "counterworld": find_heterogeneous_composition_witness(
                (family, ood),
                provenance,
            ),
            "union_bound_alpha": composed_confidence_budget((family, ood)),
        },
        "finite_quantitative_warrant": {
            "sharp_claim_bound": sharp_finite_claim_bound_under_certificates(
                (family, ood),
                provenance_warranted,
            ),
            "counterworld": find_heterogeneous_composition_witness(
                (family, ood),
                provenance_warranted,
            ),
            "delta": provenance_warranted.delta,
            "union_bound_alpha": composed_confidence_budget((family, ood)),
        },
        "interpretation": (
            "Low-risk certificates for different targets do not authorize a "
            "semantic provenance claim when a compatible counterworld survives."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    payload = build_payload()
    print(json.dumps(payload, indent=2, sort_keys=True))

    if args.output_dir is not None:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "certificate-scope-judgment.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
