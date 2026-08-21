import math
import unittest

from cogniprint.xrpl_anchor import (
    ANCHOR_SCHEMA,
    AnchorError,
    build_anchor_payload,
    canonical_json_bytes,
    encode_memo_data,
    manifest_commitment,
    verify_anchor_payload,
)


class XrplAnchorTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {
            "artifact_id": "case-001",
            "schema": "cogniprint-evidence-manifest-v0.1",
            "files": [
                {"path": "report.json", "sha256": "a" * 64},
                {"path": "metrics.json", "sha256": "b" * 64},
            ],
        }

    def test_canonicalization_is_key_order_independent(self):
        left = {"b": 2, "a": 1}
        right = {"a": 1, "b": 2}
        self.assertEqual(canonical_json_bytes(left), canonical_json_bytes(right))
        self.assertEqual(manifest_commitment(left), manifest_commitment(right))

    def test_build_and_verify(self):
        payload = build_anchor_payload(
            self.manifest,
            artifact_schema="cogniprint-evidence-manifest-v0.1",
        )
        self.assertEqual(payload["schema"], ANCHOR_SCHEMA)
        self.assertTrue(verify_anchor_payload(self.manifest, payload))

    def test_manifest_mutation_fails_verification(self):
        payload = build_anchor_payload(
            self.manifest,
            artifact_schema="cogniprint-evidence-manifest-v0.1",
        )
        changed = dict(self.manifest)
        changed["artifact_id"] = "case-002"
        self.assertFalse(verify_anchor_payload(changed, payload))

    def test_malformed_commitment_fails_closed(self):
        payload = build_anchor_payload(
            self.manifest,
            artifact_schema="cogniprint-evidence-manifest-v0.1",
        )
        payload["manifest_commitment"] = "not-a-hash"
        self.assertFalse(verify_anchor_payload(self.manifest, payload))
        with self.assertRaises(AnchorError):
            encode_memo_data(payload)

    def test_unknown_schema_fails_closed(self):
        payload = build_anchor_payload(
            self.manifest,
            artifact_schema="cogniprint-evidence-manifest-v0.1",
        )
        payload["schema"] = "future-schema"
        self.assertFalse(verify_anchor_payload(self.manifest, payload))

    def test_non_finite_json_is_rejected(self):
        with self.assertRaises(AnchorError):
            manifest_commitment({"score": math.nan})
        with self.assertRaises(AnchorError):
            manifest_commitment({"score": math.inf})

    def test_memo_encoding_is_hex_round_trip(self):
        payload = build_anchor_payload(
            self.manifest,
            artifact_schema="cogniprint-evidence-manifest-v0.1",
        )
        memo_hex = encode_memo_data(payload)
        decoded = bytes.fromhex(memo_hex)
        self.assertEqual(decoded, canonical_json_bytes(payload))


if __name__ == "__main__":
    unittest.main()
