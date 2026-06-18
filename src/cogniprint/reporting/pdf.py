"""Minimal dependency-free PDF report generation."""

from __future__ import annotations

from pathlib import Path

from .markdown import generate_markdown_report


def generate_pdf_report(study_dir: Path, output_file: Path) -> Path:
    """Generate a simple readable PDF from a study artifact.

    This intentionally avoids heavy PDF dependencies. The PDF is plain text
    layout suitable for local review and archival bundles.
    """

    temp_md = output_file.with_suffix(".tmp.md")
    generate_markdown_report(study_dir, temp_md)
    text = temp_md.read_text(encoding="utf-8")
    temp_md.unlink(missing_ok=True)
    lines = _wrap_lines(text.replace("`", ""), width=92)
    _write_simple_pdf(output_file, lines)
    return output_file


def _wrap_lines(text: str, width: int) -> list[str]:
    wrapped: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            wrapped.append("")
            continue
        while len(line) > width:
            split_at = line.rfind(" ", 0, width)
            if split_at <= 0:
                split_at = width
            wrapped.append(line[:split_at])
            line = line[split_at:].strip()
        wrapped.append(line)
    return wrapped


def _write_simple_pdf(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pages = [lines[index : index + 46] for index in range(0, len(lines), 46)] or [[]]
    objects: list[str] = ["<< /Type /Catalog /Pages 2 0 R >>"]
    page_refs = []
    content_objects = []
    for page_index, page_lines in enumerate(pages):
        page_object_number = 3 + page_index * 2
        content_object_number = page_object_number + 1
        page_refs.append(f"{page_object_number} 0 R")
        stream = _page_stream(page_lines)
        objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Times-Roman >> >> >> /Contents {content_object_number} 0 R >>")
        content_objects.append(f"<< /Length {len(stream.encode('latin-1'))} >>\nstream\n{stream}\nendstream")
    pages_object = f"<< /Type /Pages /Kids [{' '.join(page_refs)}] /Count {len(page_refs)} >>"
    objects.insert(1, pages_object)
    interleaved = objects[:2]
    for index in range(len(pages)):
        interleaved.append(objects[2 + index])
        interleaved.append(content_objects[index])
    offsets = []
    body = "%PDF-1.4\n"
    for number, obj in enumerate(interleaved, start=1):
        offsets.append(len(body.encode("latin-1")))
        body += f"{number} 0 obj\n{obj}\nendobj\n"
    xref_offset = len(body.encode("latin-1"))
    body += f"xref\n0 {len(interleaved) + 1}\n0000000000 65535 f \n"
    for offset in offsets:
        body += f"{offset:010d} 00000 n \n"
    body += f"trailer\n<< /Size {len(interleaved) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n"
    path.write_bytes(body.encode("latin-1", errors="replace"))


def _page_stream(lines: list[str]) -> str:
    commands = ["BT", "/F1 11 Tf", "50 750 Td"]
    first = True
    for line in lines:
        escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        if first:
            commands.append(f"({escaped}) Tj")
            first = False
        else:
            commands.append(f"0 -15 Td ({escaped}) Tj")
    commands.append("ET")
    return "\n".join(commands)
