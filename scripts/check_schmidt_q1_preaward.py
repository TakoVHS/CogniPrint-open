#!/usr/bin/env python3
"""Development-only gate for Schmidt Q1 pre-award scaffolding."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cogniprint.multi_principal_evidence import (  # noqa: E402
    structural_field_ablation,
    verify_multi_principal_bundle,
)


FIXTURE_DIR = ROOT / "challenge-schmidt-q1" / "fixtures"
FIXTURES = [
    FIXTURE_DIR / "synthetic-3-principal-happy-path.json",
    FIXTURE_DIR / "synthetic-4-principal-linear.json",
    FIXTURE_DIR / "synthetic-6-principal-linear.json",
]


def main() -> int:
    verified_counts: list[int] = []
    first_bundle: dict | None = None

    for fixture in FIXTURES:
        bundle = json.loads(fixture.read_text(encoding="utf-8"))
        if first_bundle is None:
            first_bundle = bundle
        result = verify_multi_principal_bundle(bundle)
        if not result.get("ok"):
            print(
                "SCHMIDT_Q1_PREAWARD_VERIFY=FAIL "
                f"fixture={fixture.name} reason={result.get('reason')}"
            )
            return 1
        verified_counts.append(int(result["principal_count"]))

    assert first_bundle is not None
    ablation = structural_field_ablation(first_bundle)
    if not ablation or not all(ablation.values()):
        print(f"SCHMIDT_Q1_PREAWARD_ABLATION=FAIL outcomes={json.dumps(ablation, sort_keys=True)}")
        return 1

    print("SCHMIDT_Q1_PREAWARD_VERIFY=PASS")
    print("SCHMIDT_Q1_PREAWARD_STRUCTURAL_ABLATION=PASS")
    print(f"SCHMIDT_Q1_PREAWARD_FIXTURE_COUNTS={','.join(map(str, verified_counts))}")
    print("SCHMIDT_Q1_SCIENTIFIC_MILESTONE=NOT_CLAIMED")
    print("RESEARCH_STATUS=DEVELOPMENT_ONLY_PREAWARD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
