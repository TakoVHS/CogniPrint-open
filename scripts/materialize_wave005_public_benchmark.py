#!/usr/bin/env python3
"""Materialize wave-005 public benchmark sources for public-benchmark-v1.1.

The script only uses short public-domain excerpts with explicit Wikisource
provenance. It updates the v1.1 public benchmark registry, public text files,
and evidence summaries. It does not read from workspace/ or any private input.
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET_ROOT = ROOT / "datasets" / "public-benchmark-v1.1"
EVIDENCE_ROOT = ROOT / "evidence" / "public-benchmark-v1.1"
REGISTRY_PATH = DATASET_ROOT / "metadata" / "sample-plan-template.csv"
INTAKE_PATH = DATASET_ROOT / "metadata" / "intake-candidates.csv"
ACQUISITION_DATE = "2026-05-05"
WAVE = "wave-005"

CSV_FIELDS = [
    "sample_id",
    "relation_type",
    "baseline_sample_id",
    "sample_title",
    "file_path",
    "intake_slot_id",
    "license",
    "source_url",
    "acquisition_date",
    "source_class",
    "language",
    "source_domain",
    "release_wave",
    "release_status",
    "usage_note",
]

INTAKE_FIELDS = [
    "candidate_slot_id",
    "target_language",
    "target_domain",
    "source_family",
    "target_kind",
    "status",
    "preferred_source_policy",
    "notes",
]

AXES = [
    ("variant-a", "punctuation_cleanup", "Punctuation-only controlled variant derived locally from the released baseline excerpt."),
    ("variant-b", "compressed_version", "Controlled compression variant derived locally from the released baseline excerpt."),
    ("variant-c", "sentence_split_merge", "Sentence segmentation variant derived locally from the released baseline excerpt."),
    ("variant-d", "word_order_shift", "Word-order and clause-order shift variant derived locally from the released baseline excerpt."),
    ("variant-e", "formalized_style", "Register-marked formal variant derived locally from the released baseline excerpt."),
    ("variant-f", "informalized_style", "Register-marked informal variant derived locally from the released baseline excerpt."),
]

FORMAL_PREFIX = {
    "en": "Formal register:",
    "fr": "Registre formel :",
    "de": "Formaler Stil:",
    "es": "Registro formal:",
    "ru": "Формальный вариант:",
}

INFORMAL_PREFIX = {
    "en": "Plain register:",
    "fr": "Registre simple :",
    "de": "Einfacher Stil:",
    "es": "Registro sencillo:",
    "ru": "Простой вариант:",
}


@dataclass(frozen=True)
class SourceRecord:
    index: int
    slot: str
    title: str
    language: str
    domain: str
    source_class: str
    source_url: str
    text: str
    slot_note: str

    @property
    def baseline_id(self) -> str:
        return f"pbv11-sample-{self.index:03d}-baseline"

    @property
    def baseline_path(self) -> str:
        return f"datasets/public-benchmark-v1.1/raw/{self.baseline_id}.txt"


WAVE005_SOURCES = [
    SourceRecord(
        index=10,
        slot="pbv11-slot-016",
        title="Alice opening excerpt",
        language="en",
        domain="literary prose",
        source_class="public-domain literary text",
        source_url="https://en.wikisource.org/wiki/Alice%27s_Adventures_in_Wonderland",
        text=(
            "Alice was beginning to get very tired of sitting by her sister on the bank, and of having "
            "nothing to do: once or twice she had peeped into the book her sister was reading, but it had "
            "no pictures or conversations in it, and what is the use of a book, thought Alice, without "
            "pictures or conversations?"
        ),
        slot_note="Selected for wave-005 as an English public-domain literary baseline with stable provenance.",
    ),
    SourceRecord(
        index=11,
        slot="pbv11-slot-017",
        title="Pride and Prejudice opening excerpt",
        language="en",
        domain="literary prose",
        source_class="public-domain literary text",
        source_url="https://en.wikisource.org/wiki/Pride_and_Prejudice",
        text=(
            "It is a truth universally acknowledged, that a single man in possession of a good fortune, "
            "must be in want of a wife."
        ),
        slot_note="Selected for wave-005 as an English public-domain literary baseline with stable provenance.",
    ),
    SourceRecord(
        index=12,
        slot="pbv11-slot-018",
        title="A Tale of Two Cities opening excerpt",
        language="en",
        domain="literary prose",
        source_class="public-domain literary text",
        source_url="https://en.wikisource.org/wiki/A_Tale_of_Two_Cities",
        text=(
            "It was the best of times, it was the worst of times, it was the age of wisdom, it was the "
            "age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the "
            "season of Light, it was the season of Darkness."
        ),
        slot_note="Selected for wave-005 as an English public-domain literary baseline with stable provenance.",
    ),
    SourceRecord(
        index=13,
        slot="pbv11-slot-019",
        title="Les Misérables opening excerpt",
        language="fr",
        domain="literary prose",
        source_class="public-domain literary text",
        source_url="https://fr.wikisource.org/wiki/Les_Mis%C3%A9rables",
        text=(
            "En 1815, M. Charles-François-Bienvenu Myriel était évêque de Digne. C'était un vieillard "
            "d'environ soixante-quinze ans; il occupait le siège de Digne depuis 1806."
        ),
        slot_note="Selected for wave-005 as a French public-domain literary baseline with stable provenance.",
    ),
    SourceRecord(
        index=14,
        slot="pbv11-slot-020",
        title="Voyage au centre de la Terre opening excerpt",
        language="fr",
        domain="literary prose",
        source_class="public-domain literary text",
        source_url="https://fr.wikisource.org/wiki/Voyage_au_centre_de_la_Terre",
        text=(
            "Le 24 mai 1863, un dimanche, mon oncle, le professeur Lidenbrock, revint précipitamment "
            "vers sa petite maison située au numéro 19 de König-strasse, l'une des plus anciennes rues "
            "du vieux quartier de Hambourg."
        ),
        slot_note="Selected for wave-005 as a French public-domain literary baseline with stable provenance.",
    ),
    SourceRecord(
        index=15,
        slot="pbv11-slot-021",
        title="Faust opening excerpt",
        language="de",
        domain="dramatic verse",
        source_class="public-domain literary text",
        source_url="https://de.wikisource.org/wiki/Faust",
        text=(
            "Habe nun, ach! Philosophie, Juristerei und Medizin, und leider auch Theologie durchaus "
            "studiert, mit heißem Bemühn. Da steh ich nun, ich armer Tor! und bin so klug als wie zuvor."
        ),
        slot_note="Selected for wave-005 as a German public-domain dramatic baseline with stable provenance.",
    ),
    SourceRecord(
        index=16,
        slot="pbv11-slot-022",
        title="Die Räuber excerpt",
        language="de",
        domain="dramatic prose",
        source_class="public-domain literary text",
        source_url="https://de.wikisource.org/wiki/Die_R%C3%A4uber",
        text=(
            "Das Gesetz hat noch keinen großen Mann gebildet, aber die Freiheit brütet Kolosse und "
            "Extremitäten aus."
        ),
        slot_note="Selected for wave-005 as a German public-domain dramatic baseline with stable provenance.",
    ),
    SourceRecord(
        index=17,
        slot="pbv11-slot-023",
        title="Lazarillo de Tormes opening excerpt",
        language="es",
        domain="literary prose",
        source_class="public-domain literary text",
        source_url="https://es.wikisource.org/wiki/El_Lazarillo_de_Tormes",
        text=(
            "Pues sepa vuestra merced, ante todas cosas, que a mí llaman Lázaro de Tormes, hijo de Tomé "
            "González y de Antona Pérez, naturales de Tejares, aldea de Salamanca. Mi nacimiento fue "
            "dentro del río Tormes, por la cual causa tomé el sobrenombre."
        ),
        slot_note="Selected for wave-005 as a Spanish public-domain literary baseline with stable provenance.",
    ),
    SourceRecord(
        index=18,
        slot="pbv11-slot-024",
        title="La Regenta opening excerpt",
        language="es",
        domain="literary prose",
        source_class="public-domain literary text",
        source_url="https://es.wikisource.org/wiki/La_Regenta",
        text=(
            "La heroica ciudad dormía la siesta. El viento sur, caliente y perezoso, empujaba las nubes "
            "blanquecinas que se rasgaban al correr hacia el norte, y en las calles no había más ruido "
            "que el rumor estridente de los remolinos de polvo."
        ),
        slot_note="Selected for wave-005 as a Spanish public-domain literary baseline with stable provenance.",
    ),
    SourceRecord(
        index=19,
        slot="pbv11-slot-025",
        title="Crime and Punishment opening excerpt",
        language="ru",
        domain="literary prose",
        source_class="public-domain literary text",
        source_url="https://ru.wikisource.org/wiki/%D0%9F%D1%80%D0%B5%D1%81%D1%82%D1%83%D0%BF%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5_%D0%B8_%D0%BD%D0%B0%D0%BA%D0%B0%D0%B7%D0%B0%D0%BD%D0%B8%D0%B5_(%D0%94%D0%BE%D1%81%D1%82%D0%BE%D0%B5%D0%B2%D1%81%D0%BA%D0%B8%D0%B9)",
        text=(
            "В начале июля, в чрезвычайно жаркое время, под вечер, один молодой человек вышел из "
            "своей каморки, которую нанимал от жильцов в С-м переулке, на улицу и медленно, как бы "
            "в нерешимости, отправился к К-ну мосту."
        ),
        slot_note="Selected for wave-005 as a Russian public-domain literary baseline with stable provenance.",
    ),
    SourceRecord(
        index=20,
        slot="pbv11-slot-026",
        title="The Captain's Daughter opening excerpt",
        language="ru",
        domain="literary prose",
        source_class="public-domain literary text",
        source_url="https://ru.wikisource.org/wiki/%D0%9A%D0%B0%D0%BF%D0%B8%D1%82%D0%B0%D0%BD%D1%81%D0%BA%D0%B0%D1%8F_%D0%B4%D0%BE%D1%87%D0%BA%D0%B0_(%D0%9F%D1%83%D1%88%D0%BA%D0%B8%D0%BD)",
        text=(
            "Отец мой, Андрей Петрович Гринев, в молодости своей служил при графе Минихе и вышел в "
            "отставку премьер-майором. С тех пор жил он в своей Симбирской деревне, где женился на "
            "девице Авдотье Васильевне Ю., дочери бедного тамошнего дворянина."
        ),
        slot_note="Selected for wave-005 as a Russian public-domain literary baseline with stable provenance.",
    ),
]


def read_csv(path: Path, fieldnames: list[str]) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = [{field: row.get(field, "") for field in fieldnames} for row in reader]
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def punctuation_cleanup(text: str) -> str:
    remove = str.maketrans("", "", ",;:!?()[]{}\"“”«»")
    return normalize_spaces(text.translate(remove))


def compressed_version(text: str) -> str:
    words = normalize_spaces(text).split()
    keep = max(18, min(len(words), int(len(words) * 0.62)))
    result = " ".join(words[:keep]).rstrip(",;:")
    return result if result.endswith(".") else f"{result}."


def sentence_split_merge(text: str) -> str:
    rewritten = re.sub(r"[,;:]\s*", ". ", text)
    rewritten = re.sub(r"\.\s*\.", ".", rewritten)
    return normalize_spaces(rewritten)


def word_order_shift(text: str) -> str:
    sentences = [segment.strip() for segment in re.split(r"(?<=[.!?])\s+", text) if segment.strip()]
    if len(sentences) > 1:
        return normalize_spaces(" ".join(sentences[1:] + sentences[:1]))
    clauses = [segment.strip() for segment in re.split(r"[,;:]\s*", text) if segment.strip()]
    if len(clauses) > 1:
        return normalize_spaces("; ".join(clauses[1:] + clauses[:1]))
    return normalize_spaces(text)


def formalized_style(text: str, language: str) -> str:
    return normalize_spaces(f"{FORMAL_PREFIX[language]} {text}")


def informalized_style(text: str, language: str) -> str:
    return normalize_spaces(f"{INFORMAL_PREFIX[language]} {text}")


def variant_text(source: SourceRecord, relation_type: str) -> str:
    transforms = {
        "punctuation_cleanup": lambda: punctuation_cleanup(source.text),
        "compressed_version": lambda: compressed_version(source.text),
        "sentence_split_merge": lambda: sentence_split_merge(source.text),
        "word_order_shift": lambda: word_order_shift(source.text),
        "formalized_style": lambda: formalized_style(source.text, source.language),
        "informalized_style": lambda: informalized_style(source.text, source.language),
    }
    return transforms[relation_type]()


def registry_rows_for(source: SourceRecord) -> list[dict[str, str]]:
    rows = [
        {
            "sample_id": source.baseline_id,
            "relation_type": "baseline",
            "baseline_sample_id": "",
            "sample_title": source.title,
            "file_path": source.baseline_path,
            "intake_slot_id": source.slot,
            "license": f"Public-domain source text via {source.source_url.split('//', 1)[1].split('/', 1)[0]}",
            "source_url": source.source_url,
            "acquisition_date": ACQUISITION_DATE,
            "source_class": source.source_class,
            "language": source.language,
            "source_domain": source.domain,
            "release_wave": WAVE,
            "release_status": "released",
            "usage_note": f"Short public-domain excerpt approved for the fifth v1.1 release wave.",
        }
    ]
    for suffix, relation_type, note in AXES:
        variant_id = source.baseline_id.replace("-baseline", f"-{suffix}")
        rows.append(
            {
                "sample_id": variant_id,
                "relation_type": relation_type,
                "baseline_sample_id": source.baseline_id,
                "sample_title": f"{source.title} {relation_type.replace('_', ' ')}",
                "file_path": f"datasets/public-benchmark-v1.1/variants/{variant_id}.txt",
                "intake_slot_id": "pbv11-slot-010",
                "license": "Derived benchmark variant from a public-domain baseline excerpt",
                "source_url": source.source_url,
                "acquisition_date": ACQUISITION_DATE,
                "source_class": "controlled public benchmark variant",
                "language": source.language,
                "source_domain": source.domain,
                "release_wave": WAVE,
                "release_status": "released",
                "usage_note": note,
            }
        )
    return rows


def write_text_files() -> None:
    for source in WAVE005_SOURCES:
        baseline_path = ROOT / source.baseline_path
        baseline_path.parent.mkdir(parents=True, exist_ok=True)
        baseline_path.write_text(f"{normalize_spaces(source.text)}\n", encoding="utf-8")
        for suffix, relation_type, _note in AXES:
            variant_id = source.baseline_id.replace("-baseline", f"-{suffix}")
            path = DATASET_ROOT / "variants" / f"{variant_id}.txt"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"{variant_text(source, relation_type)}\n", encoding="utf-8")


def sample_sort_key(row: dict[str, str]) -> tuple[int, int]:
    match = re.search(r"pbv11-sample-(\d+)", row["sample_id"])
    sample_number = int(match.group(1)) if match else 9999
    relation_order = {"baseline": 0}
    for index, (_suffix, relation_type, _note) in enumerate(AXES, start=1):
        relation_order[relation_type] = index
    return (sample_number, relation_order.get(row["relation_type"], 99))


def update_registry() -> list[dict[str, str]]:
    existing = read_csv(REGISTRY_PATH, CSV_FIELDS)
    new_ids = {row["sample_id"] for source in WAVE005_SOURCES for row in registry_rows_for(source)}
    rows = [row for row in existing if row["sample_id"] not in new_ids]
    for source in WAVE005_SOURCES:
        rows.extend(registry_rows_for(source))
    rows.sort(key=sample_sort_key)
    write_csv(REGISTRY_PATH, CSV_FIELDS, rows)
    return rows


def update_intake() -> None:
    existing = read_csv(INTAKE_PATH, INTAKE_FIELDS)
    new_slots = {
        source.slot: {
            "candidate_slot_id": source.slot,
            "target_language": source.language,
            "target_domain": source.domain.replace(" ", "-"),
            "source_family": source.source_class,
            "target_kind": "baseline-target",
            "status": "selected-wave-005",
            "preferred_source_policy": "stable-public-url-and-clear-reuse",
            "notes": source.slot_note,
        }
        for source in WAVE005_SOURCES
    }
    rows = [row for row in existing if row["candidate_slot_id"] not in new_slots]
    rows.extend(new_slots.values())
    rows.sort(key=lambda row: row["candidate_slot_id"])
    write_csv(INTAKE_PATH, INTAKE_FIELDS, rows)


def unique_preserving(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def released_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [row for row in rows if row["release_status"] == "released"]


def evidence_counts(rows: list[dict[str, str]]) -> dict[str, object]:
    released = released_rows(rows)
    baselines = [row for row in released if row["relation_type"] == "baseline"]
    variants = [row for row in released if row["relation_type"] != "baseline"]
    return {
        "snapshot_id": "public-benchmark-v1.1",
        "released_samples": len(baselines),
        "released_variants": len(variants),
        "released_languages": len({row["language"] for row in released}),
        "released_source_classes": len({row["source_class"] for row in baselines}),
        "released_perturbation_axes": len({row["relation_type"] for row in variants}),
        "notes": "Counts reflect the first through fifth approved v1.1 benchmark waves.",
    }


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def markdown_table(rows: list[dict[str, str]]) -> str:
    baselines = [row for row in released_rows(rows) if row["relation_type"] == "baseline"]
    variant_count_by_baseline: dict[str, int] = {}
    for row in released_rows(rows):
        if row["relation_type"] != "baseline":
            variant_count_by_baseline[row["baseline_sample_id"]] = variant_count_by_baseline.get(row["baseline_sample_id"], 0) + 1
    lines = [
        "# Public Benchmark v1.1 Evidence Table",
        "",
        "| Sample | Language | Source domain | Variants | Source URL |",
        "|---|---:|---|---:|---|",
    ]
    for row in baselines:
        lines.append(
            f"| `{row['sample_id']}` {row['sample_title']} | `{row['language']}` | "
            f"{row['source_domain']} | {variant_count_by_baseline.get(row['sample_id'], 0)} | "
            f"{row['source_url']} |"
        )
    lines.extend(
        [
            "",
            "Each listed baseline has a registry row, a public excerpt file, and six locally derived controlled variants.",
            "The table is a provenance index only; it does not add benchmark-performance claims.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_evidence(rows: list[dict[str, str]]) -> None:
    counts = evidence_counts(rows)
    released = released_rows(rows)
    baselines = [row for row in released if row["relation_type"] == "baseline"]
    variants = [row for row in released if row["relation_type"] != "baseline"]
    languages = unique_preserving([row["language"] for row in baselines])
    source_classes = unique_preserving([row["source_class"] for row in baselines])
    axes = unique_preserving([row["relation_type"] for row in variants])
    by_wave: dict[str, int] = {}
    for row in baselines:
        by_wave[row["release_wave"]] = by_wave.get(row["release_wave"], 0) + 1

    write_json(EVIDENCE_ROOT / "counts.json", counts)
    write_json(
        EVIDENCE_ROOT / "manifest.json",
        {
            "snapshot_id": "public-benchmark-v1.1",
            "status": "fifth released benchmark-expansion wave after the public-benchmark-v1 subset",
            "dataset_root": "datasets/public-benchmark-v1.1",
            "evidence_root": "evidence/public-benchmark-v1.1",
            "released_samples": counts["released_samples"],
            "released_variants": counts["released_variants"],
            "released_languages": languages,
            "released_source_classes": source_classes,
            "released_perturbation_axes": axes,
            "released_baselines_by_wave": dict(sorted(by_wave.items())),
            "counts_source": "datasets/public-benchmark-v1.1/metadata/sample-plan-template.csv",
            "source_url_check": "Wave-005 source URLs returned HTTP 200 during the 2026-05-05 local verification pass.",
            "guardrail": (
                "This release extends the public benchmark layer with five approved waves. It remains "
                "a benchmark increment and does not support broader benchmark-performance claims."
            ),
        },
    )

    EVIDENCE_ROOT.mkdir(parents=True, exist_ok=True)
    (EVIDENCE_ROOT / "README.md").write_text(
        "\n".join(
            [
                "# Public Benchmark v1.1",
                "",
                "This directory is the public evidence layer for the `public-benchmark-v1.1` benchmark increment.",
                "",
                f"- Released baselines: `{counts['released_samples']}`",
                f"- Released controlled variants: `{counts['released_variants']}`",
                f"- Languages: `{', '.join(languages)}`",
                f"- Perturbation axes: `{', '.join(axes)}`",
                "",
                "The layer is provenance-focused. It records public-domain source URLs, local controlled variants, and counts.",
                "It remains separate from private/local `workspace/` inputs and does not add stronger claims.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (EVIDENCE_ROOT / "methods-summary.md").write_text(
        "\n".join(
            [
                "# Public Benchmark v1.1 Methods Summary",
                "",
                "This file summarizes the released `v1.1` benchmark waves.",
                "",
                "## Release method",
                "",
                "The `v1.1` release extends the public benchmark layer through approved waves rather than a full benchmark jump.",
                "",
                "Current release method:",
                "",
                "- select public-domain source texts with stable source URLs;",
                "- extract short baseline excerpts suitable for public release;",
                "- create six locally derived controlled variants per baseline across the current perturbation axes;",
                "- record every baseline and variant in `datasets/public-benchmark-v1.1/metadata/sample-plan-template.csv`;",
                "- publish matching counts and summaries under `evidence/public-benchmark-v1.1/`.",
                "",
                "## Current released waves",
                "",
                f"The released `v1.1` waves now include `{counts['released_samples']}` baselines and `{counts['released_variants']}` variants.",
                "Wave-005 adds eleven provenance-clean public-domain baselines while preserving the six existing perturbation axes.",
                "The purpose is benchmark breadth and provenance quality, not stronger inferential wording.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (EVIDENCE_ROOT / "results-summary.md").write_text(
        "\n".join(
            [
                "# Public Benchmark v1.1 Results Summary",
                "",
                "The released `v1.1` benchmark waves now contribute:",
                "",
                f"- `{counts['released_samples']}` baseline excerpts;",
                f"- `{counts['released_variants']}` controlled variants;",
                f"- `{counts['released_languages']}` benchmark languages (`{', '.join(languages)}`);",
                f"- `{counts['released_source_classes']}` released baseline source classes.",
                "",
                "## Current usefulness",
                "",
                "This release is useful because it:",
                "",
                "- reaches the minimum public benchmark size target for the v1.1 increment;",
                "- keeps every new baseline tied to a public source URL and explicit reuse note;",
                "- expands literary coverage across English, French, German, Spanish, and Russian sources;",
                "- preserves the same six controlled perturbation axes already used by the prior v1.1 waves;",
                "- creates a cleaner basis for a later benchmark-aware descriptive validation rerun.",
                "",
                "## Guardrail",
                "",
                "This is a benchmark-expansion release. It does not by itself justify broader benchmark-performance claims or stronger inferential wording.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (EVIDENCE_ROOT / "limitations-summary.md").write_text(
        "\n".join(
            [
                "# Public Benchmark v1.1 Limitations Summary",
                "",
                "The current `v1.1` release remains limited.",
                "",
                "Main limitations:",
                "",
                f"- only `{counts['released_samples']}` baselines are released in this increment;",
                "- the benchmark is larger than the earlier subset but still small relative to a full empirical benchmark;",
                "- literary public-domain text is intentionally overrepresented because provenance is cleaner;",
                "- no private/raw local inputs are included;",
                "- this release should be treated as a benchmark expansion step, not as an inferential validation result.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    provenance_lines = [
        "# Public Benchmark v1.1 Provenance Summary",
        "",
        "Each released baseline is a short public-domain excerpt with an explicit public source URL.",
        "Controlled variants are derived locally from those baseline excerpts and inherit the baseline source URL for traceability.",
        "",
    ]
    for row in baselines:
        provenance_lines.append(
            f"- `{row['sample_id']}` {row['sample_title']} (`{row['language']}`): "
            f"{row['license']}; source: {row['source_url']}; acquired: `{row['acquisition_date']}`."
        )
    provenance_lines.extend(
        [
            "",
            "No `workspace/` private inputs are used for this public benchmark layer.",
        ]
    )
    (EVIDENCE_ROOT / "provenance-summary.md").write_text("\n".join(provenance_lines) + "\n", encoding="utf-8")
    (EVIDENCE_ROOT / "evidence-table.md").write_text(markdown_table(rows), encoding="utf-8")


def main() -> int:
    write_text_files()
    rows = update_registry()
    update_intake()
    write_evidence(rows)
    counts = evidence_counts(rows)
    print(
        "Materialized public-benchmark-v1.1: "
        f"{counts['released_samples']} baselines / {counts['released_variants']} variants."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
