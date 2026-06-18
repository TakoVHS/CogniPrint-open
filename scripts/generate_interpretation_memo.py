#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def load_decision(path: Path) -> str:
    if not path.exists():
        return "pending"
    payload = json.loads(path.read_text(encoding="utf-8"))
    return str(payload.get("decision", "pending")).strip().lower()


def effect_label(value: float | None) -> str:
    if value is None:
        return "unavailable"
    magnitude = abs(value)
    if magnitude < 0.2:
        return "negligible"
    if magnitude < 0.5:
        return "small"
    if magnitude < 0.8:
        return "medium"
    return "large"


def build_memo(validation: dict[str, object]) -> str:
    group1 = validation["group1"]
    group2 = validation["group2"]
    difference = validation["mean_difference"]
    hedges_g = validation.get("hedges_g")
    return f"""# Interpretation Memo v1

Date: {date.today()}

This memo is a manuscript-facing interpretation note for the current empirical package. It does not approve a new benchmark expansion by itself and does not strengthen public claims beyond the current descriptive layer.

## Basis

- evidence package: `evidence/empirical-v1/`
- benchmark reference: `evidence/public-benchmark-v1.1/`
- validation note: `docs/validation-status.md`
- benchmark shift note: `docs/benchmark-shift-note-v1.1.md`
- benchmark decision memo: `docs/benchmark-decision-memo-v1.1.md`

## Current descriptive snapshot

- reference group: `{group1['name']}` (`n={group1['count']}`)
- comparison group: `{group2['name']}` (`n={group2['count']}`)
- {group1['name']} mean cosine similarity: `{group1['mean']}`
- {group2['name']} mean cosine similarity: `{group2['mean']}`
- mean difference (`{group1['name']} - {group2['name']}`): `{difference['group1_minus_group2']}`
- 95% bootstrap CI for the mean difference: `[{difference['lower']}, {difference['upper']}]`
- Hedges' g: `{hedges_g}`
- Cliff's delta: `{validation.get('cliffs_delta')}`
- permutation p-value: `{validation.get('permutation_p_value')}`

## Interpretation

The current aggregate export shows an observed separation between the derived `{group1['name']}` and `{group2['name']}` perturbation tiers for cosine similarity. On conventional effect-size language, the current Hedges' g is best described as `{effect_label(hedges_g)}`.

This remains a descriptive finding rather than a generalized inference. The benchmark-composition analysis in `docs/benchmark-shift-note-v1.1.md` and `docs/benchmark-decision-memo-v1.1.md` still indicates material sensitivity of the reference layer to benchmark mix changes. That is the main reason this memo keeps manuscript wording narrow.

## Recommended use

1. Use this memo as a reviewer-facing interpretation note.
2. Keep public wording aligned with “working empirical evidence package supporting a follow-up manuscript”.
3. Do not treat the present descriptive effect as a forensic, attribution, or broad-domain generalization result.

## Explicit limitations

- small and still-evolving benchmark layer;
- descriptive validation only;
- no external cross-validation or benchmark-scale inferential claim;
- benchmark composition still moves the reference behavior materially enough to constrain wording.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a manuscript-facing interpretation memo from the current validation snapshot.")
    parser.add_argument("--decision-file", type=Path, default=Path("docs/decisions/final-decision.json"))
    parser.add_argument("--validation-file", type=Path, default=Path("docs/validation-status.json"))
    parser.add_argument("--output", type=Path, default=Path("docs/interpretation-memo-v1.md"))
    parser.add_argument("--skip-decision-check", action="store_true")
    args = parser.parse_args(argv)

    root = Path(__file__).resolve().parents[1]
    if not args.skip_decision_check:
        decision = load_decision(root / args.decision_file)
        if decision != "memo":
            raise SystemExit(f"Refusing to generate interpretation memo before a memo decision. Current decision: {decision}")

    validation_path = root / args.validation_file
    if not validation_path.exists():
        raise SystemExit(f"Missing validation snapshot: {validation_path}")
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    output_path = root / args.output
    output_path.write_text(build_memo(validation), encoding="utf-8")
    print(f"Interpretation memo written: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
