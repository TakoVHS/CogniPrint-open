# EU AI Act Article 50 — evidence mapping for CogniPrint

Status: **research/product mapping only; not legal advice, certification, or a claim of compliance.**

Status date: 2026-07-26.

The European Commission published final guidelines on Article 50 transparency obligations on 2026-07-20. The relevant transparency obligations start to apply on 2026-08-02.

Official source:

- https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems

## Why this matters to CogniPrint

Article 50 increases the practical importance of machine-readable marking and disclosure of certain AI-generated/manipulated content.

CogniPrint must **not** market itself as an "AI Act compliance tool" without legal review and validated implementation.

The appropriate research/product framing is:

> **Evidence reporting aligned with synthetic-content transparency verification workflows.**

## Evidence mapping structure

A future Transparency Audit should distinguish:

| Question | CogniPrint evidence class | Current state |
| --- | --- | --- |
| Artifact hash / analysis version captured? | `OBSERVED` | available in current evidence tooling |
| Machine-readable provenance physically present? | `OBSERVED` | planned C2PA/provenance adapter |
| Provenance validates under selected trust configuration? | `ATTESTED` | planned C2PA bridge |
| Visible disclosure present? | `OBSERVED` only if a dedicated modality-specific checker exists | not implemented for general content |
| Statistical AI/model-family indicators? | `INFERRED` | not enabled under `descriptive_only` |
| Exact model/provider proven? | `ATTESTED` only when external evidence supports it | not inferred from text |
| Evidence sources agree? | conflict result | conflict engine implemented at contract/code level |
| Overall legal compliance? | outside CogniPrint claim scope | must not be asserted |

## Proposed Transparency Audit output

Machine-readable example fields:

```text
machine_readable_provenance: FOUND | NOT_FOUND | UNSUPPORTED
c2pa_status: VALIDATED | PRESENT_UNVERIFIED | INVALID | ABSENT | UNSUPPORTED
visible_disclosure: FOUND | NOT_FOUND | NOT_ASSESSED
statistical_inference: candidate | UNKNOWN | NOT_ENABLED
evidence_consistency: CONSISTENT | PROVENANCE_CONFLICT | INSUFFICIENT_EVIDENCE
limitations: [...]
```

Every field must state how it was obtained and which CogniPrint/versioned adapter produced it.

## What CogniPrint can eventually help verify

Subject to implementation/validation, CogniPrint may help answer narrow technical questions such as:

- whether supported machine-readable provenance is present;
- whether a selected provenance validator accepts or rejects it;
- what declarations/assertions the validated provenance actually contains;
- whether content-derived research signals agree or conflict with attested provenance;
- whether the evidence record is reproducible from the same artifact/configuration.

## What CogniPrint must not claim

Without separate legal analysis and validated scope, do not state:

- "EU AI Act compliant";
- "Article 50 certified";
- "legally compliant content";
- "legal violation detected";
- that absence of a supported marker proves unlawful behaviour;
- that a statistical AI indicator proves a transparency obligation applied to the artifact or actor.

Legal obligations depend on facts and roles beyond a content artifact alone.

## Regulatory mapping template

For any later enterprise/regulatory mapping, use four columns:

1. **Requirement / guideline concept**
2. **Relevant CogniPrint evidence**
3. **What CogniPrint can technically verify**
4. **What remains outside CogniPrint / requires legal or organisational evidence**

This prevents a technical signal from being silently upgraded into a legal conclusion.

## Implementation gate

Before presenting an Article-50-oriented demo:

- [ ] review the final official Article 50 guidelines and applicable Code of Practice version;
- [ ] implement and test machine-readable provenance inspection for the chosen artifact type;
- [ ] implement C2PA validation with pinned validator/trust configuration where relevant;
- [ ] expose `OBSERVED / INFERRED / ATTESTED / UNKNOWN` truth classes;
- [ ] expose `PROVENANCE_CONFLICT` rather than resolving disagreements automatically;
- [ ] include machine-readable limitations;
- [ ] obtain qualified regulatory/legal review before making any compliance claim.
