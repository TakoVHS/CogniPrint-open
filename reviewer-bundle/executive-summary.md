# CogniPrint Reviewer Bundle — Executive Summary

## Purpose

CogniPrint is an open research framework for constructing compact, interpretable statistical profiles of text and studying profile similarity and perturbation stability.

The current public release is a **descriptive measurement framework**. A separate research programme now asks whether the same reproducible foundation can support controlled studies of model-family signals, human–AI intervention, robustness, and provenance fusion. Those extensions are research targets, not validated capabilities.

The purpose of this reviewer bundle is to support a real external methodological review of the implemented framework, its assumptions, its empirical protocol, its reproducibility boundaries, and the design of the proposed next-stage experiments.

## Current public baseline

- Release: `v0.1.2`
- DOI: `10.5281/zenodo.20756421`
- Repository: `https://github.com/TakoVHS/CogniPrint-open`
- Scientific readiness: `descriptive_only`
- External methodological reviews: `0/1`

The DOI is citation/administrative metadata only. Its public availability does not change scientific readiness or validate any stronger research claim.

## What CogniPrint currently claims

CogniPrint claims only a descriptive research status. It defines a feature-map framework for text profiles, comparison metrics for those profiles, controlled perturbation diagnostics, corpus summaries, and reproducible public-data evidence artifacts.

The current release can be inspected as a measurement system. It is not presented as a validated attribution system.

## Research programme under review

The repository also documents falsifiable next-stage work:

1. **Model-family benchmark:** test whether the current and future feature sets contain benchmark-bounded information about known model families, including open-world and transformation failure tests.
2. **Human–AI intervention mapping:** test whether controlled revision chains support reliable localisation of substantial human editing or mixed production processes.
3. **Robustness and abstention:** measure degradation under domain shift, translation, paraphrase, model drift, and unseen models; permit `insufficient evidence` rather than forced attribution.
4. **Provenance fusion:** keep content-derived measurements separate from authenticated hashes, revision history, signed credentials, and tool/workflow records.

None of those items is a current validated product claim.

## What CogniPrint does not claim

CogniPrint does not currently establish:

- authorship or identity;
- a unique source model;
- definitive AI origin;
- who requested, commissioned, approved, or deployed an action;
- intent or responsibility;
- legal status or forensic provenance;
- universal classification accuracy;
- operational readiness for high-stakes decisions.

## Reviewer request

A reviewer is asked to evaluate both:

- whether the **current descriptive core** is methodologically clear and responsibly bounded; and
- whether the **proposed research programme** has appropriate baselines, leakage controls, calibration/abstention requirements, failure criteria, and provenance boundaries before any stronger claim is considered.

Endorsement is not requested. A negative or mixed assessment is useful evidence.

## Entry points

- Public repository: `https://github.com/TakoVHS/CogniPrint-open`
- Release: `https://github.com/TakoVHS/CogniPrint-open/releases/tag/v0.1.2`
- DOI: `https://doi.org/10.5281/zenodo.20756421`
- Current state: `docs/current-state-summary.md`
- Research vision: `docs/research-vision.md`
- Model-fingerprint protocol: `docs/model-fingerprint-benchmark-v0.1.md`
- External-review request: `docs/external-review.md`
- Reviewer response template: `docs/reviewer-response-template.md`
- Manuscript source: `paper/main.tex`
- Evidence dossier: `docs/evidence-dossier.md`
