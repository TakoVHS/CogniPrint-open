"""Generate arXiv-safe PDF figures for the CogniPrint manuscript.

This script intentionally uses only the Python standard library. The arXiv
package can therefore be rebuilt without matplotlib, Inkscape, or shell-escape
SVG conversion.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from statistics import fmean


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "paper" / "figures"


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    write_boxplot_pdf(
        FIGURE_DIR / "human-paraphrase-distance-summary.pdf",
        title="Human-paraphrase diagnostic",
        subtitle="Euclidean profile distances: paraphrase pairs vs random corpus pairs",
        groups=[
            (
                "paraphrase\npairs",
                read_column(ROOT / "validation/human-paraphrase-v1/results.csv", "euclidean_distance"),
            ),
            (
                "random\npairs",
                read_filtered_column(
                    ROOT / "validation/human-paraphrase-v1/random-pair-distances.csv",
                    value_column="distance",
                    filter_column="metric",
                    filter_value="euclidean_distance",
                ),
            ),
        ],
        footer="Descriptive diagnostic only; not an inference claim or universal threshold.",
    )
    cross_rows = read_rows(ROOT / "validation/cross-genre-v1/results.csv")
    write_boxplot_pdf(
        FIGURE_DIR / "cross-genre-distance-summary.pdf",
        title="PAN15 cross-genre stress test",
        subtitle="Within-author cross-genre pairs vs inter-author controls",
        groups=[
            (
                "within-author\ncross-genre",
                [
                    float(row["euclidean_distance"])
                    for row in cross_rows
                    if row["pair_type"] == "within_author_cross_genre"
                ],
            ),
            (
                "inter-author\ncontrol",
                [
                    float(row["euclidean_distance"])
                    for row in cross_rows
                    if row["pair_type"].startswith("inter_author")
                ],
            ),
        ],
        footer="Descriptive contrast on PAN15 subset; not an identity decision system.",
    )
    print(f"Paper figures written to {FIGURE_DIR}")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_column(path: Path, column: str) -> list[float]:
    return [float(row[column]) for row in read_rows(path)]


def read_filtered_column(path: Path, *, value_column: str, filter_column: str, filter_value: str) -> list[float]:
    return [float(row[value_column]) for row in read_rows(path) if row[filter_column] == filter_value]


def write_boxplot_pdf(
    path: Path,
    *,
    title: str,
    subtitle: str,
    groups: list[tuple[str, list[float]]],
    footer: str,
) -> None:
    width, height = 612.0, 396.0
    left, bottom, plot_w, plot_h = 82.0, 78.0, 460.0, 230.0
    all_values = [value for _, values in groups for value in values]
    ymax = max(all_values) if all_values else 1.0
    ymax = nice_upper_bound(ymax)

    stream: list[str] = []
    text(stream, title, 34, height - 42, size=15, bold=True)
    text(stream, subtitle, 34, height - 62, size=9)
    text(stream, "D2 distance", 28, bottom + plot_h + 8, size=8)
    text(stream, footer, 34, 28, size=8)

    stroke(stream, 0.0, 0.0, 0.0)
    line(stream, left, bottom, left, bottom + plot_h, width=0.8)
    line(stream, left, bottom, left + plot_w, bottom, width=0.8)

    for tick in y_ticks(ymax):
        y = bottom + (tick / ymax) * plot_h
        stroke(stream, 0.82, 0.82, 0.82)
        line(stream, left, y, left + plot_w, y, width=0.25)
        stroke(stream, 0.0, 0.0, 0.0)
        line(stream, left - 4, y, left, y, width=0.6)
        text(stream, f"{tick:.2f}", 34, y - 3, size=7)

    slot = plot_w / max(len(groups), 1)
    for index, (label, values) in enumerate(groups):
        x = left + slot * (index + 0.5)
        stats = box_stats(values)
        draw_box(stream, x, bottom, plot_h, ymax, stats)
        for offset, value in sparse_points(values, limit=60):
            y = bottom + (value / ymax) * plot_h
            fill(stream, 0.18, 0.18, 0.18)
            circle(stream, x + offset, y, radius=1.15)
        for line_index, label_line in enumerate(label.split("\n")):
            text(stream, label_line, x - 38, bottom - 24 - line_index * 11, size=8)
        text(stream, f"n={len(values)}", x - 17, bottom + plot_h + 11, size=8)
        text(stream, f"mean={fmean(values):.3f}", x - 28, bottom + plot_h + 24, size=8)

    write_pdf(path, width, height, "\n".join(stream).encode("latin-1"))


def nice_upper_bound(value: float) -> float:
    if value <= 0:
        return 1.0
    exponent = math.floor(math.log10(value))
    base = 10**exponent
    scaled = value / base
    if scaled <= 1:
        rounded = 1
    elif scaled <= 2:
        rounded = 2
    elif scaled <= 5:
        rounded = 5
    else:
        rounded = 10
    return float(rounded * base)


def y_ticks(ymax: float) -> list[float]:
    return [ymax * i / 5 for i in range(6)]


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    xs = sorted(values)
    if len(xs) == 1:
        return xs[0]
    rank = (len(xs) - 1) * p
    low = math.floor(rank)
    high = math.ceil(rank)
    if low == high:
        return xs[low]
    weight = rank - low
    return xs[low] * (1 - weight) + xs[high] * weight


def box_stats(values: list[float]) -> dict[str, float]:
    return {
        "min": min(values),
        "q1": percentile(values, 0.25),
        "median": percentile(values, 0.50),
        "q3": percentile(values, 0.75),
        "max": max(values),
        "mean": fmean(values),
    }


def sparse_points(values: list[float], *, limit: int) -> list[tuple[float, float]]:
    if len(values) <= limit:
        selected = list(enumerate(values))
    else:
        step = len(values) / limit
        selected = [(int(i * step), values[int(i * step)]) for i in range(limit)]
    points = []
    for idx, value in selected:
        offset = ((idx * 37) % 29) - 14
        points.append((float(offset) * 0.9, value))
    return points


def draw_box(stream: list[str], x: float, bottom: float, plot_h: float, ymax: float, stats: dict[str, float]) -> None:
    def y(value: float) -> float:
        return bottom + (value / ymax) * plot_h

    box_w = 54.0
    whisker_w = 28.0
    stroke(stream, 0.0, 0.0, 0.0)
    line(stream, x, y(stats["min"]), x, y(stats["max"]), width=0.8)
    line(stream, x - whisker_w / 2, y(stats["min"]), x + whisker_w / 2, y(stats["min"]), width=0.8)
    line(stream, x - whisker_w / 2, y(stats["max"]), x + whisker_w / 2, y(stats["max"]), width=0.8)
    fill(stream, 0.92, 0.92, 0.92)
    rect(stream, x - box_w / 2, y(stats["q1"]), box_w, y(stats["q3"]) - y(stats["q1"]), fill_box=True)
    stroke(stream, 0.0, 0.0, 0.0)
    rect(stream, x - box_w / 2, y(stats["q1"]), box_w, y(stats["q3"]) - y(stats["q1"]), fill_box=False)
    line(stream, x - box_w / 2, y(stats["median"]), x + box_w / 2, y(stats["median"]), width=1.2)
    stroke(stream, 0.0, 0.0, 0.0)
    line(stream, x - 8, y(stats["mean"]), x + 8, y(stats["mean"]), width=0.8)
    line(stream, x, y(stats["mean"]) - 8, x, y(stats["mean"]) + 8, width=0.8)


def text(stream: list[str], value: str, x: float, y: float, *, size: int, bold: bool = False) -> None:
    font = "F2" if bold else "F1"
    stream.append(f"BT /{font} {size} Tf {x:.2f} {y:.2f} Td ({escape_pdf_text(value)}) Tj ET")


def line(stream: list[str], x1: float, y1: float, x2: float, y2: float, *, width: float) -> None:
    stream.append(f"{width:.2f} w {x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")


def rect(stream: list[str], x: float, y: float, width: float, height: float, *, fill_box: bool) -> None:
    operator = "f" if fill_box else "S"
    stream.append(f"{x:.2f} {y:.2f} {width:.2f} {height:.2f} re {operator}")


def circle(stream: list[str], x: float, y: float, *, radius: float) -> None:
    rect(stream, x - radius, y - radius, radius * 2, radius * 2, fill_box=True)


def stroke(stream: list[str], r: float, g: float, b: float) -> None:
    stream.append(f"{r:.3f} {g:.3f} {b:.3f} RG")


def fill(stream: list[str], r: float, g: float, b: float) -> None:
    stream.append(f"{r:.3f} {g:.3f} {b:.3f} rg")


def escape_pdf_text(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def write_pdf(path: Path, width: float, height: float, content: bytes) -> None:
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width:.0f} {height:.0f}] "
            f"/Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>"
        ).encode("ascii"),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>",
        b"<< /Length " + str(len(content)).encode("ascii") + b" >>\nstream\n" + content + b"\nendstream",
    ]
    chunks = [b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"]
    offsets = [0]
    for obj_id, obj in enumerate(objects, start=1):
        offsets.append(sum(len(chunk) for chunk in chunks))
        chunks.append(f"{obj_id} 0 obj\n".encode("ascii") + obj + b"\nendobj\n")
    xref_offset = sum(len(chunk) for chunk in chunks)
    chunks.append(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    chunks.append(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        chunks.append(f"{offset:010d} 00000 n \n".encode("ascii"))
    chunks.append(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n"
        ).encode("ascii")
    )
    path.write_bytes(b"".join(chunks))


if __name__ == "__main__":
    main()
