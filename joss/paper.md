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
date: 06 September 2026
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

Quantitative style analysis has a long history, from early composition curves [@Mendenhall1887] to modern stylometry [@Holmes1998; @EderEtAl2016]. Vector-space representations and distance-based comparison are also standard tools in information retrieval and language analysis [@ManningEtAl2008]. CogniPrint does not replace these traditions. Instead, it packages a deliberately compact and interpretable profile representation together with perturbation diagnostics, explicit evidence classes, reproducibility artifacts, and conservative abstention boundaries.

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

CogniPrint is designed as research infrastructure rather than a finished high-stakes classifier. Its immediate research value is to make profile construction, profile comparison, perturbation experiments, baseline checks, and failure reporting easier to reproduce and audit.

The public repository already contains reproducibility scripts, benchmark material, a mathematical manuscript, controlled public-data diagnostics, an attribution-challenge protocol, a fingerprint-registry specification, and an explicit failure charter. This makes it possible for external researchers to inspect not only successful measurements but also the conditions under which stronger interpretation must stop.

A central planned use is Attribution Challenge 001, a blind, preregistration-oriented experiment designed to test or falsify model-family fingerprint hypotheses under balanced source families, unseen-family evaluation, paraphrase, translation, human editing, and AI-to-AI rewriting. Importantly, this future research programme is not presented as a validated feature of the current release.

# AI usage disclosure

Generative AI tools have been used as development assistants for portions of code review, refactoring, documentation drafting, research-operations planning, and manuscript editing. Retained changes remain the responsibility of the project maintainer and are subject to repository review, tests, reproducibility checks, and explicit scientific-claim boundaries. AI-generated text or code is not treated as independent scientific validation, methodological review, or evidence of correctness.

# Acknowledgements

The author thanks the maintainers of the public datasets and open-source tools used in the reproducibility and diagnostic workflow. No sponsorship, grant award, or external methodological endorsement is claimed by this paper draft unless separately documented in the repository at submission time.

# References
