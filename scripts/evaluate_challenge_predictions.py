#!/usr/bin/env python3
"""Evaluate frozen CogniPrint challenge predictions against revealed labels.

Evaluation-only by design: this script does not fit a classifier, tune a
threshold, calibrate a score, or inspect source text. Predictions should be
frozen and hashed before labels are revealed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any


ABSTAIN_DECISIONS = {"unknown", "insufficient-evidence"}
ALLOWED_DECISIONS = {"known"} | ABSTAIN_DECISIONS


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number}: row must be an object")
            sample_id = row.get("sample_id")
            if not isinstance(sample_id, str) or not sample_id.strip():
                raise ValueError(f"{path}:{line_number}: sample_id must be non-empty")
            if sample_id in seen:
                raise ValueError(f"{path}:{line_number}: duplicate sample_id: {sample_id}")
            seen.add(sample_id)
            rows.append(row)
    if not rows:
        raise ValueError(f"{path}: no JSONL records found")
    return rows


def validate_prediction(row: dict[str, Any]) -> None:
    sample_id = row["sample_id"]
    if any(key in row for key in ("ground_truth", "true_class", "known_to_reference")):
        raise ValueError(f"prediction {sample_id}: ground-truth fields are forbidden")

    decision = row.get("decision")
    if decision not in ALLOWED_DECISIONS:
        raise ValueError(f"prediction {sample_id}: invalid decision {decision!r}")

    top1 = row.get("top1_candidate")
    if decision == "known":
        if not isinstance(top1, str) or not top1.strip():
            raise ValueError(f"prediction {sample_id}: known decision requires top1_candidate")
    elif top1 not in (None, ""):
        raise ValueError(f"prediction {sample_id}: abstention decision must not carry top1_candidate")

    confidence = row.get("confidence")
    if confidence is not None:
        if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
            raise ValueError(f"prediction {sample_id}: confidence must be numeric")
        if not math.isfinite(float(confidence)) or not 0 <= float(confidence) <= 1:
            raise ValueError(f"prediction {sample_id}: confidence must be in [0,1]")
        if not isinstance(row.get("calibrated"), bool):
            raise ValueError(f"prediction {sample_id}: confidence requires boolean calibrated")

    probabilities = row.get("probabilities")
    if probabilities is not None:
        if not isinstance(probabilities, dict) or not probabilities:
            raise ValueError(f"prediction {sample_id}: probabilities must be a non-empty object")
        total = 0.0
        for label, value in probabilities.items():
            if not isinstance(label, str) or not label:
                raise ValueError(f"prediction {sample_id}: invalid probability label")
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"prediction {sample_id}: probabilities must be numeric")
            value = float(value)
            if not math.isfinite(value) or not 0 <= value <= 1:
                raise ValueError(f"prediction {sample_id}: probabilities must be in [0,1]")
            total += value
        if abs(total - 1.0) > 1e-6:
            raise ValueError(f"prediction {sample_id}: probabilities must sum to 1.0 (got {total})")
        if row.get("calibrated") is not True:
            raise ValueError(f"prediction {sample_id}: probabilities require calibrated=true")


def validate_label(row: dict[str, Any]) -> None:
    sample_id = row["sample_id"]
    if not isinstance(row.get("known_to_reference"), bool):
        raise ValueError(f"label {sample_id}: known_to_reference must be boolean")
    if not isinstance(row.get("true_class"), str) or not row["true_class"].strip():
        raise ValueError(f"label {sample_id}: true_class must be non-empty")


def safe_div(num: float, den: float) -> float | None:
    return None if den == 0 else num / den


def rounded(value: float | None) -> float | None:
    return None if value is None else round(value, 6)


def per_class_metrics(joined: list[tuple[dict[str, Any], dict[str, Any]]], classes: list[str]) -> dict[str, dict[str, float | int]]:
    result: dict[str, dict[str, float | int]] = {}
    for class_name in classes:
        tp = fp = fn = support = 0
        for prediction, label in joined:
            if not label["known_to_reference"]:
                continue
            truth = label["true_class"]
            predicted = prediction.get("top1_candidate") if prediction["decision"] == "known" else None
            if truth == class_name:
                support += 1
                if predicted == class_name:
                    tp += 1
                else:
                    fn += 1
            elif predicted == class_name:
                fp += 1

        # Explicit zero_division=0 semantics keep an unpredicted true class in macro-F1.
        precision = 0.0 if tp + fp == 0 else tp / (tp + fp)
        recall = 0.0 if tp + fn == 0 else tp / (tp + fn)
        f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
        result[class_name] = {
            "support": support,
            "precision": round(precision, 6),
            "recall": round(recall, 6),
            "f1": round(f1, 6),
        }
    return result


def confusion_counts(joined: list[tuple[dict[str, Any], dict[str, Any]]], classes: list[str]) -> dict[str, dict[str, int]]:
    matrix = {truth: {pred: 0 for pred in classes + ["__ABSTAIN__"]} for truth in classes}
    for prediction, label in joined:
        if not label["known_to_reference"]:
            continue
        truth = label["true_class"]
        predicted = prediction.get("top1_candidate") if prediction["decision"] == "known" else "__ABSTAIN__"
        matrix[truth].setdefault(str(predicted), 0)
        matrix[truth][str(predicted)] += 1
    return matrix


def brier_score_known(joined: list[tuple[dict[str, Any], dict[str, Any]]], known_classes: list[str]) -> float | None:
    scored: list[float] = []
    for prediction, label in joined:
        if not label["known_to_reference"]:
            continue
        probabilities = prediction.get("probabilities")
        if not isinstance(probabilities, dict):
            continue
        # Include every probability dimension actually emitted so mass assigned to
        # UNKNOWN/other classes is not silently ignored.
        dimensions = sorted(set(known_classes) | set(probabilities))
        truth = label["true_class"]
        score = sum(
            (float(probabilities.get(name, 0.0)) - (1.0 if name == truth else 0.0)) ** 2
            for name in dimensions
        )
        scored.append(score)
    return None if not scored else sum(scored) / len(scored)


def expected_calibration_error(joined: list[tuple[dict[str, Any], dict[str, Any]]], *, bins: int) -> dict[str, Any] | None:
    if bins < 2:
        raise ValueError("ECE bins must be >= 2")
    values: list[tuple[float, int]] = []
    for prediction, label in joined:
        if not label["known_to_reference"] or prediction["decision"] != "known":
            continue
        confidence = prediction.get("confidence")
        if confidence is None or prediction.get("calibrated") is not True:
            continue
        values.append((float(confidence), int(prediction.get("top1_candidate") == label["true_class"])))
    if not values:
        return None

    ece = 0.0
    table: list[dict[str, Any]] = []
    for index in range(bins):
        lower, upper = index / bins, (index + 1) / bins
        selected = [v for v in values if lower <= v[0] < upper or (index == bins - 1 and v[0] == 1.0)]
        row: dict[str, Any] = {"bin": index, "lower": round(lower, 6), "upper": round(upper, 6), "count": len(selected)}
        if selected:
            mean_conf = sum(v[0] for v in selected) / len(selected)
            accuracy = sum(v[1] for v in selected) / len(selected)
            ece += len(selected) / len(values) * abs(accuracy - mean_conf)
            row.update(mean_confidence=round(mean_conf, 6), accuracy=round(accuracy, 6))
        table.append(row)
    return {"ece": round(ece, 6), "bins": bins, "n": len(values), "table": table}


def evaluate(predictions: list[dict[str, Any]], labels: list[dict[str, Any]], *, ece_bins: int) -> dict[str, Any]:
    for row in predictions:
        validate_prediction(row)
    for row in labels:
        validate_label(row)

    pred_by_id = {row["sample_id"]: row for row in predictions}
    label_by_id = {row["sample_id"]: row for row in labels}
    if set(pred_by_id) != set(label_by_id):
        raise ValueError(
            "prediction/label sample sets differ: "
            f"missing_predictions={sorted(set(label_by_id) - set(pred_by_id))[:10]} "
            f"missing_labels={sorted(set(pred_by_id) - set(label_by_id))[:10]}"
        )

    joined = [(pred_by_id[sample_id], label_by_id[sample_id]) for sample_id in sorted(label_by_id)]
    known_rows = [(p, l) for p, l in joined if l["known_to_reference"]]
    unknown_rows = [(p, l) for p, l in joined if not l["known_to_reference"]]
    classes = sorted({l["true_class"] for _, l in known_rows})
    metrics = per_class_metrics(joined, classes)

    correct_known = sum(1 for p, l in known_rows if p["decision"] == "known" and p.get("top1_candidate") == l["true_class"])
    issued_known = sum(1 for p, _ in known_rows if p["decision"] == "known")
    rejected_unknown = sum(1 for p, _ in unknown_rows if p["decision"] in ABSTAIN_DECISIONS)
    macro_f1 = None if not classes else sum(float(metrics[c]["f1"]) for c in classes) / len(classes)
    balanced_accuracy = None if not classes else sum(float(metrics[c]["recall"]) for c in classes) / len(classes)
    selective_accuracy = safe_div(correct_known, issued_known)

    decisions = Counter(p["decision"] for p, _ in joined)
    return {
        "schema": "cogniprint-challenge-evaluation-v0.1",
        "counts": {
            "total": len(joined),
            "known_reference": len(known_rows),
            "unknown_reference": len(unknown_rows),
            "decision_counts": dict(sorted(decisions.items())),
        },
        "closed_set_known_reference": {
            "top1_accuracy_with_abstentions_as_errors": rounded(safe_div(correct_known, len(known_rows))),
            "balanced_accuracy_with_abstentions_as_errors": rounded(balanced_accuracy),
            "macro_f1_with_abstentions_as_errors": rounded(macro_f1),
            "coverage_on_known_reference": rounded(safe_div(issued_known, len(known_rows))),
            "abstention_rate_on_known_reference": rounded(safe_div(len(known_rows) - issued_known, len(known_rows))),
            "selective_accuracy_on_issued_known": rounded(selective_accuracy),
            "selective_risk_on_issued_known": rounded(None if selective_accuracy is None else 1 - selective_accuracy),
            "per_class": metrics,
            "confusion_matrix": confusion_counts(joined, classes),
        },
        "open_world_unknown_reference": {
            "unknown_rejection_rate": rounded(safe_div(rejected_unknown, len(unknown_rows))),
            "false_known_rate": rounded(safe_div(len(unknown_rows) - rejected_unknown, len(unknown_rows))),
        },
        "calibration": {
            "multiclass_brier_known_reference": rounded(brier_score_known(joined, classes)),
            "ece_known_issued_decisions": expected_calibration_error(joined, bins=ece_bins),
            "note": "Missing calibration data is reported as null, never inferred or back-filled.",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predictions", required=True, type=Path)
    parser.add_argument("--labels", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--ece-bins", type=int, default=10)
    args = parser.parse_args()

    report = evaluate(load_jsonl(args.predictions), load_jsonl(args.labels), ece_bins=args.ece_bins)
    report["artifacts"] = {
        "predictions_sha256": sha256_file(args.predictions),
        "labels_sha256": sha256_file(args.labels),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **report["artifacts"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
