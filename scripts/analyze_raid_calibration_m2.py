#!/usr/bin/env python3
"""Run privacy-preserving RAID M2 calibration/abstention development analysis.

The script rehydrates only the already selected Stage A records from a pinned
RAID source, verifies hashes and source contract, runs the predeclared
leave-one-machine-family-out protocol twice, and persists metadata/aggregate
results only. It does not authorize Challenge 001 Stage B.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from analyze_raid_ngrams import (
    assert_safe_payload,
    load_json,
    load_jsonl,
    rehydrate_selected_records,
    selection_manifest_sha256,
    sha256_file,
    verify_source_contract,
)
from cogniprint.benchmarks.raid_m2 import (
    DEFAULT_MACHINE_FAMILIES,
    build_open_set_fold,
    evaluate_raid_m2,
)


def sha256_json(payload: Any) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    assert_safe_payload(payload)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def role_manifest_payload(records: list[dict[str, Any]], *, seed: int, alpha: float) -> dict[str, Any]:
    folds: list[dict[str, Any]] = []
    for unknown in DEFAULT_MACHINE_FAMILIES:
        fold = build_open_set_fold(
            records,
            unknown_family=unknown,
            seed=seed,
            conformal_alpha=alpha,
        )
        folds.append(
            {
                "unknown_family": unknown,
                "known_labels": fold["known_labels"],
                "role_assignment_sha256": fold["role_assignment_sha256"],
                "role_summary": fold["role_summary"],
                "records": fold["role_manifest"],
            }
        )
    payload = {
        "schema": "cogniprint-raid-m2-role-manifest-001",
        "status": "DEVELOPMENT_ONLY",
        "stage_b_status": "NOT_AUTHORISED_TO_START",
        "seed": seed,
        "conformal_alpha": alpha,
        "folds": folds,
        "raw_text_persisted": False,
        "raw_prompt_persisted": False,
    }
    assert_safe_payload(payload)
    return payload


def markdown_report(result: dict[str, Any]) -> str:
    lines = [
        "# CogniPrint RAID M2 — calibration, abstention and open-set development",
        "",
        f"Status: {result['status']}",
        f"Readiness: {result['readiness_boundary']}",
        f"Stage B: {result['stage_b_status']}",
        f"Unknown-family design: {result['unknown_family_design']}",
        f"Conformal alpha: {result['conformal_alpha']}",
        f"Minimum known coverage policy: {result['minimum_known_coverage']}",
        "",
        "## Aggregate four-fold development summary",
        "",
        "| Representation | Mean macro-F1 | Mean NLL | Mean Brier | Mean AURC | Mean false-known | Mean conformal false-known |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    labels = {
        "cogniprint_12d_cosine_centroid": "CogniPrint 12D cosine centroid",
        "character_3_5_hashed_tfidf": "Character 3–5 hashed TF-IDF",
        "word_1_2_hashed_tfidf": "Word 1–2 hashed TF-IDF",
    }
    for key in (
        "cogniprint_12d_cosine_centroid",
        "character_3_5_hashed_tfidf",
        "word_1_2_hashed_tfidf",
    ):
        row = result["aggregate"][key]
        lines.append(
            "| "
            + " | ".join(
                [
                    labels[key],
                    f"{row['mean_macro_f1']:.6f}",
                    f"{row['mean_calibrated_nll']:.6f}",
                    f"{row['mean_calibrated_brier']:.6f}",
                    f"{row['mean_aurc']:.6f}",
                    f"{row['mean_false_known_rate']:.6f}",
                    f"{row['mean_conformal_unknown_false_known_rate']:.6f}",
                ]
            )
            + " |"
        )

    lines += [
        "",
        "## Interpretation boundary",
        "",
        (
            "This is Stage A-visible development evidence. All four machine "
            "families are already exposed to the development process; the "
            "leave-one-family-out folds prevent within-fold fitting on the "
            "designated unknown family but do not make this a blind external test."
        ),
        (
            "No representation is required to win. A negative or mixed result "
            "must be retained without changing the seed, role fractions, alpha, "
            "coverage policy or representation definitions after inspection."
        ),
        result["interpretation_boundary"],
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features", type=Path, required=True)
    parser.add_argument("--input-file", type=Path, required=True)
    parser.add_argument("--expected-source-sha256", required=True)
    parser.add_argument("--expected-features-sha256", required=True)
    parser.add_argument("--expected-selection-manifest-sha256", required=True)
    parser.add_argument("--source-contract", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=20261124)
    parser.add_argument("--conformal-alpha", type=float, default=0.05)
    parser.add_argument("--minimum-known-coverage", type=float, default=0.60)
    parser.add_argument("--char-dimensions", type=int, default=262_144)
    parser.add_argument("--word-dimensions", type=int, default=131_072)
    parser.add_argument("--bootstrap-resamples", type=int, default=10_000)
    args = parser.parse_args()

    source_path = args.input_file.resolve()
    features_path = args.features.resolve()
    contract_path = args.source_contract.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    source_sha256 = sha256_file(source_path)
    if source_sha256 != args.expected_source_sha256:
        raise ValueError(
            "source SHA-256 mismatch: "
            f"expected {args.expected_source_sha256}, got {source_sha256}"
        )
    features_sha256 = sha256_file(features_path)
    if features_sha256 != args.expected_features_sha256:
        raise ValueError(
            "features SHA-256 mismatch: "
            f"expected {args.expected_features_sha256}, got {features_sha256}"
        )

    contract = load_json(contract_path)
    verify_source_contract(contract, source_sha256, source_path.stat().st_size)

    selected = load_jsonl(features_path)
    actual_selection_sha256 = selection_manifest_sha256(selected)
    if actual_selection_sha256 != args.expected_selection_manifest_sha256:
        raise ValueError(
            "selected-record manifest SHA-256 mismatch: "
            f"expected {args.expected_selection_manifest_sha256}, "
            f"got {actual_selection_sha256}"
        )

    hydrated, rehydration_audit = rehydrate_selected_records(source_path, selected)

    run_kwargs = {
        "seed": args.seed,
        "conformal_alpha": args.conformal_alpha,
        "minimum_known_coverage": args.minimum_known_coverage,
        "char_dimensions": args.char_dimensions,
        "word_dimensions": args.word_dimensions,
        "bootstrap_resamples": args.bootstrap_resamples,
    }
    first = evaluate_raid_m2(hydrated, **run_kwargs)
    second = evaluate_raid_m2(hydrated, **run_kwargs)
    first_sha256 = sha256_json(first)
    second_sha256 = sha256_json(second)
    if first_sha256 != second_sha256:
        raise AssertionError("M2 deterministic rerun mismatch")

    role_manifest = role_manifest_payload(
        hydrated,
        seed=args.seed,
        alpha=args.conformal_alpha,
    )
    result = dict(first)
    result["source_sha256"] = source_sha256
    result["source_contract_sha256"] = sha256_file(contract_path)
    result["selected_features_sha256"] = features_sha256
    result["selection_manifest_sha256"] = actual_selection_sha256
    result["source_rehydration"] = {
        key: value
        for key, value in rehydration_audit.items()
        if key not in {"scanned_source_rows"}
    }
    result["raw_text_persisted"] = False
    result["raw_prompt_persisted"] = False

    reproducibility = {
        "schema": "cogniprint-raid-m2-reproducibility-001",
        "status": "PASS",
        "run_1_sha256": first_sha256,
        "run_2_sha256": second_sha256,
        "match": True,
        "seed": args.seed,
        "source_sha256": source_sha256,
        "selected_features_sha256": features_sha256,
        "selection_manifest_sha256": actual_selection_sha256,
    }

    assert_safe_payload(result)
    assert_safe_payload(role_manifest)
    assert_safe_payload(reproducibility)

    write_json(output_dir / "m2-results.json", result)
    write_json(output_dir / "m2-role-manifest.json", role_manifest)
    write_json(output_dir / "m2-reproducibility.json", reproducibility)
    (output_dir / "m2-report.md").write_text(
        markdown_report(result),
        encoding="utf-8",
    )

    print(output_dir / "m2-results.json")
    print(output_dir / "m2-role-manifest.json")
    print(output_dir / "m2-reproducibility.json")
    print(output_dir / "m2-report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
