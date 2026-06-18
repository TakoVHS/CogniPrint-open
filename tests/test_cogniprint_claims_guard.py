from __future__ import annotations

from pathlib import Path

from scripts import cogniprint_claims_guard as guard


def test_claims_guard_flags_unbounded_public_claim(tmp_path: Path) -> None:
    public_file = tmp_path / "README.md"
    public_file.write_text("CogniPrint is an AI detector for production use.\n", encoding="utf-8")

    findings = guard.scan(tmp_path)

    assert any(finding.severity == "review" for finding in findings)
    assert guard.should_fail(findings, "review") is True


def test_claims_guard_allows_explicit_guardrail_context(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    public_file = docs_dir / "claims.md"
    public_file.write_text("Do not describe CogniPrint as an AI detector.\n", encoding="utf-8")

    findings = guard.scan(tmp_path)

    assert findings
    assert all(finding.severity == "allow-review" for finding in findings)
    assert guard.should_fail(findings, "review") is False


def test_claims_guard_blocks_legacy_branding(tmp_path: Path) -> None:
    script_file = tmp_path / "scripts" / "legacy.py"
    script_file.parent.mkdir()
    script_file.write_text("name = 'Aletheia'\n", encoding="utf-8")

    findings = guard.scan(tmp_path)

    assert any(finding.severity == "blocker" for finding in findings)
    assert guard.should_fail(findings, "blocker") is True


def test_claims_guard_skips_generated_report(tmp_path: Path) -> None:
    report = tmp_path / "docs" / "claims-guard-report.md"
    report.parent.mkdir()
    report.write_text("CogniPrint is an AI detector.\n", encoding="utf-8")

    assert guard.scan(tmp_path) == []


def test_claims_guard_flags_stale_arxiv_pending_wording(tmp_path: Path) -> None:
    public_file = tmp_path / "README.md"
    public_file.write_text("The manuscript has arXiv submission pending.\n", encoding="utf-8")

    findings = guard.scan(tmp_path)

    assert any(finding.term == "arXiv submission pending" and finding.severity == "review" for finding in findings)
