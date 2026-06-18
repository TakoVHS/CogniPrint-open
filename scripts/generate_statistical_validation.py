#!/usr/bin/env python3
"""Generate the current descriptive statistical validation layer."""

from __future__ import annotations

import argparse
from pathlib import Path

from cogniprint.stats.validation import generate_statistical_validation


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate CogniPrint statistical validation outputs from existing empirical and benchmark artifacts.")
    parser.add_argument("--campaign-root", type=Path, default=Path("workspace/campaigns"), help="Directory containing campaign results.")
    parser.add_argument("--benchmark-samples", type=Path, default=Path("datasets/public-benchmark-v1/metadata/samples.csv"), help="Benchmark sample registry CSV.")
    parser.add_argument("--output-dir", type=Path, default=Path("evidence/statistical-validation-v1"), help="Output directory for validation artifacts.")
    args = parser.parse_args()
    output_dir = generate_statistical_validation(
        campaign_root=args.campaign_root.resolve(),
        benchmark_samples_csv=args.benchmark_samples.resolve(),
        output_dir=args.output_dir.resolve(),
    )
    print(f"Statistical validation outputs written: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
