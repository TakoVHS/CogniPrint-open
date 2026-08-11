#!/usr/bin/env python3
"""Read-only CLI verifier for a CogniPrint XRPL Testnet anchor receipt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cogniprint.xrpl_receipt import (
    ReceiptError,
    TESTNET_JSON_RPC,
    fetch_transaction,
    verify_validated_receipt,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path, help="public-safe evidence manifest JSON")
    parser.add_argument("transaction_hash", help="XRPL transaction hash")
    parser.add_argument("--rpc-url", default=TESTNET_JSON_RPC)
    args = parser.parse_args()

    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        if not isinstance(manifest, dict):
            raise ReceiptError("manifest JSON must be an object")
        response = fetch_transaction(args.transaction_hash, rpc_url=args.rpc_url)
        receipt = verify_validated_receipt(manifest, response)
    except (OSError, json.JSONDecodeError, ReceiptError) as exc:
        print(f"XRPL_ANCHOR_VERIFICATION=FAIL\nREASON={exc}")
        return 1

    print("XRPL_ANCHOR_VERIFICATION=PASS")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
