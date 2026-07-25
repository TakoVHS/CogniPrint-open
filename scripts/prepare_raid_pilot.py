#!/usr/bin/env python3
"""Prepare a balanced metadata-only CogniPrint pilot from the RAID dataset."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cogniprint.benchmarks.raid import RaidPilotConfig, collect_records, count_cells
from cogniprint.fingerprint import FINGERPRINT_VERSION


DATASET_ID = "liamdugan/raid"
SOURCE_URL = "https://huggingface.co/datasets/liamdugan/raid"
SOURCE_PAPER = "https://aclanthology.org/2024.acl-long.674/"


def parse_csv(value: str) -> tuple[str, ...]:
    items = tuple(item.strip().lower() for item in value.split(",") if item.strip())
    if not items:
        raise argparse.ArgumentTypeError("expected at least one comma-separated value")
    return items


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", default="train")
    parser.add_argument("--revision", default="main", help="Hugging Face dataset revision; pin when publishing evidence")
    parser.add_argument("--models", type=parse_csv, default=None)
    parser.add_argument("--domains", type=parse_csv, default=None)
    parser.add_argument("--per-cell", type=int, default=25)
    parser.add_argument("--seed", type=int, default=20260725)
    parser.add_argument("--shuffle-buffer", type=int, default=10_000)
    parser.add_argument("--max-scanned", type=int, default=None)
    parser.add_argument("--output-dir", type=Path, default=Path("evidence/model-fingerprint-m1/raid-pilot"))
    args = parser.parse_args()

    if args.per_cell <= 0:
        parser.error("--per-cell must be positive")

    config_kwargs = {"per_cell": args.per_cell}
    if args.models is not None:
        config_kwargs["models"] = args.models
    if args.domains is not None:
        config_kwargs["domains"] = args.domains
    config = RaidPilotConfig(**config_kwargs)

    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise SystemExit("Install the real-data extra first: pip install -e '.[real-data]'") from exc

    stream = load_dataset(DATASET_ID, split=args.split, revision=args.revision, streaming=True)
    stream = stream.shuffle(seed=args.seed, buffer_size=args.shuffle_buffer)
    records, scanned = collect_records(stream, config, max_scanned=args.max_scanned)

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    records_path = output_dir / "features.jsonl"
    summary_path = output_dir / "summary.json"

    with records_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    summary = {
        "dataset_id": DATASET_ID,
        "dataset_revision": args.revision,
        "dataset_license": "MIT",
        "source_url": SOURCE_URL,
        "source_paper": SOURCE_PAPER,
        "split": args.split,
        "seed": args.seed,
        "shuffle_buffer": args.shuffle_buffer,
        "scanned_rows": scanned,
        "released_raw_text": False,
        "released_raw_prompts": False,
        "fingerprint_version": FINGERPRINT_VERSION,
        "readiness_boundary": "descriptive_only",
        "selection": {
            "models": list(config.models),
            "domains": list(config.domains),
            "per_cell": config.per_cell,
            "model_decoding": config.model_decoding,
            "repetition_penalty": config.repetition_penalty,
            "language": config.language,
            "attack": "none",
        },
        "record_count": len(records),
        "cell_counts": count_cells(records),
        "notes": [
            "This pilot emits features and hashes, not RAID source text.",
            "The default first pilot is English-only because CogniPrint v2 tokenization has not been validated for Czech/German diacritics.",
            "Pin --revision to an immutable dataset revision before citing a final result.",
            "No model-origin or authorship claim follows from this feature export alone.",
        ],
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"wrote {len(records)} records after scanning {scanned} RAID rows")
    print(records_path)
    print(summary_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
