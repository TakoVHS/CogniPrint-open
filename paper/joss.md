---
title: 'CogniPrint: A Reproducible Workstation for Compact Statistical Text Profiles'
tags:
  - Python
  - text analysis
  - stylometry
  - reproducibility
  - statistics
authors:
  - name: Roman Adriashkin
    orcid: 0009-0009-6337-1806
    affiliation: 1
affiliations:
  - name: CogniPrint Research Initiative
    index: 1
date: 2026-05-20
bibliography: references.bib
---

# Summary

CogniPrint is an open-source Python research workstation for constructing a
compact statistical profile of a text sample. The central representation is a
12-dimensional feature vector, called a cognitive fingerprint, whose
coordinates include word-length, lexical diversity, entropy, punctuation,
capitalisation, numeric-token, sentence-length, bigram-uniqueness, Simpson
diversity, syllable, and readability summaries.

The package is designed for reproducible descriptive analysis rather than final
categorical conclusions. It includes a Python API, command-line workflows,
Makefile-driven evidence generation, reviewer bundle tooling, public-data
diagnostics, and a small local Streamlit demonstration. The project also ships
claim-boundary checks to keep public language aligned with the current evidence
base.

# Statement of need

Computational text analysis often uses high-dimensional sparse features or
opaque embedding spaces. Those representations are useful, but they can be hard
to inspect, explain, or reproduce in lightweight reviewer settings. CogniPrint
provides a deliberately small and interpretable profile space that can be used
as a baseline, teaching tool, or reproducible diagnostic layer for studying
profile geometry in text collections.

The current repository contains descriptive mathematical diagnostics: PCA-style
geometry summaries, empirical sensitivity checks, length-stability summaries,
TF-IDF and deterministic random-vector baselines, public paraphrase diagnostics
based on PAWS and Hugging Face datasets, and a PAN15-derived cross-genre stress
test [@ZhangEtAl2019PAWS; @PAN15AuthorshipVerificationDataset;
@StamatatosEtAl2015PAN]. These artifacts are generated from documented scripts
and remain bounded to corpus-specific descriptive interpretation.

# Functionality

CogniPrint supports:

- extraction of raw and normalised 12-coordinate profile vectors;
- Euclidean and cosine comparison of profile vectors;
- perturbation and campaign workflows;
- corpus-level summaries and evidence snapshots;
- public-data diagnostic generation;
- reviewer-oriented reproducibility checks;
- a local Streamlit interface for single-text and two-text exploration.

The lightweight core uses the Python standard library plus PyYAML for the main
package. Optional extras are used for public dataset loading and the local demo.

# Research boundary

CogniPrint does not provide author identity decisions, text-origin guarantees,
AI-origin decisions, legal conclusions, or forensic status. The package is a
descriptive research workstation for profile construction, profile comparison,
and reproducible empirical diagnostics.

# Acknowledgements

The project uses public benchmark and dataset resources including PAWS, PAN15,
and Hugging Face-hosted paraphrase datasets. The project currently reports no
external funding.

# References
