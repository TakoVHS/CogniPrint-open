import unittest

from cogniprint.xrpl_anchor import build_anchor_payload, encode_memo_data
from cogniprint.xrpl_receipt import ReceiptError, verify_validated_receipt


class XrplReceiptTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {
            "artifact_id": "case-001",
            "schema": "cogniprint-evidence-manifest-v0.1",
            "files": [{"path": "report.json", "sha256": "a" * 64}],
        }
        payload = build_anchor_payload(
            self.manifest,
            artifact_schema="cogniprint-evidence-manifest-v0.1",
        )
        self.response = {
            "result": {
                "validated": True,
                "hash": "A" * 64,
                "ledger_index": 123456,
                "meta": {"TransactionResult": "tesSUCCESS"},
                "tx_json": {
                    "TransactionType": "Payment",
                    "Memos": [{"Memo": {"MemoData": encode_memo_data(payload)}}],
                },
            }
        }

    def test_validated_match(self):
        receipt = verify_validated_receipt(self.manifest, self.response)
        self.assertEqual(receipt["status"], "VALIDATED_MATCH")
        self.assertEqual(receipt["transaction_hash"], "A" * 64)
        self.assertEqual(receipt["ledger_index"], 123456)

    def test_mutation_fails(self):
        changed = dict(self.manifest)
        changed["artifact_id"] = "case-002"
        with self.assertRaisesRegex(ReceiptError, "commitment"):
            verify_validated_receipt(changed, self.response)

    def test_unvalidated_fails(self):
        self.response["result"]["validated"] = False
        with self.assertRaisesRegex(ReceiptError, "validated ledger"):
            verify_validated_receipt(self.manifest, self.response)

    def test_non_success_fails(self):
        self.response["result"]["meta"]["TransactionResult"] = "tecFAILED_PROCESSING"
        with self.assertRaisesRegex(ReceiptError, "tesSUCCESS"):
            verify_validated_receipt(self.manifest, self.response)

    def test_missing_memo_fails(self):
        self.response["result"]["tx_json"].pop("Memos")
        with self.assertRaisesRegex(ReceiptError, "Memos"):
            verify_validated_receipt(self.manifest, self.response)

    def test_multiple_anchor_memos_fail_as_ambiguous(self):
        memo = self.response["result"]["tx_json"]["Memos"][0]
        self.response["result"]["tx_json"]["Memos"].append(memo)
        with self.assertRaisesRegex(ReceiptError, "ambiguous"):
            verify_validated_receipt(self.manifest, self.response)

    def test_legacy_v1_shape_supported(self):
        result = self.response["result"]
        legacy = {
            "result": {
                "validated": result["validated"],
                "hash": result["hash"],
                "ledger_index": result["ledger_index"],
                "meta": result["meta"],
                "TransactionType": "Payment",
                "Memos": result["tx_json"]["Memos"],
            }
        }
        receipt = verify_validated_receipt(self.manifest, legacy)
        self.assertEqual(receipt["status"], "VALIDATED_MATCH")


if __name__ == "__main__":
    unittest.main()
