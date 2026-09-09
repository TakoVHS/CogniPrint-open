---
title: 'CogniPrint: Reproducible statistical text profiles for evidence-oriented synthetic-language research'
tags:
  - Python
  - text analysis
  - stylometry
  - reproducible research
  - content provenance
  - synthetic language
authors:
  - name: Roman Adriashkin
    orcid: 0009-0009-6337-1806
    affiliation: 1
affiliations:
  - name: CogniPrint Research Initiative, Independent Research
    index: 1
date: 09 September 2026
bibliography: paper.bib
---

# Summary

CogniPrint is an open-source research software framework for constructing compact, interpretable statistical profiles of text and studying how those profiles behave under controlled comparisons and transformations. The software is intended for researchers who need reproducible measurements of textual structure without collapsing the result into a single unsupported verdict such as “AI-generated” or “human-written.”

At its current scientific readiness level, CogniPrint is deliberately descriptive. It computes a documented 12-dimensional profile, supports Euclidean and cosine profile comparisons, controlled perturbation analysis, corpus aggregation and dispersion measurements, entropy and word/character n-gram analysis, and reproducible diagnostic runs on public datasets. The project also records explicit failure boundaries and supports an `UNKNOWN / insufficient evidence` outcome when stronger claims are not justified.

The long-term research programme studies what measurable traces survive across human and model-mediated production chains. The software itself does not establish author identity, a unique source model, definitive AI origin, legal or forensic provenance, or intent. These non-claims are part of the software design rather than post-hoc disclaimers.

# Statement of need

Text that reaches a researcher or auditor may have passed through editing, paraphrasing, translation, multiple language models, publishing systems, or human revision. In such settings, binary origin labels are often too coarse. Researchers need tools that preserve the distinction between what was measured, what was inferred from a reference set, what was externally attested, and what remains unknown.

CogniPrint addresses this need by providing a small, reproducible measurement layer for text-profile research. A text sample $T$ is mapped to an interpretable finite-dimensional profile $\phi(T)$. Researchers can compare profiles, study stability under bounded edits, evaluate corpus-relative geometry, and export evidence artifacts with versioned configuration and provenance metadata. The emphasis is on reproducibility and inspectability rather than opaque prediction.

The software is useful for experiments in stylometry, robustness analysis, synthetic-language research, human–AI coauthoring studies, evaluation of transformation effects, and provenance-oriented research where content-derived evidence must remain distinct from authenticated external provenance.

# State of the field

Quantitative style analysis has a long history, from early composition curves [@Mendenhall1887] to modern stylometry [@Holmes1998]. The `stylo` package provides mature computational-stylometry workflows in R [@EderEtAl2016], and standard vector-space and n-gram methods remain strong transparent baselines in language analysis [@ManningEtAl2008]. CogniPrint does not aim to replace these tools or claim a generally superior classifier.

Its build-vs-contribute justification is narrower: CogniPrint couples a compact interpretable profile with controlled perturbation measurements, explicit evidence classes (`OBSERVED`, `INFERRED`, `ATTESTED`, `UNKNOWN`), versioned evidence artifacts, failure-first reporting, and research-governance gates that keep software maturity separate from stronger provenance or attribution claims. Conventional stylometric and n-gram methods remain comparison baselines rather than targets for replacement.

The current public diagnostics use established public resources, including PAWS [@ZhangEtAl2019PAWS], Russian paraphrase datasets, and PAN15 authorship-verification material [@StamatatosEtAl2015PAN]. These datasets are used to test whether the implemented geometry can be reproduced and stress-tested under documented conditions; they are not treated as proof of universal attribution capability.

# Software design

CogniPrint is implemented as a Python package with a command-line entry point and reproducible research scripts. The core package exposes the profile construction and comparison logic, while validation scripts produce versioned CSV, JSON, and figure artifacts for defined diagnostic runs.

The current software includes:

- a documented 12-dimensional interpretable profile $\phi(T)$;
- Euclidean-distance and cosine-similarity comparison;
- controlled perturbation measurements $\Delta\phi$;
- corpus aggregation and dispersion summaries;
- entropy and word/character n-gram analysis;
- leakage-aware baseline evaluation infrastructure;
- public-data diagnostic scripts and seed-fixture smoke tests;
- evidence artifacts that record configuration, source, version, and non-claim boundaries;
- an evidence-oriented vocabulary separating `OBSERVED`, `INFERRED`, `ATTESTED`, and `UNKNOWN` states.

The project is distributed under the MIT License and supports Python 3.10–3.12 in the current package metadata. Reproduction commands and validation targets are maintained in the repository. The design intentionally keeps the mathematical manuscript, software validation artifacts, and future attribution research gates separate so that software maturity cannot be mistaken for scientific validation of stronger claims.

# Research impact statement

CogniPrint is designed as research infrastructure rather than a finished high-stakes classifier. Its current realized use is within the public CogniPrint research programme: the package and scripts generate and audit statistical profiles, controlled comparisons, public-data diagnostics, and benchmark artifacts used to test the framework itself.

A concrete public result is the fixed Stage A descriptive pilot, where simple hashed TF-IDF baselines outperform the current 12D nearest-centroid representation. That negative result is retained because it constrains the software’s present role rather than being hidden.

External adoption remains an open gate rather than an asserted success. Before JOSS submission the project will document any external reproductions, integrations, citations, or research use that actually occurs. Attribution Challenge 001 is a planned blind preregistered experiment and is not presented as a validated feature of the current release.

# AI usage disclosure

Generative-AI assistants, including ChatGPT and coding-assistant tooling, have been used during parts of CogniPrint development and publication preparation. They have assisted with code review and refactoring suggestions, documentation drafting, research-operations checklists, manuscript editing, and inspection of repository or deployment state.

Retained AI-assisted material remains the responsibility of the maintainer. Code changes are reviewed against the intended repository contract and are accepted only after available tests or reproducibility checks. Scientific statements are checked against versioned repository evidence, explicit evidence classes, failure/non-claim rules, and cited external sources where applicable. AI output is not treated as independent authorship, peer review, methodological validation, or evidence of correctness. The disclosure will be re-audited against the actual tools used through the final candidate release date.

# Acknowledgements

The author thanks the maintainers of the public datasets and open-source tools used in the reproducibility and diagnostic workflow. No sponsorship, grant award, or external methodological endorsement is claimed by this paper draft unless separately documented in the repository at submission time.

# References
