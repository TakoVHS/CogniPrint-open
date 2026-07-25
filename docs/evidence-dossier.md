# CogniPrint evidence dossier

## Current evidence claim

CogniPrint computes an interpretable statistical feature vector for text and compares vectors using documented distance, similarity, perturbation, entropy, and n-gram measurements.

Public evidence includes bounded benchmark material, controlled perturbation outputs, descriptive validation artifacts, mathematical diagnostics, tests, and manuscript source.

## What this evidence currently supports

The public package supports the claim that CogniPrint can produce **reproducible descriptive fingerprints of text** under the documented feature map and can measure how those fingerprints vary across samples and controlled edits.

It does not yet support a validated attribution claim.

## Research direction supported by the current architecture

The current evidence layer is intended to become the measurable-content component of a broader synthetic-language provenance programme. Future validation work may test:

- probabilistic attribution to known model families under controlled closed-set benchmarks;
- localisation of human–AI coauthoring or substantial editing;
- robustness under paraphrase, translation, and revision;
- fusion of content measurements with external provenance records such as signed metadata, hashes, tool logs, and C2PA-style credentials.

Those are research targets, not current capabilities.

## Non-claims

All current outputs are descriptive research measurements. They are not conclusions about:

- identity or authorship;
- a unique source model;
- definitive AI origin;
- the person or organisation that commissioned a generation action;
- intent or responsibility;
- legal status;
- forensic provenance suitable for high-stakes use.

Actor or workflow attribution requires independent provenance evidence and cannot responsibly be inferred from text alone.
