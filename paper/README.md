# Paper Directory

This directory contains the manuscript layer for CogniPrint.

## Files

- `main.tex` — the current LaTeX manuscript scaffold.
- `references.bib` — the BibTeX reference database for the manuscript.
- `joss.md` — short Journal of Open Source Software draft stub.
- `README.md` — overview of the manuscript layer.
- `NOTES.md` — editorial notes and next writing tasks.

## Current status

The manuscript is an early research draft. It already contains:
- title, author, and ORCID block;
- abstract;
- introduction;
- formal setting;
- stability sections;
- limitations;
- empirical protocol;
- conclusion and open problems;
- appendix scaffold;
- an initial verified bibliography layer.

## Build notes

The checked build target is:

```bash
cd /home/vietcash/projects/CogniPrint
make paper-build
```

`make paper-build` uses local `latexmk` when available. If local TeX is not installed but Docker is available, it falls back to the `texlive/texlive:latest` container.

A minimal manual local build flow is:

```bash
cd paper
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

If `latexmk` is available, an equivalent one-command flow is:

```bash
cd paper
latexmk -pdf main.tex
```

Last verified container build:

```bash
docker run --rm \
  -v /home/vietcash/projects/CogniPrint/paper:/work \
  -w /work \
  texlive/texlive:latest \
  latexmk -pdf -interaction=nonstopmode main.tex
```

Verification date: 2026-05-04. Output: `paper/main.pdf` built successfully.

## Editorial rule

No sentence in the manuscript should make a stronger claim than is supported by:
- a formal theorem with assumptions;
- a proof or proof sketch;
- a documented empirical result;
- or a clearly labelled open question.
