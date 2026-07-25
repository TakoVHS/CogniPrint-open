#!/usr/bin/env python3
"""Evaluate frozen CogniPrint challenge predictions against revealed labels.

This script is intentionally evaluation-only: it does not fit a classifier,
change thresholds, calibrate scores, or inspect source text. Predictions should
be frozen and hashed before labels are revealed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any


KNOWN_DECISIONS = {"known"}
ABSTAIN_DECISIONS = {"unknown", "insufficient-evidence"}
ALLOWED_DECISIONS = KNOWN_DECISIONS | ABSTAIN_DECISIONS


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            line = raw.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number}: row must be a JSON object")
            sample_id = row.get("sample_id")
            if not isinstance(sample_id, str) or not sample_id.strip():
                raise ValueError(f"{path}:{line_number}: sample_id must be a non-empty string")
            if sample_id in seen_ids:
                raise ValueError(f"{path}:{line_number}: duplicate sample_id: {sample_id}")
            seen_ids.add(sample_id)
            rows.append(row)
    if not rows:
        raise ValueError(f"{path}: no JSONL records found")
    return rows


def validate_prediction(row: dict[str, Any]) -> None:
    if any(key in row for key in ("ground_truth", "true_class", "known_to_reference")):
        raise ValueError(f"prediction {row['sample_id']}: ground-truth fields are forbidden")
    decision = row.get("decision")
    if decision not in ALLOWED_DECISIONS:
        raise ValueError(
            f"prediction {row['sample_id']}: decision must be one of {sorted(ALLOWED_DECISIONS)}"
        )
    top1 = row.get("top1_candidate")
    if decision == "known":
        if not isinstance(top1, str) or not top1.strip():
            raise ValueError(f"prediction {row['sample_id']}: known decision requires top1_candidate")
    elif top1 not in (None, ""):
        raise ValueError(
            f"prediction {row['sample_id']}: abstention decision must not carry top1_candidate"
        )

    confidence = row.get("confidence")
    if confidence is not None:
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
            raise ValueError(f"prediction {row['sample_id']}: confidence must be numeric")
        if not math.isfinite(float(confidence)) or not 0.0 <= float(confidence) <= 1.0:
            raise ValueError(f"prediction {row['sample_id']}: confidence must be in [0,1]")
        if "calibrated" not in row or not isinstance(row.get("calibrated"), bool):
            raise ValueError(
                f"prediction {row['sample_id']}: confidence requires boolean calibrated field"
            )

    probabilities = row.get("probabilities")
    if probabilities is not None:
        if not isinstance(probabilities, dict) or not probabilities:
            raise ValueError(f"prediction {row['sample_id']}: probabilities must be a non-empty object")
        total = 0.0
        for label, value in probabilities.items():
            if not isinstance(label, str) or not label:
                raise ValueError(f"prediction {row['sample_id']}: probability label must be non-empty")
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise ValueError(f"prediction {row['sample_id']}: probabilities must be numeric")
            number = float(value)
            if not math.isfinite(number) or number < 0.0 or number > 1.0:
                raise ValueError(f"prediction {row['sample_id']}: probabilities must be in [0,1]")
            total += number
        if abs(total - 1.0) > 1e-6:
            raise ValueError(
                f"prediction {row['sample_id']}: probabilities must sum to 1.0 (got {total})"
            )
        if row.get("calibrated") is not True:
            raise ValueError(
                f"prediction {row['sample_id']}: probabilities require calibrated=true"
            )


def validate_label(row: dict[str, Any]) -> None:
    known = row.get("known_to_reference")
    if not isinstance(known, bool):
        raise ValueError(f"label {row['sample_id']}: known_to_reference must be boolean")
    true_class = row.get("true_class")
    if not isinstance(true_class, str) or not true_class.strip():
        raise ValueError(f"label {row['sample_id']}: true_class must be a non-empty string")


def safe_div(numerator: float, denominator: float) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


def rounded(value: float | None) -> float | None:
    return None if value is None else round(value, 6)


def confusion_counts(
    joined: list[tuple[dict[str, Any], dict[str, Any]]],
    classes: list[str],
) -> dict[str, dict[str, int]]:
    matrix = {truth: {pred: 0 for pred in classes + ["__ABSTAIN__"]} for truth in classes}
    for prediction, label in joined:
        if not label["known_to_reference"]:
            continue
        truth = label["true_class"]
        predicted = prediction.get("top1_candidate") if prediction["decision"] == "known" else "__ABSTAIN__"
        if truth in matrix:
            matrix[truth].setdefault(str(predicted), 0)
            matrix[truth][str(predicted)] += 1
    return matrix


def per_class_metrics(
    joined: list[tuple[dict[str, Any], dict[str, Any]]],
    classes: list[str],
) -> dict[str, dict[str, float | int | None]]:
    result: dict[str, dict[str, float | int | None]] = {}
    for class_name in classes:
        tp = fp = fn = 0
        support = 0
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
        precision = safe_div(tp, tp + fp)
        recall = safe_div(tp, tp + fn)
        if precision is None or recall is None or precision + recall == 0:
            f1 = None if precision is None or recall is None else 0.0
        else:
            f1 = 2 * precision * recall / (precision + recall)
        result[class_name] = {
            "support": support,
            "precision": rounded(precision),
            "recall": rounded(recall),
            "f1": rounded(f1),
        }
    return result


def mean_defined(values: list[float | None]) -> float | None:
    defined = [value for value in values if value is not None]
    return None if not defined else sum(defined) / len(defined)


def brier_score_known(
    joined: list[tuple[dict[str, Any], dict[str, Any]]],
    classes: list[str],
) -> float | None:
    rows: list[float] = []
    for prediction, label in joined:
        if not label["known_to_reference"]:
            continue
        probabilities = prediction.get("probabilities")
        if not isinstance(probabilities, dict):
            continue
        truth = label["true_class"]
        score = 0.0
        for class_name in classes:
            probability = float(probabilities.get(class_name, 0.0))
            target = 1.0 if class_name == truth else 0.0
            score += (probability - target) ** 2
        rows.append(score)
    return None if not rows else sum(rows) / len(rows)


def expected_calibration_error(
    joined: list[tuple[dict[str, Any], dict[str, Any]]],
    *,
    bins: int,
) -> dict[str, Any] | None:
    if bins < 2:
        raise ValueError("ECE bins must be >= 2")
    observations: list[tuple[float, int]] = []
    for prediction, label in joined:
        if not label["known_to_reference"] or prediction["decision"] != "known":
            continue
        confidence = prediction.get("confidence")
        if confidence is None or prediction.get("calibrated") is not True:
            continue
        correct = int(prediction.get("top1_candidate") == label["true_class"])
        observations.append((float(confidence), correct))
    if not observations:
        return None

    total = len(observations)
    ece = 0.0
    table: list[dict[str, Any]] = []
    for index in range(bins):
        lower = index / bins
        upper = (index + 1) / bins
        selected = [item for item in observations if lower <= item[0] < upper or (index == bins - 1 and item[0] == 1.0)]
        if not selected:
            table.append({"bin": index, "lower": lower, "upper": upper, "count": 0})
            continue
        mean_confidence = sum(item[0] for item in selected) / len(selected)
        accuracy = sum(item[1] for item in selected) / len(selected)
        ece += (len(selected) / total) * abs(accuracy - mean_confidence)
        table.append(
            {
                "bin": index,
                "lower": round(lower, 6),
                "upper": round(upper, 6),
                "count": len(selected),
                "mean_confidence": round(mean_confidence, 6),
                "accuracy": round(accuracy, 6),
            }
        )
    return {"ece": round(ece, 6), "bins": bins, "n": total, "table": table}


def evaluate(
    predictions: list[dict[str, Any]],
    labels: list[dict[str, Any]],
    *,
    ece_bins: int,
) -> dict[str, Any]:
    for row in predictions:
        validate_prediction(row)
    for row in labels:
        validate_label(row)

    predictions_by_id = {row["sample_id"]: row for row in predictions}
    labels_by_id = {row["sample_id"]: row for row in labels}
    if set(predictions_by_id) != set(labels_by_id):
        missing_predictions = sorted(set(labels_by_id) - set(predictions_by_id))
        missing_labels = sorted(set(predictions_by_id) - set(labels_by_id))
        raise ValueError(
            "prediction/label sample sets differ: "
            f"missing_predictions={missing_predictions[:10]} missing_labels={missing_labels[:10]}"
        )

    joined = [(predictions_by_id[sample_id], labels_by_id[sample_id]) for sample_id in sorted(labels_by_id)]
    known_rows = [(prediction, label) for prediction, label in joined if label["known_to_reference"]]
    unknown_rows = [(prediction, label) for prediction, label in joined if not label["known_to_reference"]]
    classes = sorted({label["true_class"] for _, label in known_rows})

    correct_known = sum(
        1
        for prediction, label in known_rows
        if prediction["decision"] == "known" and prediction.get("top1_candidate") == label["true_class"]
    )
    issued_known_on_known = sum(1 for prediction, _ in known_rows if prediction["decision"] == "known")
    abstained_known = len(known_rows) - issued_known_on_known
    rejected_unknown = sum(1 for prediction, _ in unknown_rows if prediction["decision"] in ABSTAIN_DECISIONS)
    false_known_unknown = len(unknown_rows) - rejected_unknown
    total_known_decisions = sum(1 for prediction, _ in joined if prediction["decision"] == "known")

    class_metrics = per_class_metrics(joined, classes)
    macro_f1 = mean_defined([metrics["f1"] for metrics in class_metrics.values()])
    macro_recall = mean_defined([metrics["recall"] for metrics in class_metrics.values()])

    selective_accuracy = safe_div(correct_known, issued_known_on_known)
    selective_risk = None if selective_accuracy is None else 1.0 - selective_accuracy

    decision_counts = Counter(prediction["decision"] for prediction, _ in joined)
    calibrated_confidence_rows = sum(
        1
        for prediction, _ in joined
        if prediction.get("confidence") is not None and prediction.get("calibrated") is True
    )

    return {
        "schema": "cogniprint-challenge-evaluation-v0.1",
        "counts": {
            "total": len(joined),
            "known_reference": len(known_rows),
            "unknown_reference": len(unknown_rows),
            "known_decisions": total_known_decisions,
            "decision_counts": dict(sorted(decision_counts.items())),
            "calibrated_confidence_rows": calibrated_confidence_rows,
        },
        "closed_set_known_reference": {
            "top1_accuracy_with_abstentions_as_errors": rounded(safe_div(correct_known, len(known_rows))),
            "balanced_accuracy_with_abstentions_as_errors": rounded(macro_recall),
            "macro_f1_with_abstentions_as_errors": rounded(macro_f1),
            "coverage_on_known_reference": rounded(safe_div(issued_known_on_known, len(known_rows))),
            "abstention_rate_on_known_reference": rounded(safe_div(abstained_known, len(known_rows))),
            "selective_accuracy_on_issued_known": rounded(selective_accuracy),
            "selective_risk_on_issued_known": rounded(selective_risk),
            "per_class": class_metrics,
            "confusion_matrix": confusion_counts(joined, classes),
        },
        "open_world_unknown_reference": {
            "unknown_rejection_rate": rounded(safe_div(rejected_unknown, len(unknown_rows))),
            "false_known_rate": rounded(safe_div(false_known_unknown, len(unknown_rows))),
        },
        "calibration": {
            "multiclass_brier_known_reference": rounded(brier_score_known(joined, classes)),
            "ece_known_issued_decisions": expected_calibration_error(joined, bins=ece_bins),
            "note": (
                "Calibration metrics are reported only when the frozen prediction rows contain the required "
                "calibrated probabilities/confidence. Missing calibration data is reported as null, not inferred."
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predictions", required=True, type=Path)
    parser.add_argument("--labels", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--ece-bins", type=int, default=10)
    args = parser.parse_args()

    predictions = load_jsonl(args.predictions)
    labels = load_jsonl(args.labels)
    report = evaluate(predictions, labels, ece_bins=args.ece_bins)
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
