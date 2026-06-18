"""Command-line interface for the CogniPrint local workstation."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .campaign import create_colleague_pack, generate_paper2_outputs, run_campaign, summarize_all_campaigns, summarize_campaign
from .core.analyzer import get_analyzer
from .core.profile_manager import ProfileManager
from .dataset import create_dataset_scaffold
from .experiment.runner import run_experiment
from .fingerprint import perturb_stability_test
from .perturbation import create_perturbation_lab
from .reporting.markdown import generate_aggregate_report, generate_markdown_report
from .reporting.notes import generate_empirical_notes
from .reporting.pdf import generate_pdf_report
from .stats.validation import generate_statistical_validation
from .study import collect_study_samples, create_study
from .validation import (
    generate_random_pair_distances,
    load_texts_from_dir,
    permutation_test_against_random,
    recommend_threshold,
    run_validation_suite,
)
from .workstation import collect_samples, create_run, ensure_workspace


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "handler"):
        parser.print_help()
        return 2
    return args.handler(args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cogniprint",
        description=(
            "CogniPrint local research workstation. Outputs are analytical signals "
            "for profile analysis, comparison, and reproducible experiment notes."
        ),
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path("workspace"),
        help="Workspace directory containing input, runs, reports, notes, exports, and studies.",
    )

    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init-workspace", help="Create the local research workspace directories.")
    init_parser.set_defaults(handler=_handle_init)

    run_parser = subparsers.add_parser("run", help="Analyze one or more text inputs and write a run bundle.")
    _add_input_args(run_parser)
    run_parser.add_argument("--label", help="Optional human-readable run label.")
    run_parser.add_argument("--run-id", help="Optional explicit run directory name for exact reproducibility.")
    run_parser.set_defaults(handler=_handle_run)

    compare_parser = subparsers.add_parser("compare", help="Compare a baseline text with one or more variants.")
    compare_parser.add_argument("--baseline-text", help="Inline baseline text.")
    compare_parser.add_argument("--baseline-file", type=Path, help="Baseline text file.")
    compare_parser.add_argument("--variant-text", action="append", default=[], help="Inline variant text. Repeatable.")
    compare_parser.add_argument("--variant-file", action="append", type=Path, default=[], help="Variant text file. Repeatable.")
    compare_parser.add_argument("--variant-folder", action="append", type=Path, default=[], help="Folder of variant text files. Repeatable.")
    compare_parser.add_argument(
        "--metric",
        choices=["all", "cosine", "euclidean", "manhattan", "mahalanobis", "wasserstein", "jensen-shannon"],
        default="all",
        help="Optional selected metric to highlight in comparison outputs.",
    )
    compare_parser.add_argument("--label", help="Optional human-readable run label.")
    compare_parser.add_argument("--run-id", help="Optional explicit run directory name for exact reproducibility.")
    compare_parser.set_defaults(handler=_handle_compare)

    study_parser = subparsers.add_parser("study", help="Run a named baseline-and-variants study with aggregated outputs.")
    study_parser.add_argument("--name", required=True, help="Human-readable study name.")
    study_parser.add_argument("--study-id", help="Optional explicit study directory name for scripted workflows.")
    study_parser.add_argument("--baseline-text", help="Inline baseline text.")
    study_parser.add_argument("--baseline-file", type=Path, help="Baseline text file.")
    study_parser.add_argument("--variant-text", action="append", default=[], help="Inline variant text. Repeatable.")
    study_parser.add_argument("--variant-file", action="append", type=Path, default=[], help="Variant text file. Repeatable.")
    study_parser.add_argument("--variant-folder", action="append", type=Path, default=[], help="Folder of variant text files. Repeatable.")
    study_parser.set_defaults(handler=_handle_study)

    profile_parser = subparsers.add_parser("profile", help="Compute one text profile and write JSON to stdout or file.")
    profile_sources = profile_parser.add_mutually_exclusive_group(required=True)
    profile_sources.add_argument("--text", help="Inline text to profile.")
    profile_sources.add_argument("--file", type=Path, help="Text file to profile.")
    profile_parser.add_argument("--output", "-o", type=Path, help="Optional JSON output path.")
    profile_parser.add_argument("--save", action="store_true", help="Also save the profile under workspace/profiles.")
    profile_parser.add_argument("--label", help="Label used when saving the profile.")
    profile_parser.add_argument("--similar-threshold", type=float, help="Find saved profiles at or above this cosine similarity.")
    profile_parser.set_defaults(handler=_handle_profile)

    corpus_parser = subparsers.add_parser("corpus", help="Batch profile a directory of text files.")
    corpus_parser.add_argument("--input-dir", type=Path, required=True, help="Directory containing text files.")
    corpus_parser.add_argument("--output-dir", type=Path, default=None, help="Directory for per-file JSON profile artifacts.")
    corpus_parser.add_argument("--pattern", default="*.txt", help="Glob pattern for input files.")
    corpus_parser.set_defaults(handler=_handle_corpus)

    report_parser = subparsers.add_parser("report", help="Generate a human-readable report from a study directory.")
    report_parser.add_argument("--study-dir", type=Path, required=True, help="Study artifact directory.")
    report_parser.add_argument("--format", choices=["md", "pdf"], default="md", help="Report output format.")
    report_parser.add_argument("--output", "-o", type=Path, help="Report output path.")
    report_parser.add_argument("--aggregate", action="store_true", help="Treat --study-dir as a directory of studies and write an aggregate report.")
    report_parser.add_argument("--csv-output", type=Path, help="Optional aggregate CSV output path.")
    report_parser.set_defaults(handler=_handle_report)

    experiment_parser = subparsers.add_parser("experiment", help="Run YAML-configured experiment workflows.")
    experiment_subparsers = experiment_parser.add_subparsers(dest="experiment_command")
    experiment_run_parser = experiment_subparsers.add_parser("run", help="Run an experiment from a YAML config file.")
    experiment_run_parser.add_argument("--config", type=Path, required=True, help="YAML experiment configuration file.")
    experiment_run_parser.set_defaults(handler=_handle_experiment_run)

    perturb_parser = subparsers.add_parser("perturb", help="Run a perturbation lab study from baseline and variants.")
    perturb_parser.add_argument("--name", required=True, help="Human-readable perturbation study name.")
    perturb_parser.add_argument("--perturbation-id", help="Optional explicit perturbation output directory name.")
    perturb_parser.add_argument("--baseline-file", type=Path, required=True, help="Baseline text file.")
    perturb_parser.add_argument("--light-file", type=Path, help="Lightly edited variant file.")
    perturb_parser.add_argument("--strong-file", type=Path, help="Strongly edited variant file.")
    perturb_parser.add_argument("--variant-file", action="append", type=Path, default=[], help="Additional variant file. Repeatable.")
    perturb_parser.add_argument("--variant-folder", type=Path, help="Folder of additional variants.")
    perturb_parser.set_defaults(handler=_handle_perturb)

    stability_parser = subparsers.add_parser(
        "stability-test",
        help="Compare one baseline file against a folder of controlled perturbation variants.",
    )
    stability_parser.add_argument("--baseline-file", type=Path, required=True, help="Baseline text file.")
    stability_parser.add_argument("--perturbed-folder", type=Path, required=True, help="Folder containing perturbation variant files.")
    stability_parser.add_argument("--pattern", default="*.txt", help="Glob pattern for variant files.")
    stability_parser.add_argument("--metric", choices=["cosine", "euclidean"], default="cosine", help="Distance metric for the stability summary.")
    stability_parser.add_argument(
        "--threshold",
        type=float,
        default=None,
        help="Optional exploratory mean-distance threshold. No default fixed threshold is validated.",
    )
    stability_parser.add_argument("--permutation-n", type=int, default=0, help="Random-pair draws for an optional empirical permutation contrast.")
    stability_parser.add_argument("--corpus-dir", type=Path, help="Directory with .txt files for random-pair contrasts.")
    stability_parser.add_argument("--seed", type=int, default=42, help="Random seed for optional permutation contrasts.")
    stability_parser.add_argument("--output", "-o", type=Path, help="Optional JSON output path.")
    stability_parser.set_defaults(handler=_handle_stability_test)

    validate_parser = subparsers.add_parser(
        "validate",
        help="Run a reviewer-facing validation dry-run with baselines and random-pair contrasts.",
    )
    validate_parser.add_argument("--corpus-dir", type=Path, required=True, help="Directory with .txt files for random-pair contrasts.")
    validate_parser.add_argument("--campaign-dir", type=Path, required=True, help="Campaign input folder containing original.txt and variants/.")
    validate_parser.add_argument("--pattern", default="*.txt", help="Glob pattern for campaign variant files.")
    validate_parser.add_argument("--metric", choices=["cosine", "euclidean"], default="cosine", help="Fingerprint distance metric.")
    validate_parser.add_argument("--n-permutations", type=int, default=1000, help="Number of random text pairs for permutation contrasts.")
    validate_parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility.")
    validate_parser.add_argument("--output", type=Path, default=Path("validation/inferential-v1/reviewer-validation-report.json"), help="Output JSON report path.")
    validate_parser.set_defaults(handler=_handle_validate)

    notes_parser = subparsers.add_parser("notes", help="Generate empirical manuscript notes from a study directory.")
    notes_parser.add_argument("--study-dir", type=Path, required=True, help="Study artifact directory.")
    notes_parser.add_argument("--output-dir", type=Path, help="Output directory for generated note files.")
    notes_parser.set_defaults(handler=_handle_notes)

    dataset_parser = subparsers.add_parser("dataset", help="Create a lightweight dataset scaffold.")
    dataset_parser.add_argument("--name", required=True, help="Dataset name.")
    dataset_parser.add_argument("--description", help="Short dataset description.")
    dataset_parser.add_argument("--baseline-file", action="append", type=Path, default=[], help="Baseline/source sample file. Repeatable.")
    dataset_parser.add_argument("--variant-file", action="append", type=Path, default=[], help="Variant sample file. Repeatable.")
    dataset_parser.add_argument("--sources-file", type=Path, help="Optional source metadata file to copy into dataset metadata.")
    dataset_parser.set_defaults(handler=_handle_dataset)

    campaign_parser = subparsers.add_parser("campaign", help="Run or summarize empirical campaigns.")
    campaign_subparsers = campaign_parser.add_subparsers(dest="campaign_command")
    campaign_run_parser = campaign_subparsers.add_parser("run", help="Run a campaign from a YAML config.")
    campaign_run_parser.add_argument("--config", type=Path, required=True, help="YAML campaign configuration file.")
    campaign_run_parser.set_defaults(handler=_handle_campaign_run)
    campaign_summary_parser = campaign_subparsers.add_parser("summarize", help="Regenerate campaign synthesis outputs.")
    campaign_summary_parser.add_argument("--campaign-dir", type=Path, required=True, help="Campaign directory.")
    campaign_summary_parser.set_defaults(handler=_handle_campaign_summarize)
    campaign_all_parser = campaign_subparsers.add_parser("summarize-all", help="Summarize all campaign directories into multi-campaign artifacts.")
    campaign_all_parser.add_argument("--campaign-root", type=Path, help="Directory containing campaign directories. Defaults to workspace/campaigns.")
    campaign_all_parser.set_defaults(handler=_handle_campaign_summarize_all)
    campaign_share_parser = campaign_subparsers.add_parser("share-pack", help="Build a compact colleague-facing pack from one real campaign.")
    campaign_share_parser.add_argument("--campaign-dir", type=Path, required=True, help="Campaign directory to package.")
    campaign_share_parser.add_argument("--output-dir", type=Path, default=Path("workspace/share/colleague-pack-001"), help="Output directory for the share pack.")
    campaign_share_parser.add_argument("--dataset-dir", type=Path, help="Optional dataset directory or dataset-manifest.json to include.")
    campaign_share_parser.set_defaults(handler=_handle_campaign_share_pack)
    campaign_paper2_parser = campaign_subparsers.add_parser("paper2", help="Generate paper-2 drafting outputs from real campaigns.")
    campaign_paper2_parser.add_argument("--campaign-root", type=Path, help="Directory containing campaign directories. Defaults to workspace/campaigns.")
    campaign_paper2_parser.add_argument("--output-dir", type=Path, default=Path("workspace/reports/paper-2"), help="Output directory for paper-2 drafts.")
    campaign_paper2_parser.set_defaults(handler=_handle_campaign_paper2)

    stats_parser = subparsers.add_parser("stats", help="Generate statistical validation outputs from existing artifacts.")
    stats_subparsers = stats_parser.add_subparsers(dest="stats_command")
    stats_validate_parser = stats_subparsers.add_parser("validate", help="Build descriptive statistical validation outputs.")
    stats_validate_parser.add_argument("--campaign-root", type=Path, default=Path("workspace/campaigns"), help="Directory containing campaign directories.")
    stats_validate_parser.add_argument("--benchmark-samples", type=Path, default=Path("datasets/public-benchmark-v1/metadata/samples.csv"), help="Benchmark sample registry CSV.")
    stats_validate_parser.add_argument("--output-dir", type=Path, default=Path("evidence/statistical-validation-v1"), help="Output directory for validation artifacts.")
    stats_validate_parser.set_defaults(handler=_handle_stats_validate)

    return parser


def _add_input_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--text", action="append", default=[], help="Inline text input. Repeatable.")
    parser.add_argument("--file", action="append", type=Path, default=[], help="Text file input. Repeatable.")
    parser.add_argument("--folder", action="append", type=Path, default=[], help="Folder of text files. Repeatable.")


def _handle_init(args: argparse.Namespace) -> int:
    ensure_workspace(args.workspace)
    print(f"Workspace ready: {args.workspace.resolve()}")
    return 0


def _handle_run(args: argparse.Namespace) -> int:
    samples = collect_samples(texts=args.text, files=args.file, folders=args.folder)
    run_dir = create_run(
        samples=samples,
        workspace=args.workspace,
        command_name="run",
        run_label=args.label,
        run_id=args.run_id,
        cli_args=vars(args),
    )
    print(f"Run bundle written: {run_dir.resolve()}")
    return 0


def _handle_compare(args: argparse.Namespace) -> int:
    baseline_sources = [source for source in [args.baseline_text, args.baseline_file] if source]
    if len(baseline_sources) != 1:
        raise SystemExit("Provide exactly one baseline input with --baseline-text or --baseline-file.")

    baseline = collect_samples(
        texts=[args.baseline_text] if args.baseline_text else [],
        files=[args.baseline_file] if args.baseline_file else [],
    )
    variants = collect_samples(texts=args.variant_text, files=args.variant_file, folders=args.variant_folder)
    if not variants:
        raise SystemExit("Provide at least one variant with --variant-text, --variant-file, or --variant-folder.")
    run_dir = create_run(
        samples=baseline + variants,
        workspace=args.workspace,
        command_name="compare",
        run_label=args.label,
        run_id=args.run_id,
        baseline_index=0,
        cli_args=vars(args),
        metric=args.metric,
    )
    print(f"Comparison bundle written: {run_dir.resolve()}")
    return 0


def _handle_study(args: argparse.Namespace) -> int:
    try:
        baseline, variants = collect_study_samples(
            baseline_text=args.baseline_text,
            baseline_file=args.baseline_file,
            variant_texts=args.variant_text,
            variant_files=args.variant_file,
            variant_folders=args.variant_folder,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    study_dir = create_study(
        workspace=args.workspace,
        name=args.name,
        study_id=args.study_id,
        baseline=baseline,
        variants=variants,
        cli_args=vars(args),
    )
    print(f"Study bundle written: {study_dir.resolve()}")
    return 0


def _handle_profile(args: argparse.Namespace) -> int:
    text = args.text if args.text is not None else args.file.read_text(encoding="utf-8")
    payload = get_analyzer().analyze(text)
    payload["source"] = {"type": "inline" if args.text is not None else "file", "ref": "inline" if args.text is not None else str(args.file)}
    if args.save:
        manager = ProfileManager(args.workspace / "profiles")
        label = args.label or (args.file.stem if args.file else "profile")
        saved_path = manager.save(payload, label)
        payload["saved_profile"] = str(saved_path)
    if args.similar_threshold is not None:
        manager = ProfileManager(args.workspace / "profiles")
        payload["similar_profiles"] = manager.find_similar(payload["fingerprint_vector"], args.similar_threshold)
    output = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"Profile JSON written: {args.output.resolve()}")
    else:
        print(output, end="")
    return 0


def _handle_corpus(args: argparse.Namespace) -> int:
    input_dir = args.input_dir.expanduser().resolve()
    if not input_dir.is_dir():
        raise SystemExit(f"Input directory not found: {input_dir}")
    output_dir = args.output_dir or (args.workspace / "corpus" / input_dir.name)
    output_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(path for path in input_dir.glob(args.pattern) if path.is_file())
    analyzer = get_analyzer()
    results = analyzer.analyze_batch([path.read_text(encoding="utf-8") for path in files])
    for path, payload in zip(files, results):
        payload["source"] = {"type": "file", "ref": str(path.resolve()), "name": path.name}
        out_path = output_dir / f"{path.stem}.profile.json"
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = {
        "input_dir": str(input_dir),
        "output_dir": str(output_dir.resolve()),
        "pattern": args.pattern,
        "file_count": len(files),
        "files": [str(path.resolve()) for path in files],
    }
    (output_dir / "corpus-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Corpus profiles written: {output_dir.resolve()} ({len(files)} files)")
    return 0


def _handle_report(args: argparse.Namespace) -> int:
    study_dir = args.study_dir.expanduser().resolve()
    if not study_dir.is_dir():
        raise SystemExit(f"Study directory not found: {study_dir}")
    if args.aggregate:
        output = args.output or Path("workspace/reports/aggregate-study-summary.md")
        generate_aggregate_report(study_dir, output, args.csv_output)
        print(f"Aggregate report written: {output.resolve()}")
        return 0
    output = args.output or Path(f"{study_dir.name}-report.{args.format}")
    if args.format == "md":
        generate_markdown_report(study_dir, output)
    else:
        generate_pdf_report(study_dir, output)
    print(f"Report written: {output.resolve()}")
    return 0


def _handle_experiment_run(args: argparse.Namespace) -> int:
    payload = _load_yaml(args.config)
    experiment_dir = run_experiment(payload, config_path=args.config.expanduser().resolve(), workspace=args.workspace)
    print(f"Experiment written: {experiment_dir.resolve()}")
    return 0


def _handle_perturb(args: argparse.Namespace) -> int:
    lab_dir = create_perturbation_lab(
        workspace=args.workspace,
        name=args.name,
        lab_id=args.perturbation_id,
        baseline_file=args.baseline_file,
        light_file=args.light_file,
        strong_file=args.strong_file,
        variant_files=args.variant_file,
        variant_folder=args.variant_folder,
        cli_args=vars(args),
    )
    print(f"Perturbation lab written: {lab_dir.resolve()}")
    return 0


def _handle_stability_test(args: argparse.Namespace) -> int:
    baseline_file = args.baseline_file.expanduser().resolve()
    perturbed_folder = args.perturbed_folder.expanduser().resolve()
    if not baseline_file.is_file():
        raise SystemExit(f"Baseline file not found: {baseline_file}")
    if not perturbed_folder.is_dir():
        raise SystemExit(f"Perturbed folder not found: {perturbed_folder}")

    variant_files = sorted(path for path in perturbed_folder.glob(args.pattern) if path.is_file())
    if not variant_files:
        raise SystemExit(f"No perturbed files matched {args.pattern!r} in {perturbed_folder}")

    payload = perturb_stability_test(
        baseline_file.read_text(encoding="utf-8"),
        [path.read_text(encoding="utf-8") for path in variant_files],
        metric=args.metric,
        threshold=args.threshold,
    )
    payload.update(
        {
            "baseline_file": str(baseline_file),
            "perturbed_folder": str(perturbed_folder),
            "variant_files": [str(path) for path in variant_files],
        }
    )
    if args.permutation_n:
        if args.corpus_dir is None:
            raise SystemExit("--corpus-dir is required when --permutation-n is greater than 0.")
        corpus_texts = [text for _, text in load_texts_from_dir(args.corpus_dir)]
        random_distances = generate_random_pair_distances(
            corpus_texts,
            metric=args.metric,
            n_pairs=args.permutation_n,
            seed=args.seed,
        )
        p_values = [
            permutation_test_against_random(distance, random_distances, alternative="less")
            for distance in payload["distances"]
        ]
        payload["permutation_test"] = {
            "alternative": "less",
            "n_random_pairs": len(random_distances),
            "seed": args.seed,
            "p_values_plus_one": [round(value, 6) for value in p_values],
            "all_p_less_0_05": all(value < 0.05 for value in p_values),
            "threshold_recommendation": recommend_threshold(payload["distances"], random_distances),
            "random_distances_sample": [round(value, 6) for value in random_distances[:10]],
        }
    output = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"Stability summary written: {args.output.resolve()}")
    else:
        print(output, end="")
    return 0


def _handle_validate(args: argparse.Namespace) -> int:
    campaign_dir = args.campaign_dir.expanduser().resolve()
    original_path = campaign_dir / "original.txt"
    variants_dir = campaign_dir / "variants"
    if not original_path.is_file():
        raise SystemExit(f"Campaign original.txt not found: {original_path}")
    if not variants_dir.is_dir():
        raise SystemExit(f"Campaign variants directory not found: {variants_dir}")
    variant_files = sorted(path for path in variants_dir.glob(args.pattern) if path.is_file())
    if not variant_files:
        raise SystemExit(f"No campaign variants matched {args.pattern!r} in {variants_dir}")
    corpus_rows = load_texts_from_dir(args.corpus_dir)
    report = run_validation_suite(
        corpus_texts=[text for _, text in corpus_rows],
        original_text=original_path.read_text(encoding="utf-8"),
        variant_texts=[path.read_text(encoding="utf-8") for path in variant_files],
        variant_labels=[path.name for path in variant_files],
        metric=args.metric,
        n_permutations=args.n_permutations,
        seed=args.seed,
    )
    report.update(
        {
            "campaign_dir": _display_path(campaign_dir),
            "corpus_dir": _display_path(args.corpus_dir.expanduser().resolve()),
            "corpus_file_count": len(corpus_rows),
            "variant_files": [_display_path(path) for path in variant_files],
        }
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    pvalues_csv = args.output.with_name(args.output.stem + "-pvalues.csv")
    summary_csv = args.output.with_name(args.output.stem + "-summary.csv")
    _write_validation_pvalues_csv(pvalues_csv, report)
    _write_validation_summary_csv(summary_csv, report)
    summary = report["perturbation_distance_summary"]
    threshold = report["threshold_recommendation"]
    print(f"Validation dry-run report written: {args.output.resolve()}")
    print(f"Validation p-values CSV written: {pvalues_csv.resolve()}")
    print(f"Validation summary CSV written: {summary_csv.resolve()}")
    print(f"Mean perturbation distance: {summary['mean']}")
    print(f"Recommended threshold: {threshold['recommended_threshold']}")
    print("Readiness remains descriptive_only.")
    return 0


def _write_validation_pvalues_csv(path: Path, report: dict) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "variant_label",
                "fingerprint_distance",
                "permutation_p_less_plus_one",
                "significant_at_alpha_0_05",
                "tfidf_cosine_similarity",
                "random_vector_similarity",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        for row in report["variant_results"]:
            writer.writerow({field: row.get(field) for field in writer.fieldnames})


def _write_validation_summary_csv(path: Path, report: dict) -> None:
    rows = [
        ("readiness_boundary", report["readiness_boundary"]),
        ("external_review_gate_satisfied", report["external_review_gate_satisfied"]),
        ("metric", report["metric"]),
        ("n_perturbation_pairs", report["n_perturbation_pairs"]),
        ("n_random_pairs", report["n_random_pairs"]),
        ("perturbation_mean", report["perturbation_distance_summary"]["mean"]),
        ("perturbation_std", report["perturbation_distance_summary"]["std"]),
        ("random_mean", report["random_distance_summary"]["mean"]),
        ("random_std", report["random_distance_summary"]["std"]),
        ("effect_size_cohens_d_random_vs_perturbation", report["effect_size_cohens_d_random_vs_perturbation"]),
        ("required_sample_size_for_power_0_8", report["required_sample_size_for_power_0_8"]),
        ("recommended_threshold", report["threshold_recommendation"]["recommended_threshold"]),
        ("recommended_threshold_fpr", report["threshold_recommendation"]["fpr_at_threshold"]),
        ("recommended_threshold_power", report["threshold_recommendation"]["power_at_threshold"]),
        ("fixed_threshold_0_15_fpr", report["fixed_threshold_0_15_evaluation"]["fpr_at_threshold"]),
        ("fixed_threshold_0_15_power", report["fixed_threshold_0_15_evaluation"]["power_at_threshold"]),
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["metric", "value"])
        writer.writerows(rows)


def _display_path(path: Path) -> str:
    resolved = path.expanduser().resolve()
    try:
        return resolved.relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return str(resolved)


def _handle_notes(args: argparse.Namespace) -> int:
    study_dir = args.study_dir.expanduser().resolve()
    if not study_dir.is_dir():
        raise SystemExit(f"Study directory not found: {study_dir}")
    output_dir = args.output_dir or Path("workspace/reports") / study_dir.name
    generate_empirical_notes(study_dir, output_dir)
    print(f"Empirical notes written: {output_dir.resolve()}")
    return 0


def _handle_dataset(args: argparse.Namespace) -> int:
    dataset_dir = create_dataset_scaffold(
        workspace=args.workspace,
        name=args.name,
        description=args.description,
        baseline_files=args.baseline_file,
        variant_files=args.variant_file,
        sources_file=args.sources_file,
    )
    print(f"Dataset scaffold written: {dataset_dir.resolve()}")
    return 0


def _handle_campaign_run(args: argparse.Namespace) -> int:
    payload = _load_yaml(args.config)
    campaign_dir = run_campaign(payload, config_path=args.config.expanduser().resolve(), workspace=args.workspace)
    print(f"Campaign written: {campaign_dir.resolve()}")
    return 0


def _handle_campaign_summarize(args: argparse.Namespace) -> int:
    campaign_dir = args.campaign_dir.expanduser().resolve()
    if not campaign_dir.is_dir():
        raise SystemExit(f"Campaign directory not found: {campaign_dir}")
    summarize_campaign(campaign_dir)
    print(f"Campaign summary written: {campaign_dir.resolve()}")
    return 0


def _handle_campaign_summarize_all(args: argparse.Namespace) -> int:
    campaign_root = args.campaign_root.expanduser().resolve() if args.campaign_root else None
    output = summarize_all_campaigns(workspace=args.workspace, campaign_root=campaign_root)
    print(f"Multi-campaign summary written: {output.resolve()}")
    return 0


def _handle_campaign_share_pack(args: argparse.Namespace) -> int:
    output = create_colleague_pack(
        campaign_dir=args.campaign_dir.expanduser().resolve(),
        output_dir=args.output_dir,
        dataset_dir=args.dataset_dir.expanduser().resolve() if args.dataset_dir else None,
    )
    print(f"Colleague share pack written: {output.resolve()}")
    return 0


def _handle_campaign_paper2(args: argparse.Namespace) -> int:
    campaign_root = args.campaign_root.expanduser().resolve() if args.campaign_root else None
    output = generate_paper2_outputs(workspace=args.workspace, campaign_root=campaign_root, output_dir=args.output_dir)
    print(f"Paper-2 drafting outputs written: {output.resolve()}")
    return 0


def _handle_stats_validate(args: argparse.Namespace) -> int:
    output = generate_statistical_validation(
        campaign_root=args.campaign_root.expanduser().resolve(),
        benchmark_samples_csv=args.benchmark_samples.expanduser().resolve(),
        output_dir=args.output_dir.expanduser().resolve(),
    )
    print(f"Statistical validation outputs written: {output.resolve()}")
    return 0


def _load_yaml(path: Path) -> dict:
    try:
        import yaml
    except ImportError as exc:
        raise SystemExit("PyYAML is required for experiment configs. Run `pip install -e .`.") from exc
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)
    if not isinstance(payload, dict):
        raise SystemExit("Experiment config must be a YAML mapping.")
    return payload
