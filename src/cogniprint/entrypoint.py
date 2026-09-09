"""Primary console entrypoint with the M3 dossier workflow."""
from __future__ import annotations

import sys
from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] == "dossier":
        from .dossier_security import main as dossier_main

        return dossier_main(args[1:])
    if not args or args[0] in {"-h", "--help"}:
        print("M3 workflow: cogniprint dossier {export,verify,purge-temp,limits} ...")
    from .cli import main as legacy_main

    return legacy_main(args)
