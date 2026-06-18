# CogniPrint arXiv v1 package

This directory contains the manuscript source for the first arXiv preprint
package of CogniPrint.

## Compile locally

From inside the unpacked arXiv package:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

If your LaTeX environment does not run BibTeX automatically, keep
`references.bib` in the same directory as `main.tex`.

## Package contents

- `main.tex` - manuscript source.
- `references.bib` - bibliography.
- `arxiv-abstract.txt` - plain-text abstract for the arXiv submission form.
- `figures/*.pdf` - static PDF figures generated from frozen validation CSVs.
- `README-for-arxiv.md` - this file.

The arXiv archive intentionally does not include source code or datasets. The
reproducible code and data artifacts remain in the project repository under
`scripts/` and `validation/`.

## Rebuild package from repository

From the repository root:

```bash
make arxiv-package
```

This regenerates the arXiv-safe PDF figures and writes:

```text
release_artifacts/cogniprint-arxiv-v1.tar.gz
```

## Boundary

The manuscript reports descriptive mathematical diagnostics. It does not claim
validation, authorship detection, source provenance, AI-origin detection, legal
status, forensic status, or any universal decision threshold.
