from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "check_metadata_consistency.py"
SPEC = importlib.util.spec_from_file_location("check_metadata_consistency", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class MetadataConsistencyTests(unittest.TestCase):
    def test_normalize_author_variants(self) -> None:
        self.assertEqual(MODULE.normalize_author("Adriashkin, Roman"), "Adriashkin Roman")
        self.assertEqual(MODULE.normalize_author("Adriashkin Roman"), "Adriashkin Roman")

    def test_normalize_orcid_variants(self) -> None:
        self.assertEqual(MODULE.normalize_orcid("https://orcid.org/0009-0009-6337-1806"), "0009-0009-6337-1806")
        self.assertEqual(MODULE.normalize_orcid("0009-0009-6337-1806"), "0009-0009-6337-1806")

    def test_script_passes_for_repo_state(self) -> None:
        result = MODULE.main(["--root", str(ROOT), "--site-root", str(ROOT.parent / "TakoVHS.github.io")])
        self.assertEqual(result, 0)

    def test_script_fails_on_bad_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "README.md").write_text("CogniPrint Adriashkin Roman 0009-0009-6337-1806", encoding="utf-8")
            (root / "CITATION.cff").write_text(
                "\n".join(
                    [
                        "cff-version: 1.2.0",
                        'title: "Wrong title"',
                        "authors:",
                        '  - family-names: "Adriashkin"',
                        '    given-names: "Roman"',
                        '    orcid: "https://orcid.org/0009-0009-6337-1806"',
                        'url: "https://cogniprint.org"',
                        'repository-code: "https://github.com/TakoVHS/CogniPrint"',
                        "date-released: 2026-04-20",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (root / ".zenodo.json").write_text(
                '{"title": "Wrong title", "creators": [{"name": "Adriashkin, Roman", "orcid": "0009-0009-6337-1806"}]}',
                encoding="utf-8",
            )
            result = MODULE.main(["--root", str(root)])
            self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
