"""Stage-A RAID development screen for known-membership certificates.

DEVELOPMENT ONLY. RAID is already exposed to the research process.
No output from this script is confirmatory and no numeric result may be used to
set a future confirmatory protocol.

The screen asks whether a standard lexical detector yields certificate lift
above the mandatory accept-all reference. It uses source-group-disjoint roles,
a fixed decoding regime, exact one-sided Clopper-Pearson bounds, and Bonferroni
control over the complete threshold x stratum family.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cogniprint.stats.evidence_bounded import (  # noqa: E402
    clopper_pearson_lower,
    clopper_pearson_upper,
)

DEFAULT_FAMILIES = (
    "human,chatgpt,gpt4,cohere-chat,llama-chat,mistral-chat,mpt-chat"
)
DEFAULT_DOMAINS = "abstracts,books,news,poetry,recipes,reddit,reviews,wiki"
DEFAULT_THRESHOLDS = "0,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,0.99"
DEFAULT_PI_GRID = "0.10,0.20,0.30,0.50"
DEFAULT_LK_FLOORS = "0.10,0.30,0.50,0.70"
ROLE_FRACTIONS = (("train", 0.50), ("certificate", 0.30), ("test", 0.20))


def h64(*parts: str) -> int:
    digest = hashlib.sha256("\x1f".join(parts).encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


def role_of(seed: str, group: str) -> str:
    u = h64(seed, "role", group) / 2.0**64
    acc = 0.0
    for name, frac in ROLE_FRACTIONS:
        acc += frac
        if u < acc:
            return name
    return ROLE_FRACTIONS[-1][0]


def group_of(row: dict[str, str]) -> str:
    source_id = str(row.get("source_id") or row.get("id") or "")
    return f"{row.get('domain','')}\x1f{source_id}"


def open_rows(path: Path):
    csv.field_size_limit(min(sys.maxsize, 2**31 - 1))
    with path.open("r", encoding="utf-8", newline="") as handle:
        yield from csv.DictReader(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_no_penalty(value: str | None) -> bool:
    if value is None:
        return True
    v = str(value).strip().lower()
    return v in ("", "no", "none", "false", "1", "1.0")


def keep_row(
    row: dict[str, str],
    families: set[str],
    domains: set[str],
    *,
    decoding: str,
) -> bool:
    family = row.get("model")
    if family not in families or row.get("domain") not in domains:
        return False
    attack = str(row.get("attack") or "none").strip().lower()
    if attack not in ("", "none") or not row.get("generation"):
        return False
    if family == "human":
        return True
    return (
        str(row.get("decoding") or "").strip().lower() == decoding
        and _is_no_penalty(row.get("repetition_penalty"))
    )


def load_records(
    path: Path,
    families: list[str],
    domains: list[str],
    per_family: int,
    seed: str,
    decoding: str,
) -> list[dict[str, str]]:
    fam, dom = set(families), set(domains)
    groups: dict[str, set[str]] = {f: set() for f in families}

    for row in open_rows(path):
        if keep_row(row, fam, dom, decoding=decoding):
            groups[row["model"]].add(group_of(row))

    common = set.intersection(*(groups[f] for f in families))
    ordered = sorted(common, key=lambda g: h64(seed, "group", g))
    selected = set(ordered[:per_family])
    if len(selected) < per_family:
        raise ValueError(
            f"requested {per_family} common source groups but only "
            f"{len(selected)} are available"
        )

    best: dict[tuple[str, str], tuple[int, dict[str, str]]] = {}
    for row in open_rows(path):
        if not keep_row(row, fam, dom, decoding=decoding):
            continue
        f, g = row["model"], group_of(row)
        if g not in selected:
            continue
        key = h64(seed, "row", str(row.get("id") or ""))
        if (f, g) not in best or key < best[(f, g)][0]:
            best[(f, g)] = (
                key,
                {
                    "family": f,
                    "group": g,
                    "domain": str(row.get("domain") or ""),
                    "text": row["generation"],
                },
            )

    records = [rec for _, rec in best.values()]
    expected = len(families) * per_family
    if len(records) != expected:
        raise ValueError(f"expected {expected} selected rows, got {len(records)}")
    for rec in records:
        rec["role"] = role_of(seed, rec["group"])
    records.sort(key=lambda r: (r["family"], h64(seed, "order", r["group"])))
    return records


def gate_counts(probs, thresholds):
    import numpy as np

    top = probs.max(axis=1) if len(probs) else np.zeros(0)
    return {t: int((top >= t).sum()) for t in thresholds}, int(len(top))


def certificate_risk(pi_u: float, l_k: float, u_u: float) -> float | None:
    den = (1.0 - pi_u) * l_k + pi_u * u_u
    if den <= 0.0:
        return None
    return pi_u * u_u / den


def break_even(delta: float, l_k: float, u_u: float) -> float | None:
    den = u_u * (1.0 - delta) + delta * l_k
    if den <= 0.0:
        return None
    return min(1.0, delta * l_k / den)


def certify(
    known_counts,
    unknown_counts,
    thresholds,
    alpha,
    delta,
    pi_grid,
    lk_floors,
):
    nonzero = [t for t in thresholds if t > 0]
    n_bounds = len(nonzero) * (len(known_counts) + len(unknown_counts))
    tail = alpha / n_bounds if n_bounds else alpha
    rows = []

    for t in thresholds:
        if t == 0:
            per_known = {k: 1.0 for k in known_counts}
            per_unknown = {u: 1.0 for u in unknown_counts}
        else:
            per_known = {}
            for k, (acc, n) in known_counts.items():
                lb = clopper_pearson_lower(acc[t], n, tail)
                per_known[k] = 0.0 if lb is None else lb
            per_unknown = {}
            for u, (acc, n) in unknown_counts.items():
                ub = clopper_pearson_upper(acc[t], n, tail)
                per_unknown[u] = 1.0 if ub is None else ub

        l_k = min(per_known.values())
        u_u = max(per_unknown.values())
        pe = break_even(delta, l_k, u_u)
        rows.append(
            {
                "tau": t,
                "L_K": l_k,
                "U_U": u_u,
                "known_point_acceptance": {
                    k: acc[t] / n if n else None
                    for k, (acc, n) in known_counts.items()
                },
                "unknown_point_acceptance": {
                    u: acc[t] / n if n else None
                    for u, (acc, n) in unknown_counts.items()
                },
                "break_even_pi": pe,
                "lift": None if pe is None else pe / delta,
                "B_by_pi": {
                    str(p): certificate_risk(p, l_k, u_u) for p in pi_grid
                },
            }
        )

    decisions = {}
    for p in pi_grid:
        passing = [
            r for r in rows
            if r["tau"] > 0
            and r["B_by_pi"][str(p)] is not None
            and r["B_by_pi"][str(p)] <= delta
            and r["B_by_pi"][str(p)] < p
        ]
        if passing:
            best = max(passing, key=lambda r: (r["L_K"], -r["B_by_pi"][str(p)]))
            decisions[str(p)] = {
                "decision": "PROMOTE",
                "tau": best["tau"],
                "L_K": best["L_K"],
                "U_U": best["U_U"],
                "B": best["B_by_pi"][str(p)],
            }
        elif p <= delta:
            decisions[str(p)] = {"decision": "PROMOTE_TRIVIAL"}
        else:
            decisions[str(p)] = {"decision": "ABSTAIN"}

    lift_by_floor = {}
    for floor in lk_floors:
        values = [
            r["lift"] for r in rows
            if r["tau"] > 0 and r["L_K"] >= floor and r["lift"] is not None
        ]
        lift_by_floor[str(floor)] = max(values) if values else None

    return {
        "n_bounds": n_bounds,
        "per_bound_tail": tail,
        "thresholds": rows,
        "decisions": decisions,
        "best_lift_any_gate": max(
            (r["lift"] for r in rows if r["tau"] > 0 and r["lift"] is not None),
            default=None,
        ),
        "best_lift_by_LK_floor": lift_by_floor,
    }


def fit_detector(texts, labels, max_features: int, C: float):
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression

    vec = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=2,
        max_features=max_features,
        sublinear_tf=True,
        dtype=np.float32,
    )
    x = vec.fit_transform(texts)
    clf = LogisticRegression(C=C, max_iter=2000)
    clf.fit(x, labels)
    return vec, clf


def proper_scores(probs, y_idx, k):
    import numpy as np

    eps = 1e-12
    p_true = probs[np.arange(len(y_idx)), y_idx]
    nll = float(-np.log(np.clip(p_true, eps, 1.0)).mean())
    onehot = np.zeros_like(probs)
    onehot[np.arange(len(y_idx)), y_idx] = 1.0
    brier = float(((probs - onehot) ** 2).sum(axis=1).mean())
    acc = float((probs.argmax(axis=1) == y_idx).mean())
    return {
        "nll": nll,
        "brier": brier,
        "accuracy": acc,
        "uniform_nll": math.log(k),
        "uniform_brier": 1.0 - 1.0 / k,
    }


def run_fold(records, known, unknown_cert, unknown_extra, args):
    import numpy as np

    known = list(known)
    idx = {f: i for i, f in enumerate(known)}
    train = [r for r in records if r["role"] == "train" and r["family"] in idx]
    vec, clf = fit_detector(
        [r["text"] for r in train],
        [idx[r["family"]] for r in train],
        args.max_features,
        args.C,
    )
    order = [list(clf.classes_).index(i) for i in range(len(known))]

    def probs_for(rows):
        if not rows:
            return np.zeros((0, len(known)))
        return clf.predict_proba(
            vec.transform([r["text"] for r in rows])
        )[:, order]

    known_counts, unknown_counts = {}, {}
    for f in known:
        rows = [
            r for r in records
            if r["role"] == "certificate" and r["family"] == f
        ]
        known_counts[f] = gate_counts(probs_for(rows), args.thresholds)
    for u in unknown_cert:
        rows = [
            r for r in records
            if r["role"] == "certificate" and r["family"] == u
        ]
        unknown_counts[u] = gate_counts(probs_for(rows), args.thresholds)

    cert = certify(
        known_counts,
        unknown_counts,
        args.thresholds,
        args.alpha,
        args.delta,
        args.pi_grid,
        args.lk_floors,
    )

    test_known = [
        r for r in records if r["role"] == "test" and r["family"] in idx
    ]
    pk = probs_for(test_known)
    cert["known_test_scores"] = (
        proper_scores(
            pk,
            np.array([idx[r["family"]] for r in test_known]),
            len(known),
        )
        if test_known else None
    )
    cert["counts"] = {
        "train": len(train),
        "certificate_known": {f: n for f, (_, n) in known_counts.items()},
        "certificate_unknown": {u: n for u, (_, n) in unknown_counts.items()},
    }

    if unknown_extra:
        transport = {}
        for g in unknown_extra:
            rows = [
                r for r in records if r["role"] == "test" and r["family"] == g
            ]
            acc, n = gate_counts(probs_for(rows), args.thresholds)
            transport[g] = {
                "n": n,
                "observed_acceptance": {
                    str(t): acc[t] / n if n else None for t in args.thresholds
                },
                "certified_U_U": {
                    str(r["tau"]): r["U_U"] for r in cert["thresholds"]
                },
                "exceedances": [
                    r["tau"] for r in cert["thresholds"]
                    if r["tau"] > 0 and n and acc[r["tau"]] / n > r["U_U"]
                ],
            }
        cert["transport"] = transport
    return cert


def render(summary: dict) -> str:
    config = summary["config"]
    lines = [
        "# Known-membership certificate — RAID development run",
        "",
        f"Status: `{summary['status']}`",
        "",
        "## Leave-one-machine-family-out",
        "",
        "| Unknown | Known acc. | NLL / uniform | Lift@L_K>=0.5 | "
        "Best lift any gate | "
        + " | ".join(f"pi_U={p}" for p in config["pi_grid"])
        + " |",
        "| --- | --- | --- | --- | --- | "
        + " | ".join("---" for _ in config["pi_grid"])
        + " |",
    ]
    for u, fold in summary["leave_one_family_out"].items():
        sc = fold.get("known_test_scores") or {}
        lift50 = fold["best_lift_by_LK_floor"].get("0.5")
        any_lift = fold["best_lift_any_gate"]
        decisions = []
        for p in config["pi_grid"]:
            d = fold["decisions"][str(p)]
            if d["decision"] == "PROMOTE":
                decisions.append(
                    f"PROMOTE (tau={d['tau']}, L_K={d['L_K']:.2f})"
                )
            else:
                decisions.append(d["decision"])
        lines.append(
            f"| {u} | {sc.get('accuracy', float('nan')):.3f} | "
            f"{sc.get('nll', float('nan')):.3f} / "
            f"{sc.get('uniform_nll', float('nan')):.3f} | "
            f"{'n/a' if lift50 is None else f'{lift50:.2f}'} | "
            f"{'n/a' if any_lift is None else f'{any_lift:.2f}'} | "
            + " | ".join(decisions)
            + " |"
        )

    if summary["transport_pairs"]:
        lines += [
            "",
            "## Transport stress test (certify on f, observe g)",
            "",
            "| f -> g | Lift@L_K>=0.5 on f | Thresholds where g exceeds U_U(f) |",
            "| --- | --- | --- |",
        ]
        for pair, row in summary["transport_pairs"].items():
            lift50_text = (
                "n/a" if row["lift50"] is None else f"{row['lift50']:.2f}"
            )
            exceedance_text = (
                ", ".join(str(v) for v in row["exceedances"]) or "none"
            )
            lines.append(
                f"| {pair} | {lift50_text} | {exceedance_text} |"
            )

    lines += [
        "",
        "Lift = break-even prevalence / delta; 1.0 = accept-all.",
        "Lift@L_K>=0.5 is the fixed development viability screen; "
        "the unconstrained maximum is reported only to expose tiny-coverage gates.",
        "Development-only: these results must not tune a confirmatory protocol.",
        "",
    ]
    return "\n".join(lines)


def parse_args(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--input-file", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--expected-sha256")
    ap.add_argument("--families", default=DEFAULT_FAMILIES)
    ap.add_argument("--domains", default=DEFAULT_DOMAINS)
    ap.add_argument("--human-label", default="human")
    ap.add_argument("--decoding", default="sampling")
    ap.add_argument("--per-family", type=int, default=3000)
    ap.add_argument("--seed", default="km-dev-20261125")
    ap.add_argument("--thresholds", default=DEFAULT_THRESHOLDS)
    ap.add_argument("--pi-grid", default=DEFAULT_PI_GRID)
    ap.add_argument("--lk-floors", default=DEFAULT_LK_FLOORS)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--delta", type=float, default=0.10)
    ap.add_argument("--max-features", type=int, default=200000)
    ap.add_argument("--C", type=float, default=4.0)
    ap.add_argument("--transport", action="store_true")
    args = ap.parse_args(argv)
    args.families = [s for s in args.families.split(",") if s]
    args.domains = [s for s in args.domains.split(",") if s]
    args.thresholds = sorted({float(s) for s in args.thresholds.split(",")})
    if 0.0 not in args.thresholds:
        args.thresholds = [0.0] + args.thresholds
    args.pi_grid = [float(s) for s in args.pi_grid.split(",")]
    args.lk_floors = [float(s) for s in args.lk_floors.split(",")]
    return args


def main(argv=None) -> int:
    args = parse_args(argv)
    t0 = time.time()
    if args.expected_sha256:
        actual = sha256_file(args.input_file)
        if actual != args.expected_sha256:
            raise SystemExit(f"source sha256 mismatch: {actual}")

    records = load_records(
        args.input_file,
        args.families,
        args.domains,
        args.per_family,
        args.seed,
        args.decoding,
    )
    machines = [f for f in args.families if f != args.human_label]

    folds = {}
    for unknown in machines:
        known = [f for f in args.families if f != unknown]
        folds[unknown] = run_fold(records, known, [unknown], [], args)

    transport = {}
    if args.transport:
        for f in machines:
            for g in machines:
                if f == g:
                    continue
                known = [x for x in args.families if x not in (f, g)]
                result = run_fold(records, known, [f], [g], args)
                transport[f"{f}->{g}"] = {
                    "lift50": result["best_lift_by_LK_floor"].get("0.5"),
                    **result["transport"][g],
                }

    summary = {
        "status": "STAGE_A_DEVELOPMENT_ONLY / NOT_CONFIRMATORY",
        "source_sha256": args.expected_sha256,
        "config": {
            k: v for k, v in vars(args).items()
            if k not in ("input_file", "output_dir")
        },
        "record_counts": {
            f: {
                role: sum(
                    1 for r in records
                    if r["family"] == f and r["role"] == role
                )
                for role, _ in ROLE_FRACTIONS
            }
            for f in args.families
        },
        "leave_one_family_out": folds,
        "transport_pairs": transport,
        "runtime_seconds": round(time.time() - t0, 1),
        "raw_text_persisted": False,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "known-membership-dev-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True, default=str),
        encoding="utf-8",
    )
    report = render(summary)
    (args.output_dir / "known-membership-dev-report.md").write_text(
        report, encoding="utf-8"
    )
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
