"""Build one wheel, install it twice, export in one install and verify in the other."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(
    command: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def binary(venv: Path, name: str) -> Path:
    directory = "Scripts" if os.name == "nt" else "bin"
    suffix = ".exe" if os.name == "nt" else ""
    return venv / directory / f"{name}{suffix}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--software-commit", default=None)
    args = parser.parse_args()
    repo = args.repo.resolve()
    commit = args.software_commit or run(["git", "rev-parse", "HEAD"], cwd=repo).stdout.strip()

    with tempfile.TemporaryDirectory(prefix="cogniprint-cross-install-") as temporary:
        root = Path(temporary)
        wheelhouse = root / "wheelhouse"
        wheelhouse.mkdir()
        run(
            [
                sys.executable,
                "-m",
                "pip",
                "wheel",
                "--no-deps",
                "--no-build-isolation",
                "--wheel-dir",
                str(wheelhouse),
                str(repo),
            ]
        )
        wheels = list(wheelhouse.glob("cogniprint-*.whl"))
        if len(wheels) != 1:
            raise SystemExit(f"expected one wheel, found {wheels}")

        producer = root / "producer"
        verifier = root / "verifier"
        for environment in (producer, verifier):
            run([sys.executable, "-m", "venv", str(environment)])
            run(
                [
                    str(binary(environment, "python")),
                    "-m",
                    "pip",
                    "install",
                    "--no-deps",
                    str(wheels[0]),
                ]
            )

        source = root / "source.txt"
        source_bytes = b"cross-installation private source\n"
        source.write_bytes(source_bytes)
        artifact = root / "analysis.json"
        artifact.write_text(
            '{"signal":"descriptive","value":0.5}\n',
            encoding="utf-8",
        )
        produced = root / "produced"
        run(
            [
                str(binary(producer, "cogniprint")),
                "dossier",
                "export",
                "--source",
                str(source),
                "--artifact",
                f"analysis.json={artifact}",
                "--software-commit",
                commit,
                "--output",
                str(produced),
            ]
        )
        received = root / "received"
        shutil.copytree(produced, received)

        guard = root / "network-guard"
        guard.mkdir()
        (guard / "sitecustomize.py").write_text(
            "import socket\n"
            "def blocked(*args, **kwargs):\n"
            "    raise RuntimeError('network access forbidden by cross-installation gate')\n"
            "socket.socket = blocked\n"
            "socket.create_connection = blocked\n",
            encoding="utf-8",
        )
        verifier_env = os.environ.copy()
        verifier_env["PYTHONPATH"] = str(guard)
        verified = run(
            [
                str(binary(verifier, "cogniprint")),
                "dossier",
                "verify",
                "--bundle",
                str(received),
            ],
            env=verifier_env,
        )
        report = json.loads(verified.stdout)
        if report.get("status") != "VERIFIED" or report.get("offline") is not True:
            raise SystemExit(f"unexpected verifier report: {report}")

        producer_prefix = run(
            [str(binary(producer, "python")), "-c", "import sys; print(sys.prefix)"]
        ).stdout.strip()
        verifier_prefix = run(
            [str(binary(verifier, "python")), "-c", "import sys; print(sys.prefix)"]
        ).stdout.strip()
        if producer_prefix == verifier_prefix:
            raise SystemExit("producer and verifier are not independent installations")
        for path in received.rglob("*"):
            if path.is_file() and source_bytes in path.read_bytes():
                raise SystemExit(f"source bytes leaked into dossier: {path}")

        corrupted = root / "corrupted"
        shutil.copytree(received, corrupted)
        payload = corrupted / "artifacts/analysis.json"
        data = bytearray(payload.read_bytes())
        data[-2] ^= 1
        payload.write_bytes(data)
        failed = subprocess.run(
            [
                str(binary(verifier, "cogniprint")),
                "dossier",
                "verify",
                "--bundle",
                str(corrupted),
            ],
            env=verifier_env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if failed.returncode == 0:
            raise SystemExit("corrupted dossier unexpectedly verified")

    print("CROSS_INSTALLATION_PRODUCER=PASS")
    print("CROSS_INSTALLATION_OFFLINE_VERIFIER=PASS")
    print("CROSS_INSTALLATION_MUTATION_REJECTION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
