#!/usr/bin/env python3
"""Execute development-only smoke checks for open-world evaluation tools."""
from __future__ import annotations

from cogniprint.benchmarks.calibration import fit_temperature_scaling
from cogniprint.benchmarks.claims import (
    assert_aggregate_output_safe,
    evaluate_claim_narrowing,
)
from cogniprint.benchmarks.conformal import (
    fit_class_conditional_conformal,
    predict_conformal_unknown,
)
from cogniprint.benchmarks.surface import evaluate_surface_baseline
from cogniprint.benchmarks.uncertainty import (
    paired_group_bootstrap_delta,
    wilson_interval,
)


def vector(record: dict) -> list[float]:
    return list(record["vector"])


def main() -> int:
    train = []
    test = []
    for index in range(12):
        train.extend(
            [
                {
                    "model_family": "human",
                    "_text": f"I remember this scene, and it felt vivid! {index}",
                },
                {
                    "model_family": "model",
                    "_text": f"Structured analysis: item {index}; result: complete.",
                },
            ]
        )
    for index in range(4):
        test.extend(
            [
                {
                    "model_family": "human",
                    "_text": f"I recall the place, and I smiled! {index}",
                },
                {
                    "model_family": "model",
                    "_text": f"Formal summary: point {index}; status: verified.",
                },
            ]
        )
    surface = evaluate_surface_baseline(train, test)
    assert_aggregate_output_safe(surface)

    reference = []
    calibration = []
    for index in range(12):
        reference.extend(
            [
                {"model_family": "a", "vector": [1.0, index * 0.01]},
                {"model_family": "b", "vector": [index * 0.01, 1.0]},
            ]
        )
    for index in range(19):
        calibration.extend(
            [
                {"model_family": "a", "vector": [1.0, index * 0.005]},
                {"model_family": "b", "vector": [index * 0.005, 1.0]},
            ]
        )
    calibration.extend(
        [
            {"model_family": "a", "vector": [0.707, 0.707]},
            {"model_family": "b", "vector": [0.707, 0.707]},
        ]
    )
    conformal = fit_class_conditional_conformal(
        reference,
        calibration,
        vector,
        alpha=0.05,
    )
    decisions = {
        "known": predict_conformal_unknown(
            conformal,
            [0.99, 0.03],
            minimum_evidence_passed=True,
        ),
        "ood": predict_conformal_unknown(
            conformal,
            [-1.0, -1.0],
            minimum_evidence_passed=True,
        ),
        "ambiguous": predict_conformal_unknown(
            conformal,
            [0.707, 0.707],
            minimum_evidence_passed=True,
        ),
        "insufficient": predict_conformal_unknown(
            conformal,
            [1.0, 0.0],
            minimum_evidence_passed=False,
        ),
    }
    expected = {
        "known": "KNOWN",
        "ood": "UNKNOWN_OOD",
        "ambiguous": "UNKNOWN_AMBIGUOUS",
        "insufficient": "UNKNOWN_INSUFFICIENT_EVIDENCE",
    }
    if {
        key: value["decision"] for key, value in decisions.items()
    } != expected:
        raise AssertionError("conformal development decisions drifted")

    calibration_result = fit_temperature_scaling(
        [
            [8.0, 0.0],
            [8.0, 0.0],
            [8.0, 0.0],
            [8.0, 0.0],
            [8.0, 0.0],
            [8.0, 0.0],
            [0.0, 8.0],
            [0.0, 8.0],
        ],
        ["a", "a", "a", "a", "b", "b", "b", "b"],
        ("a", "b"),
        ece_bins=4,
    )
    if calibration_result.nll_after >= calibration_result.nll_before:
        raise AssertionError("temperature scaling did not improve fixture NLL")

    lower, upper = wilson_interval(10, 100)
    if not (0.055 < lower < 0.056 and 0.174 < upper < 0.175):
        raise AssertionError("Wilson interval reference drift")

    truth = ["a"] * 8 + ["b"] * 8
    groups = [f"a-{index // 2}" for index in range(8)] + [
        f"b-{index // 2}" for index in range(8)
    ]
    better = [
        "a", "a", "a", "a", "a", "a", "b", "a",
        "b", "b", "b", "b", "b", "b", "a", "b",
    ]
    worse = [
        "a", "b", "a", "b", "a", "b", "b", "a",
        "b", "a", "b", "a", "b", "a", "a", "b",
    ]
    bootstrap = paired_group_bootstrap_delta(
        truth,
        better,
        worse,
        groups,
        resamples=500,
        seed=20260730,
    )
    if bootstrap["point_delta"] <= 0.0:
        raise AssertionError("paired bootstrap fixture direction drift")

    claims = evaluate_claim_narrowing(
        {
            "held_out_false_known_point": 0.08,
            "held_out_false_known_wilson_upper": 0.14,
            "held_out_unknown_rejection": 0.92,
            "known_coverage": 0.70,
            "best_system_balanced_accuracy": 0.60,
            "best_system_macro_f1": 0.60,
            "cogniprint_vs_ngram_delta_macro_f1": 0.03,
            "cogniprint_vs_ngram_ci_lower": 0.01,
            "minimum_known_class_recall": 0.50,
            "ece": 0.08,
            "calibrated_nll": 0.70,
            "uncalibrated_nll": 0.80,
            "calibrated_brier": 0.30,
            "uncalibrated_brier": 0.35,
            "minimum_domain_balanced_accuracy": 0.50,
            "maximum_domain_drop": 0.10,
            "empty_primary_cells": 0,
            "t1_balanced_accuracy_drop": 0.10,
            "t1_false_known_increase": 0.03,
        }
    )
    assert_aggregate_output_safe(claims)
    if not claims["all_gates_clear"]:
        raise AssertionError("passing claim fixture unexpectedly triggered")

    print("STAGE_A_SURFACE_BASELINE_DEVELOPMENT_PASS")
    print("STAGE_A_CONFORMAL_UNKNOWN_DEVELOPMENT_PASS")
    print("STAGE_A_TEMPERATURE_CALIBRATION_DEVELOPMENT_PASS")
    print("STAGE_A_WILSON_BOOTSTRAP_CLAIM_MATRIX_DEVELOPMENT_PASS")
    print("STATUS=DEVELOPMENT_ONLY")
    print("CANONICAL_RESEARCH_FREEZE=PRE-FREEZE")
    print("EXTERNAL_REGISTRATION=NOT_SUBMITTED")
    print("STAGE_B=NOT_AUTHORISED_TO_START")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
