#!/usr/bin/env python3
"""Run pinned RAID M2.1 post-result exploratory diagnostics.

The command rehydrates only the historical Stage A selection, verifies source
custody, executes the frozen M2.1 diagnostic protocol twice, and persists
raw-text-free diagnostic artifacts. It does not modify M2 #1.
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
from cogniprint.benchmarks.raid_m2_1 import evaluate_raid_m2_1


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


def markdown_report(result: dict[str, Any]) -> str:
    names = {
        "cogniprint_12d_cosine_centroid": "CogniPrint 12D",
        "character_3_5_hashed_tfidf": "Character 3–5",
        "word_1_2_hashed_tfidf": "Word 1–2",
    }
    lines = [
        "# RAID M2.1 — post-result exploratory diagnostics",
        "",
        f"Status: `{result['status']}`",
        f"Parent M2 results SHA-256: `{result['parent_m2_results_sha256']}`",
        "",
        "This report is exploratory and cannot replace M2 #1.",
        "",
        "## Per-fold diagnostic summary",
        "",
    ]
    for fold in result["folds"]:
        lines += [
            f"### Unknown family: {fold['unknown_family']}",
            "",
            "| Representation | M2 T | Grid-best T | Unknown empty | Unknown ambiguous | Unknown false-known singleton | Known singleton | Frozen-policy coverage | Frozen-policy risk |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
        for key, label in names.items():
            rep = fold["representations"][key]
            unknown = rep["conformal_decomposition"]["unknown"]
            known = rep["conformal_decomposition"]["known"]
            policy = rep["frozen_threshold_policy"]["known_evaluation"]
            lines.append(
                "| "
                + " | ".join(
                    [
                        label,
                        f"{rep['m2_temperature']:.6f}",
                        f"{rep['temperature_sensitivity']['best_grid_temperature']:.6f}",
                        f"{unknown['empty_set_rate']:.6f}",
                        f"{unknown['ambiguous_set_rate']:.6f}",
                        f"{unknown['singleton_false_known_rate']:.6f}",
                        f"{known['singleton_rate']:.6f}",
                        f"{policy['coverage']:.6f}",
                        (
                            "NA"
                            if policy["selective_risk"] is None
                            else f"{policy['selective_risk']:.6f}"
                        ),
                    ]
                )
                + " |"
            )
        lines.append("")

    lines += [
        "## Interpretation boundary",
        "",
        result["interpretation_boundary"],
        "",
        "Matched-coverage values in this report are M2.1 exploratory outputs and are not retroactive primary M2 outcomes.",
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

    kwargs = {
        "seed": args.seed,
        "conformal_alpha": args.conformal_alpha,
        "minimum_known_coverage": args.minimum_known_coverage,
        "char_dimensions": args.char_dimensions,
        "word_dimensions": args.word_dimensions,
    }
    first = evaluate_raid_m2_1(hydrated, **kwargs)
    second = evaluate_raid_m2_1(hydrated, **kwargs)
    first_hash = sha256_json(first)
    second_hash = sha256_json(second)
    if first_hash != second_hash:
        raise AssertionError("M2.1 deterministic rerun mismatch")

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
        "schema": "cogniprint-raid-m2-1-reproducibility-001",
        "status": "PASS",
        "run_1_sha256": first_hash,
        "run_2_sha256": second_hash,
        "match": True,
        "seed": args.seed,
        "source_sha256": source_sha256,
        "selected_features_sha256": features_sha256,
        "selection_manifest_sha256": actual_selection_sha256,
    }

    assert_safe_payload(result)
    assert_safe_payload(reproducibility)
    write_json(output_dir / "m2-1-diagnostics.json", result)
    write_json(output_dir / "m2-1-reproducibility.json", reproducibility)
    (output_dir / "m2-1-report.md").write_text(
        markdown_report(result),
        encoding="utf-8",
    )

    print(output_dir / "m2-1-diagnostics.json")
    print(output_dir / "m2-1-reproducibility.json")
    print(output_dir / "m2-1-report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
