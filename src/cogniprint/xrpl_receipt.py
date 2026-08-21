"""Independent verification of CogniPrint XRPL evidence-anchor receipts.

This module is intentionally read-only with respect to the XRP Ledger. It can
query a public JSON-RPC endpoint for an existing transaction hash, but it never
creates wallets, signs transactions, submits transactions, or handles secrets.
"""

from __future__ import annotations

import json
import re
from typing import Any, Mapping
from urllib import error, request

from cogniprint.xrpl_anchor import ANCHOR_SCHEMA, verify_anchor_payload

TESTNET_JSON_RPC = "https://s.altnet.rippletest.net:51234/"
MAX_MEMO_DATA_BYTES = 1024
_TX_HASH_RE = re.compile(r"^[0-9A-Fa-f]{64}$")


class ReceiptError(ValueError):
    """Raised when ledger evidence is missing, ambiguous, or inconsistent."""


def decode_memo_data(memo_data: str) -> dict[str, Any]:
    """Decode one XRPL MemoData hex string into a JSON object, fail closed."""

    if not isinstance(memo_data, str) or len(memo_data) % 2:
        raise ReceiptError("MemoData must be an even-length hex string")
    try:
        raw = bytes.fromhex(memo_data)
    except ValueError as exc:
        raise ReceiptError("MemoData is not valid hex") from exc
    if len(raw) > MAX_MEMO_DATA_BYTES:
        raise ReceiptError("MemoData exceeds the verifier safety limit")
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReceiptError("MemoData is not UTF-8 JSON") from exc
    if not isinstance(payload, dict):
        raise ReceiptError("MemoData JSON must be an object")
    return payload


def _unwrap_result(response: Mapping[str, Any]) -> Mapping[str, Any]:
    if not isinstance(response, Mapping):
        raise ReceiptError("XRPL response must be an object")
    if "error" in response and "result" not in response:
        raise ReceiptError(f"XRPL RPC error: {response.get('error')}")
    result = response.get("result", response)
    if not isinstance(result, Mapping):
        raise ReceiptError("XRPL result must be an object")
    if result.get("error"):
        raise ReceiptError(f"XRPL RPC error: {result.get('error')}")
    return result


def _transaction_json(result: Mapping[str, Any]) -> Mapping[str, Any]:
    """Support current API v2 tx_json plus legacy API v1 result shape."""

    tx_json = result.get("tx_json")
    if isinstance(tx_json, Mapping):
        return tx_json
    return result


def extract_cogniprint_anchor(response: Mapping[str, Any]) -> dict[str, Any]:
    """Extract exactly one CogniPrint anchor from a validated successful tx."""

    result = _unwrap_result(response)
    if result.get("validated") is not True:
        raise ReceiptError("transaction is not from a validated ledger")

    meta = result.get("meta")
    if not isinstance(meta, Mapping):
        raise ReceiptError("validated transaction metadata is missing")
    if meta.get("TransactionResult") != "tesSUCCESS":
        raise ReceiptError("validated transaction result is not tesSUCCESS")

    tx_json = _transaction_json(result)
    memos = tx_json.get("Memos")
    if not isinstance(memos, list):
        raise ReceiptError("transaction does not contain Memos")

    candidates: list[dict[str, Any]] = []
    for entry in memos:
        if not isinstance(entry, Mapping):
            continue
        memo = entry.get("Memo")
        if not isinstance(memo, Mapping):
            continue
        memo_data = memo.get("MemoData")
        if not isinstance(memo_data, str):
            continue
        try:
            payload = decode_memo_data(memo_data)
        except ReceiptError:
            continue
        if payload.get("schema") == ANCHOR_SCHEMA:
            candidates.append(payload)

    if not candidates:
        raise ReceiptError("CogniPrint anchor memo not found")
    if len(candidates) != 1:
        raise ReceiptError("multiple CogniPrint anchor memos are ambiguous")
    return candidates[0]


def verify_validated_receipt(
    manifest: Mapping[str, Any],
    response: Mapping[str, Any],
) -> dict[str, Any]:
    """Verify ledger finality and bind one local manifest to one anchor memo."""

    result = _unwrap_result(response)
    payload = extract_cogniprint_anchor(response)
    if not verify_anchor_payload(manifest, payload):
        raise ReceiptError("manifest commitment does not match validated anchor")

    tx_json = _transaction_json(result)
    transaction_hash = result.get("hash") or tx_json.get("hash")
    ledger_index = result.get("ledger_index") or tx_json.get("ledger_index")

    return {
        "status": "VALIDATED_MATCH",
        "validated": True,
        "transaction_result": "tesSUCCESS",
        "transaction_hash": transaction_hash,
        "ledger_index": ledger_index,
        "anchor": payload,
    }


def fetch_transaction(
    transaction_hash: str,
    *,
    rpc_url: str = TESTNET_JSON_RPC,
    timeout: float = 10.0,
) -> dict[str, Any]:
    """Read one transaction by hash from an XRPL JSON-RPC endpoint."""

    if not isinstance(transaction_hash, str) or _TX_HASH_RE.fullmatch(transaction_hash) is None:
        raise ReceiptError("transaction hash must be 64 hexadecimal characters")
    if not isinstance(rpc_url, str) or not rpc_url.startswith("https://"):
        raise ReceiptError("rpc_url must use https")

    body = json.dumps(
        {
            "method": "tx",
            "params": [
                {
                    "transaction": transaction_hash.upper(),
                    "binary": False,
                }
            ],
        }
    ).encode("utf-8")
    http_request = request.Request(
        rpc_url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(http_request, timeout=timeout) as response:
            raw = response.read()
    except (error.HTTPError, error.URLError, TimeoutError) as exc:
        raise ReceiptError("XRPL RPC lookup failed") from exc

    try:
        decoded = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReceiptError("XRPL RPC returned invalid JSON") from exc
    if not isinstance(decoded, dict):
        raise ReceiptError("XRPL RPC returned a non-object response")
    return decoded
