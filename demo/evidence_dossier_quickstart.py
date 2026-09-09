"""Small reproducible M3 export/verify/mutation-rejection demonstration."""
from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path

from cogniprint.dossier import DossierError
from cogniprint.dossier_security import export_dossier_hardened, verify_dossier_hardened


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--software-commit", required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() or output.is_symlink():
        raise SystemExit(f"output already exists: {output}")

    with tempfile.TemporaryDirectory(prefix="cogniprint-m3-demo-") as temporary:
        root = Path(temporary)
        source = root / "source.txt"
        source.write_text(
            "private demo source; it must not enter the dossier\n",
            encoding="utf-8",
        )
        artifact = root / "analysis.json"
        artifact.write_text(
            '{"signal":"descriptive","value":0.125}\n',
            encoding="utf-8",
        )
        export_dossier_hardened(
            source=source,
            artifacts={"analysis.json": artifact},
            output=output,
            software_commit=args.software_commit,
        )
        report = verify_dossier_hardened(output)
        print(json.dumps(report, sort_keys=True, separators=(",", ":")))

        corrupted = root / "corrupted"
        shutil.copytree(output, corrupted)
        target = corrupted / "artifacts/analysis.json"
        data = bytearray(target.read_bytes())
        data[-2] ^= 1
        target.write_bytes(data)
        try:
            verify_dossier_hardened(corrupted)
        except DossierError:
            pass
        else:
            raise SystemExit("mutation rejection failed")

    print("M3_QUICKSTART_EXPORT_VERIFY=PASS")
    print("M3_QUICKSTART_MUTATION_REJECTION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
