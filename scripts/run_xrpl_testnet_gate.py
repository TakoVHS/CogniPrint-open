#!/usr/bin/env python3
"""Run the real CogniPrint XRPL Testnet evidence-anchor gate.

This script is intentionally Testnet-only. It generates two ephemeral faucet
wallets, sends 1 drop of Testnet XRP with a CogniPrint commitment memo, waits
for a validated ledger result, independently re-fetches the transaction by hash,
verifies the local manifest against the ledger memo, then mutates the manifest
and requires fail-closed rejection.

Wallet seeds are never printed or written to disk by this script.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

from cogniprint.xrpl_anchor import build_anchor_payload, encode_memo_data
from cogniprint.xrpl_receipt import (
    TESTNET_JSON_RPC,
    ReceiptError,
    fetch_transaction,
    verify_validated_receipt,
)

try:
    from xrpl.clients import JsonRpcClient
    from xrpl.models.transactions import Memo, Payment
    from xrpl.transaction import submit_and_wait
    from xrpl.wallet import generate_faucet_wallet
except ImportError as exc:  # pragma: no cover - environment gate
    raise SystemExit(
        "xrpl-py is required for the live Testnet gate. "
        "Install with: python -m pip install -r requirements-xrpl-testnet.txt"
    ) from exc

DEFAULT_MANIFEST = Path(
    "docs/applications/xrpl-aquarium-cohort9/demo-manifest.json"
)


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"unable to read manifest: {path}") from exc
    if not isinstance(value, dict):
        raise SystemExit("manifest root must be a JSON object")
    return value


def mutate_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    changed = copy.deepcopy(manifest)
    current = changed.get("artifact_id")
    if isinstance(current, str):
        changed["artifact_id"] = f"{current}-MUTATED"
    else:
        changed["mutation_probe"] = True
    return changed


def public_receipt(
    *,
    verification: dict[str, Any],
    sender: str,
    destination: str,
) -> dict[str, Any]:
    return {
        "network": "XRPL Testnet",
        "rpc": TESTNET_JSON_RPC,
        "status": verification["status"],
        "validated": verification["validated"],
        "transaction_result": verification["transaction_result"],
        "transaction_hash": verification["transaction_hash"],
        "ledger_index": verification["ledger_index"],
        "sender": sender,
        "destination": destination,
        "anchor": verification["anchor"],
        "mutation_probe": "REJECTED_AS_EXPECTED",
        "secrets_persisted": False,
        "mainnet_used": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    payload = build_anchor_payload(
        manifest,
        artifact_schema=str(manifest.get("schema", "cogniprint-evidence-manifest-v0.1")),
    )
    memo_data = encode_memo_data(payload)

    if len(bytes.fromhex(memo_data)) > 900:
        raise SystemExit("anchor memo is unexpectedly large; refusing submission")

    print("NETWORK=XRPL_TESTNET")
    print(f"RPC={TESTNET_JSON_RPC}")
    print("GENERATING_EPHEMERAL_FAUCET_WALLETS")

    client = JsonRpcClient(TESTNET_JSON_RPC)
    sender = generate_faucet_wallet(client, debug=False)
    destination = generate_faucet_wallet(client, debug=False)

    print(f"SENDER={sender.classic_address}")
    print(f"DESTINATION={destination.classic_address}")
    print(f"MANIFEST_COMMITMENT={payload['manifest_commitment']}")
    print("SEEDS_LOGGED=false")

    payment = Payment(
        account=sender.classic_address,
        destination=destination.classic_address,
        amount="1",
        memos=[Memo(memo_data=memo_data)],
    )

    print("SUBMITTING_AND_WAITING_FOR_VALIDATION")
    submit_response = submit_and_wait(payment, client, sender)
    result = submit_response.result
    if not isinstance(result, dict):
        raise SystemExit("unexpected submit response")

    meta = result.get("meta")
    if not isinstance(meta, dict):
        raise SystemExit("validated transaction metadata missing")
    if result.get("validated") is not True:
        raise SystemExit("transaction response is not validated")
    if meta.get("TransactionResult") != "tesSUCCESS":
        raise SystemExit(
            f"validated transaction failed: {meta.get('TransactionResult')}"
        )

    tx_hash = result.get("hash")
    if not isinstance(tx_hash, str) or len(tx_hash) != 64:
        raise SystemExit("validated response did not contain a transaction hash")

    print(f"REAL_TESTNET_TX={tx_hash}")
    print("VALIDATED=true")
    print("TRANSACTION_RESULT=tesSUCCESS")

    independent_response = fetch_transaction(tx_hash)
    verification = verify_validated_receipt(manifest, independent_response)
    if verification.get("status") != "VALIDATED_MATCH":
        raise SystemExit("independent verifier did not return VALIDATED_MATCH")

    print("INDEPENDENT_LEDGER_LOOKUP=PASS")
    print("VALIDATED_MATCH=PASS")

    mutated = mutate_manifest(manifest)
    try:
        verify_validated_receipt(mutated, independent_response)
    except ReceiptError:
        print("MUTATION=FAIL_CLOSED_PASS")
    else:
        raise SystemExit("mutation unexpectedly verified; fail-closed gate failed")

    receipt = public_receipt(
        verification=verification,
        sender=sender.classic_address,
        destination=destination.classic_address,
    )
    if args.receipt_out is not None:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        args.receipt_out.write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"PUBLIC_RECEIPT={args.receipt_out}")

    print("XRPL_REAL_TESTNET_GATE=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
