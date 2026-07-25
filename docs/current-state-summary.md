# CogniPrint current state

CogniPrint is an MIT-licensed research framework for constructing compact statistical fingerprints of text and studying how those fingerprints behave under comparison, perturbation, and corpus aggregation.

## Current scientific status

- Scientific readiness: `descriptive_only`
- External methodological reviews: `0/1`
- Release line: `v0.1.2`
- DOI: pending direct public Zenodo verification
- Repository: https://github.com/TakoVHS/CogniPrint-open

The current public release supports reproducible **measurement**, not definitive attribution.

## What is implemented

CogniPrint currently provides:

- a documented 12-dimensional text profile `φ(T)`;
- profile comparison with Euclidean distance and cosine similarity;
- corpus-relative exploratory thresholds and p-value diagnostics;
- perturbation analysis for measuring profile change under edits;
- corpus aggregation and dispersion summaries;
- Shannon entropy measurements;
- word/character n-gram analysis;
- reproducibility, validation, benchmark, and evidence artifacts.

These components form the present mathematical and experimental core.

## What the research is trying to reach

The broader programme asks whether measurable text fingerprints can contribute to a future provenance stack for synthetic language:

1. **Model-family attribution:** test whether known generative-model families produce sufficiently stable, distinguishable output patterns under controlled conditions.
2. **Human–AI intervention mapping:** test whether mixed human/machine documents can be segmented or revision chains can reveal where substantial human editing occurred.
3. **Provenance reconstruction:** combine content-derived measurements with external evidence such as signed metadata, document history, model/tool logs, hashes, and C2PA-style credentials.
4. **Workflow attribution:** where trustworthy external provenance exists, reconstruct which tool performed an action and which declared actor initiated or approved a workflow.

Items 1–4 are research targets unless and until supported by dedicated validation evidence.

## Critical boundary

CogniPrint does **not** currently infer from text alone:

- a unique author;
- a unique source model;
- definitive AI origin;
- who commissioned or requested the generation;
- intent, responsibility, or legal status;
- forensic provenance suitable for high-stakes decisions.

The distinction matters scientifically. Content-derived signals can support hypotheses; claims about actors, tools, and workflow history require independent provenance evidence.

## Positioning

CogniPrint should be understood as a **reproducible research programme for synthetic-language fingerprints and provenance**, with a conservative implemented core and a clearly separated future validation roadmap.

The project remains bounded to descriptive measurement until evidence justifies expanding its public claim scope.
