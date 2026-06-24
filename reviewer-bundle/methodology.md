# CogniPrint Reviewer Bundle — Methodology

## Formal object

CogniPrint represents a text sample as a finite-dimensional statistical profile. A feature map maps token sequences into a vector space, and the resulting vector is treated as the text profile or cognitive fingerprint.

## Comparison layer

The framework compares profiles using geometric quantities such as Euclidean distance and cosine similarity. These measurements are descriptive and are not classification decisions.

## Stability layer

Perturbation analysis is conditional. Stability statements depend on explicit coordinate-wise Lipschitz assumptions and non-degeneracy assumptions for the selected feature family and analysis regime.

## Empirical layer

The public empirical layer is a diagnostic layer. It is intended to test whether the implemented pipeline can run reproducibly on public data and whether profile geometry can be inspected under controlled comparisons.

## Reviewer focus

Please review:

1. whether the feature-map abstraction is clearly defined;
2. whether the perturbation assumptions are stated narrowly enough;
3. whether the stability statements follow from the assumptions;
4. whether the empirical protocol is reproducible;
5. whether the limitations prevent over-interpretation;
6. whether any stronger claim appears unsupported.

## Claims boundary

The methodology should be read as a descriptive mathematical and empirical framework. It should not be read as an authorship attribution system, AI-origin detector, forensic tool, or legal-status classifier.
