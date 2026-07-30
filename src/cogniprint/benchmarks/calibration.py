"""Development-only deterministic temperature calibration utilities."""
from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from statistics import fmean
from typing import Any, Sequence


def _finite(value: float, name: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _validate_logits(
    logits: Sequence[Sequence[float]],
    truth: Sequence[str],
    classes: Sequence[str],
) -> tuple[list[list[float]], list[str], tuple[str, ...]]:
    if not logits or len(logits) != len(truth):
        raise ValueError("logits and truth must be non-empty and equal length")
    class_tuple = tuple(classes)
    if not class_tuple or len(set(class_tuple)) != len(class_tuple):
        raise ValueError("classes must be unique and non-empty")
    if any(label not in class_tuple for label in truth):
        raise ValueError("truth contains a label absent from classes")
    rows: list[list[float]] = []
    for row_index, row in enumerate(logits):
        values = [_finite(value, f"logits[{row_index}]") for value in row]
        if len(values) != len(class_tuple):
            raise ValueError("every logit row must match class count")
        rows.append(values)
    return rows, list(truth), class_tuple


def _probability_row(
    row: Sequence[float],
    width: int,
) -> list[float]:
    values = [_finite(value, "probability") for value in row]
    if len(values) != width:
        raise ValueError("probability row is incompatible with classes")
    if any(not 0.0 <= value <= 1.0 for value in values):
        raise ValueError("probabilities must be in [0,1]")
    if abs(sum(values) - 1.0) > 1e-9:
        raise ValueError("probability row must sum to one")
    return values


def temperature_softmax(
    logits: Sequence[float],
    temperature: float,
) -> list[float]:
    temperature = _finite(temperature, "temperature")
    if temperature <= 0.0:
        raise ValueError("temperature must be positive")
    if not logits:
        raise ValueError("logits must be non-empty")
    scaled = [_finite(value, "logit") / temperature for value in logits]
    maximum = max(scaled)
    exponentials = [math.exp(value - maximum) for value in scaled]
    total = sum(exponentials)
    return [value / total for value in exponentials]


def multiclass_nll(
    probabilities: Sequence[Sequence[float]],
    truth: Sequence[str],
    classes: Sequence[str],
) -> float:
    if not probabilities or len(probabilities) != len(truth):
        raise ValueError("probabilities and truth must be non-empty and equal length")
    class_tuple = tuple(classes)
    index = {label: position for position, label in enumerate(class_tuple)}
    losses: list[float] = []
    for row, label in zip(probabilities, truth):
        if label not in index:
            raise ValueError("truth label is incompatible with classes")
        values = _probability_row(row, len(class_tuple))
        probability = min(1.0, max(1e-15, values[index[label]]))
        losses.append(-math.log(probability))
    return fmean(losses)


def multiclass_brier(
    probabilities: Sequence[Sequence[float]],
    truth: Sequence[str],
    classes: Sequence[str],
) -> float:
    if not probabilities or len(probabilities) != len(truth):
        raise ValueError("probabilities and truth must be non-empty and equal length")
    class_tuple = tuple(classes)
    index = {label: position for position, label in enumerate(class_tuple)}
    losses: list[float] = []
    for row, label in zip(probabilities, truth):
        if label not in index:
            raise ValueError("truth label is incompatible with classes")
        values = _probability_row(row, len(class_tuple))
        losses.append(
            sum(
                (
                    probability
                    - (1.0 if position == index[label] else 0.0)
                )
                ** 2
                for position, probability in enumerate(values)
            )
        )
    return fmean(losses)


def expected_calibration_error(
    probabilities: Sequence[Sequence[float]],
    truth: Sequence[str],
    classes: Sequence[str],
    *,
    bins: int = 15,
) -> float:
    """Return equal-frequency multiclass top-label ECE."""

    if bins <= 0:
        raise ValueError("bins must be positive")
    if not probabilities or len(probabilities) != len(truth):
        raise ValueError("probabilities and truth must be non-empty and equal length")
    class_tuple = tuple(classes)
    samples: list[tuple[float, int, int]] = []
    for row_index, (row, label) in enumerate(zip(probabilities, truth)):
        if label not in class_tuple:
            raise ValueError("truth label is incompatible with classes")
        values = _probability_row(row, len(class_tuple))
        predicted_index = min(
            range(len(values)),
            key=lambda index: (
                -values[index],
                class_tuple[index],
            ),
        )
        confidence = values[predicted_index]
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("confidence must be in [0,1]")
        samples.append(
            (
                confidence,
                int(class_tuple[predicted_index] == label),
                row_index,
            )
        )
    samples.sort(key=lambda item: (item[0], item[2]))
    effective_bins = min(bins, len(samples))
    ece = 0.0
    for bin_index in range(effective_bins):
        start = bin_index * len(samples) // effective_bins
        end = (bin_index + 1) * len(samples) // effective_bins
        bucket = samples[start:end]
        mean_confidence = fmean(item[0] for item in bucket)
        mean_accuracy = fmean(item[1] for item in bucket)
        ece += (
            len(bucket)
            / len(samples)
            * abs(mean_accuracy - mean_confidence)
        )
    return ece


@dataclass(frozen=True)
class TemperatureCalibrationResult:
    temperature: float
    nll_before: float
    nll_after: float
    brier_before: float
    brier_after: float
    ece_before: float
    ece_after: float
    ece_bins: int
    accepted: bool

    def to_public_dict(self) -> dict[str, Any]:
        return asdict(self)


def fit_temperature_scaling(
    logits: Sequence[Sequence[float]],
    truth: Sequence[str],
    classes: Sequence[str],
    *,
    lower: float = 0.05,
    upper: float = 20.0,
    iterations: int = 160,
    ece_bins: int = 15,
    ece_max: float = 0.10,
) -> TemperatureCalibrationResult:
    """Fit one temperature by deterministic bounded NLL minimization."""

    rows, labels, class_tuple = _validate_logits(logits, truth, classes)
    if not 0.0 < lower < upper or iterations <= 0:
        raise ValueError("invalid search bounds or iteration count")

    def probabilities(temperature: float) -> list[list[float]]:
        return [temperature_softmax(row, temperature) for row in rows]

    def objective(log_temperature: float) -> float:
        return multiclass_nll(
            probabilities(math.exp(log_temperature)),
            labels,
            class_tuple,
        )

    left = math.log(lower)
    right = math.log(upper)
    ratio = (math.sqrt(5.0) - 1.0) / 2.0
    x1 = right - ratio * (right - left)
    x2 = left + ratio * (right - left)
    f1 = objective(x1)
    f2 = objective(x2)
    for _ in range(iterations):
        if f1 <= f2:
            right, x2, f2 = x2, x1, f1
            x1 = right - ratio * (right - left)
            f1 = objective(x1)
        else:
            left, x1, f1 = x1, x2, f2
            x2 = left + ratio * (right - left)
            f2 = objective(x2)

    candidates = [
        lower,
        upper,
        1.0,
        math.exp((left + right) / 2.0),
    ]
    temperature = min(
        candidates,
        key=lambda value: (objective(math.log(value)), value),
    )
    before = probabilities(1.0)
    after = probabilities(temperature)
    nll_before = multiclass_nll(before, labels, class_tuple)
    nll_after = multiclass_nll(after, labels, class_tuple)
    brier_before = multiclass_brier(before, labels, class_tuple)
    brier_after = multiclass_brier(after, labels, class_tuple)
    ece_before = expected_calibration_error(
        before,
        labels,
        class_tuple,
        bins=ece_bins,
    )
    ece_after = expected_calibration_error(
        after,
        labels,
        class_tuple,
        bins=ece_bins,
    )
    accepted = (
        ece_after <= ece_max
        and nll_after <= nll_before + 1e-12
        and brier_after <= brier_before + 1e-12
    )
    return TemperatureCalibrationResult(
        temperature=round(temperature, 12),
        nll_before=round(nll_before, 12),
        nll_after=round(nll_after, 12),
        brier_before=round(brier_before, 12),
        brier_after=round(brier_after, 12),
        ece_before=round(ece_before, 12),
        ece_after=round(ece_after, 12),
        ece_bins=ece_bins,
        accepted=accepted,
    )
