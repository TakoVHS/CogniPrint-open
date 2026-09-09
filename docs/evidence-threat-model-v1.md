# Self-Hosted Evidence Workstation — Threat Model v1

Status: `DEVELOPMENT_ONLY`

Scientific boundary:

- `SCIENTIFIC_CLAIM_EVIDENCE=false`
- `CANONICAL_FREEZE=PRE-FREEZE`
- `EXTERNAL_REGISTRATION=NOT_SUBMITTED`
- `STAGE_B=NOT_AUTHORISED_TO_START`

## Scope

This model covers local export, transport and offline verification of CogniPrint evidence dossier v1. It does not claim protection against a compromised operating system, kernel, administrator account, Python runtime or physical attacker.

## Assets

1. Raw source text and local configuration, which must remain outside the dossier.
2. Dossier integrity: canonical manifest, artifact inventory, byte lengths and SHA-256 values.
3. Operator workspace contents outside CogniPrint-owned temporary directories.
4. Availability of the verifier under malformed or oversized input.
5. The fixed scientific claim boundary.

## Trust boundaries

- **Producer installation:** reads local source and artifacts, creates the dossier.
- **Transport boundary:** the dossier may pass through untrusted storage or another person.
- **Verifier installation:** receives only the dossier and must not contact a CogniPrint service.
- **Local filesystem:** may contain symlinks, special files, mount points or concurrent modifications.
- **Package and base-image supply chain:** Nix input, Python base digest and Python build dependencies remain external trust anchors even when pinned.

## Threat actors and failure modes

| Threat | Required control | M3 treatment |
|---|---|---|
| Malicious dossier sender | Fail closed on malformed content | Exact keys, canonical JSON, duplicate-key rejection, fixed schema and claim boundary |
| Path traversal or symlink escape | Never follow attacker-controlled links | Normalized relative artifact paths, `O_NOFOLLOW` where available, bounded non-following inventory |
| JSON nesting or directory-tree exhaustion | Bound work before deep parsing/traversal | Manifest byte cap, JSON nesting cap, tree depth and entry caps |
| Oversized source or artifacts | Bound read and copy volume | Per-file, aggregate and artifact-count limits |
| Concurrent mutation | Detect inconsistent reads | Descriptor identity checks plus before/after inventory comparison |
| Special filesystem object | Reject non-regular content | FIFOs, devices and unsupported entries fail closed |
| Accidental deletion | Delete only owned temporary names | Direct-child prefix allowlist, precomputed deletion plan and filesystem-boundary rejection |
| Symlink deletion trap | Unlink the link, not its target | Temporary-root symlinks are removed without traversal |
| Network disclosure during verification | Verifier must be offline-capable | Standard-library-only verification path and a cross-installation network guard |
| Source/configuration disclosure | Export hashes only | Raw source and configuration content remain excluded and are regression-tested |
| Claim expansion | Preserve fixed semantics | `DEVELOPMENT_ONLY`, false scientific-evidence flag and immutable claim boundary |

## Temporary-data deletion semantics

`cogniprint dossier purge-temp` performs **logical deletion** by unlinking files and removing directories after a complete bounded pre-scan. It only considers direct workspace children whose names begin with `.cogniprint-dossier-`.

This is not cryptographic erasure. SSD wear levelling, copy-on-write filesystems, snapshots, backups, journaling and privileged recovery may retain data. Sensitive operators should use encrypted storage and destroy encryption keys according to their own policy.

## Residual risks

- SHA-256 establishes integrity against the manifest, not signer identity or authenticity.
- No trusted timestamp or remote attestation is provided.
- A privileged local attacker can race or replace the runtime itself.
- Pinned dependencies reduce drift but do not prove that upstream artifacts are benign.
- Resource limits protect this implementation profile; operators may need stricter limits on constrained systems.
- The dossier does not support legal, forensic, disciplinary, authorship or deterministic model-source conclusions.

## Review gates

Before Ready or merge consideration:

1. independent security review of deletion and traversal assumptions;
2. independent review of dossier authenticity requirements;
3. operator usability review on Linux and at least one second supported platform;
4. confirmation that no new network path is introduced by future UI/service integration.
