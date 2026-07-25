# CogniPrint C2PA / Content Credentials bridge v0.1

Status: **interface and validation contract; a production C2PA reader/validator is not yet implemented.**

Status date: 2026-07-26.

The current C2PA technical specification line is 2.4 (April 2026). CogniPrint treats C2PA/Content Credentials as an external provenance source, not as a replacement for content-derived evidence and not as an infallible truth oracle.

Official specification: https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html

## Design goal

A future bridge should be able to:

1. detect whether Content Credentials / a C2PA manifest are present;
2. validate them with a standards-conformant implementation;
3. preserve validation output without rewriting its meaning;
4. map relevant assertions into CogniPrint `ATTESTED` evidence records;
5. compare attested provenance with statistical/content evidence;
6. emit a conflict state instead of choosing a preferred truth when evidence disagrees.

## C2PA status model

CogniPrint should expose at least:

- `VALIDATED` — the selected standards-conformant validator reports the credential/manifest as valid under its trust configuration;
- `PRESENT_UNVERIFIED` — provenance material is present but has not been validated successfully;
- `INVALID` — validation failed;
- `ABSENT` — no supported C2PA provenance was found;
- `UNSUPPORTED` — a form/version/feature cannot currently be interpreted safely.

The validator name/version and trust configuration must be recorded.

## Evidence mapping

C2PA-derived evidence is **ATTESTED**.

Examples:

```text
ATTESTED: an action assertion says software/tool T performed transform A.
ATTESTED: a validated credential binds a declared provenance record to asset hash H.
```

Do not convert those statements into:

```text
OBSERVED/INFERRED: therefore the prose statistically came from model T.
```

Those are different evidence classes.

## Conflict layer

CogniPrint's conflict engine lives in `src/cogniprint/provenance_conflict.py`.

Conceptual matrix:

| Validated provenance | authorised statistical inference | Result |
| --- | --- | --- |
| A | A | `CONSISTENT` |
| A | B | `PROVENANCE_CONFLICT` |
| none/unverified | A | `STATISTICAL_EVIDENCE_ONLY` |
| A | none/blocked | `ATTESTED_EVIDENCE_ONLY` |
| none | none | `INSUFFICIENT_EVIDENCE` |

A conflict is not resolved by rank alone. The report should preserve both records, validation status, limitations and the unresolved question.

## C2PA is not a universal ground truth

CogniPrint must not describe Content Credentials as absolute truth.

A credential may be:

- absent;
- incomplete;
- invalid under a selected trust configuration;
- limited to the assertions actually present;
- unrelated to a requested actor/intent claim;
- in conflict with other evidence.

The system should therefore report **what was validated**, not a generic "C2PA = true" flag.

## Privacy

Do not ingest arbitrary credential metadata into public evidence artifacts by default.

A future adapter should:

- whitelist mapped fields;
- hash or omit sensitive external identifiers where appropriate;
- record only what is necessary for the analysis/reproducibility purpose;
- preserve the original credential separately when lawful and necessary;
- support zero-retention/local workflows.

## Implementation gate

Do not claim a working C2PA bridge until all are true:

- [ ] a maintained standards-conformant validator is selected and pinned;
- [ ] known-valid, known-invalid, absent and unsupported fixtures are tested;
- [ ] validator/trust-store versions are captured;
- [ ] mapped output conforms to `cogniprint-evidence-v1`;
- [ ] conflicting attested/inferred fixtures produce `PROVENANCE_CONFLICT`;
- [ ] no source credential is silently rewritten into a stronger claim;
- [ ] privacy/redaction behaviour is tested.
