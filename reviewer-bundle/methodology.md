# CogniPrint Reviewer Bundle — Methodology

## Formal object — implemented

CogniPrint represents a text sample as a finite-dimensional statistical profile. A feature map maps token sequences into a vector space, and the resulting vector is treated as the text profile or cognitive fingerprint.

The public implementation currently uses a documented versioned 12-coordinate profile. The broader mathematical formalism does not imply that these coordinates uniquely identify a person, model, or production process.

## Comparison layer — implemented

The framework compares profiles using geometric quantities such as Euclidean distance and cosine similarity. These measurements are descriptive and are not classification decisions.

## Stability layer — implemented/conditional

Perturbation analysis is conditional. Stability statements depend on explicit coordinate-wise Lipschitz assumptions and non-degeneracy assumptions for the selected feature family and analysis regime.

The assumptions are part of the statement; they are not evidence that arbitrary text transformations preserve a fingerprint.

## Empirical layer — implemented descriptive diagnostics

The public empirical layer is a diagnostic layer. It is intended to test whether the implemented pipeline can run reproducibly on public data and whether profile geometry can be inspected under controlled comparisons.

Existing corpus-specific diagnostics do not establish general classification accuracy.

## External model-family pilot — research infrastructure, no result yet

The repository now includes an M1 adapter and evaluation protocol for an independently maintained RAID dataset revision.

The pilot is designed to ask a falsifiable question: under controlled conditions, do current CogniPrint features contain benchmark-bounded information associated with known model-family labels beyond simple baselines?

The design includes:

- pinned external data revision;
- controlled model/domain/decoding selection;
- hashes and lineage metadata without committing raw RAID text;
- grouped train/test splitting intended to reduce source/prompt leakage;
- majority and length-only controls;
- a transparent 12D nearest-centroid baseline;
- planned n-gram, robustness, open-world, calibration, and abstention stages.

No RAID empirical result is currently claimed. The infrastructure is itself available for methodological criticism.

## Human–AI intervention — proposed research target

A separate proposed research direction asks whether controlled revision chains can support sentence/span-level or change-point analysis of substantial human editing in machine-assisted documents.

No implemented current-release output is described as a validated human–AI intervention map. A reviewer is specifically asked to challenge whether the construct, ground truth, segmentation unit, and failure criteria are scientifically meaningful.

## Provenance layer — evidence-class separation

CogniPrint treats two evidence classes separately:

1. **content-derived measurements** — statistical properties observed in the artifact;
2. **authenticated/declared provenance** — hashes, signed credentials, revision history, publication records, or tool/workflow records where legitimately available.

A content-derived similarity score must not be silently upgraded into an authenticated provenance fact.

Actor, commissioner, approval, or workflow identity can enter a future provenance graph only when independent records support it. Such identity is not inferred from prose alone.

## Local explanation prototype — non-scientific evidence transformation

The experimental QVAC integration consumes a whitelisted CogniPrint evidence envelope and may generate a local human-readable explanation. The generative explanation layer is not permitted to alter the deterministic measurements or create stronger scientific evidence.

The QVAC runtime itself is not yet recorded as validated in the public evidence state.

## Reviewer focus

Please review:

1. whether the feature-map abstraction is clearly defined;
2. whether the perturbation assumptions are stated narrowly enough;
3. whether the stability statements follow from the assumptions;
4. whether the current empirical protocol is reproducible;
5. whether the M1 split/baseline protocol sufficiently guards against leakage and trivial confounders;
6. whether open-world, calibration, abstention, and transformation tests are adequate before stronger claims;
7. whether human–AI intervention is a defensible construct with obtainable ground truth;
8. whether content measurements and authenticated provenance are kept conceptually separate;
9. whether the limitations prevent over-interpretation;
10. whether any stronger claim appears unsupported.

## Claims boundary

The current methodology should be read as a descriptive mathematical and empirical framework plus documented experimental extensions.

It should **not** be read as a validated authorship system, exact-model identifier, AI-origin oracle, actor/commissioner identifier, legal-status classifier, or forensic provenance system.