# Security Policy

CogniPrint is a research framework that processes text-derived evidence, hashes, metadata, manifests, and reproducibility artifacts. Security reports are handled separately from ordinary bug reports.

## Supported versions

Security fixes are targeted first at the current `main` branch and the latest public release. Older releases may receive documentation-only mitigations when a safe patch is not practical.

## Reporting a vulnerability

Please do not open a public issue for a suspected vulnerability that could expose private text, credentials, signing material, unpublished research data, or a practical exploit.

Preferred reporting routes:

1. Use GitHub private vulnerability reporting when it is available for this repository.
2. Otherwise email `roman@cogniprint.org` with the subject `CogniPrint security report`.

Include, where possible:

- affected commit or release;
- affected file, command, dossier, manifest, or integration;
- minimal reproduction steps using synthetic or non-sensitive data;
- expected and observed behaviour;
- impact and realistic attacker capabilities;
- proposed mitigation, if known.

Do not include real private documents, access tokens, API keys, sealed Stage B labels, signing keys, or third-party personal data.

## Response targets

The project aims to:

- acknowledge a credible report within 3 business days;
- provide an initial severity and scope assessment within 7 business days;
- coordinate a remediation and disclosure plan for confirmed vulnerabilities;
- preserve reporter credit when requested and safe.

These are response targets, not a guarantee of a specific fix date.

## Security boundaries

A valid security report may include:

- source-text leakage from evidence exports;
- path traversal, symlink, archive, or unsafe extraction defects;
- manifest or dossier verification bypass;
- signature, hash, canonicalisation, or trust-state confusion;
- command injection or unsafe subprocess execution;
- secret exposure in logs, artifacts, examples, or release exports;
- network activity that violates an offline or local-only contract;
- denial-of-service through malformed or adversarial inputs;
- dependency or build-pipeline compromise;
- privilege escalation in container or self-hosted packaging;
- a claim-firewall bypass that turns unsupported evidence into a stronger conclusion.

Scientific disagreement, weak benchmark performance, or an unsupported research claim should normally be reported as a methodological issue unless it also creates a concrete security or safety impact.

## Coordinated disclosure

Please allow reasonable time for triage and remediation before public disclosure. CogniPrint will not ask reporters to hide unresolved scientific limitations or suppress good-faith criticism.

## Safe research rules

- Use synthetic or publicly licensed fixtures.
- Never test with data you are not authorised to access.
- Do not attempt to obtain sealed labels, private keys, credentials, or unpublished third-party documents.
- Avoid destructive testing against public services.
- Stop testing if it risks exposing personal or confidential information.

## Current non-claims

CogniPrint does not currently claim that text analysis establishes author identity, exact source model, intent, responsibility, legal provenance, or forensic proof. Security fixes must not silently expand those claims.
