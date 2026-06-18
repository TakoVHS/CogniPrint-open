#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


def require(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    dashboard = root.parent / "TakoVHS.github.io" / "evidence" / "dashboard.html"
    if not dashboard.exists():
        print(f"Evidence dashboard check failed:\n- missing dashboard file: {dashboard}")
        return 1

    text = dashboard.read_text(encoding="utf-8")
    errors: list[str] = []

    require(errors, "Evidence Visibility Dashboard" in text, "dashboard title heading is missing")
    require(errors, "descriptive_only" in text, "dashboard is missing current readiness decision")
    require(errors, ">311<" in text and "combined readiness rows" in text, "dashboard is missing combined readiness count 311")
    require(errors, ">0/1<" in text and "valid external reviews recorded" in text, "dashboard is missing external review gate 0/1")
    require(errors, ">5<" in text and "controlled perturbation campaigns" in text, "dashboard is missing empirical campaign count 5")
    require(errors, ">41<" in text and "local campaign comparison rows" in text, "dashboard is missing local empirical comparison row count 41")
    require(errors, ">11<" in text and "campaign-004 comparison rows" in text, "dashboard is missing campaign-004 row count 11")
    require(errors, ">20<" in text and "released benchmark baselines" in text, "dashboard is missing benchmark v1.1 baseline count 20")
    require(errors, ">120<" in text and "released benchmark variants" in text, "dashboard is missing benchmark v1.1 variant count 120")
    require(errors, ">50<" in text and "independent holdout rows" in text, "dashboard is missing independent holdout count 50")
    require(errors, "wave-005 validation" in text.casefold(), "dashboard is missing wave-005 validation wording")
    require(errors, "multiple-comparison correction" in text.casefold(), "dashboard is missing validation v1.2 wording")
    require(errors, "descriptive" in text.casefold(), "dashboard is missing descriptive framing")
    require(errors, "working empirical evidence package supporting a follow-up manuscript" in text, "dashboard is missing core research framing")
    require(errors, "/styles.css" in text, "dashboard is missing stylesheet link")
    require(errors, "https://github.com/TakoVHS/CogniPrint/tree/main/evidence/empirical-v1" in text, "dashboard is missing empirical snapshot link")
    require(errors, "https://github.com/TakoVHS/CogniPrint/tree/main/evidence/public-benchmark-v1.1" in text, "dashboard is missing public benchmark v1.1 link")
    require(errors, "https://github.com/TakoVHS/CogniPrint/tree/main/evidence/independent-holdout-v1" in text, "dashboard is missing holdout link")
    require(errors, "https://github.com/TakoVHS/CogniPrint/tree/main/validation/wave005-descriptive-validation" in text, "dashboard is missing wave005 validation link")

    if errors:
        print("Evidence dashboard check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Evidence dashboard check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
