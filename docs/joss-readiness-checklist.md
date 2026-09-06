# CogniPrint — JOSS readiness checklist

Status date: 2026-09-06

Target: Journal of Open Source Software (JOSS)

Submission state: **NOT SUBMITTED**

Scientific state: **`descriptive_only`**

This checklist separates software-publication readiness from stronger scientific validation. A JOSS acceptance would validate that the software meets JOSS review criteria; it would not validate model attribution, AI-origin detection, authorship inference, or forensic provenance claims.

## 1. Scope and eligibility

| Gate | Status | Evidence / action |
|---|---|---|
| Open-source software | PASS | MIT-licensed repository. |
| Active research application | PASS | Text-profile construction, perturbation diagnostics, reproducible public-data runs, evidence artifacts. |
| Research software rather than one-off script | PASS WITH REVIEW | Packaged Python project, CLI, validation scripts, tests and documentation; external reviewer should confirm usability beyond maintainer workflow. |
| Feature-complete enough for review | CONDITIONAL | Current v0.1.2 has a bounded usable descriptive core. No stronger attribution capability is required or claimed. Confirm clean install and end-to-end reviewer path before submission. |
| Repository public | PASS | `TakoVHS/CogniPrint-open`. |
| OSI-approved license | PASS | MIT. |
| Community standards | PASS | Code of Conduct exists on `main`. |
| Contribution guide | PREPARED | `CONTRIBUTING.md` added in the publication-prep branch; must be reviewed before merge. |

## 2. JOSS paper-format gates

Current JOSS requirements checked 2026-09-06 require Markdown + YAML metadata, a non-specialist opening, research applications, approximately 750–1750 words, and sections covering Summary, Statement of need, State of the field, Software design, Research impact statement, AI usage disclosure, Acknowledgements, and References.

| Gate | Status | Evidence / action |
|---|---|---|
| `joss/paper.md` | DRAFT READY | Separate from mathematical `paper/main.tex`. |
| YAML metadata | PASS DRAFT | Title, tags, author, ORCID and affiliation included. |
| Non-specialist summary | PASS DRAFT | Opens with purpose/functionality and current boundary. |
| Statement of need | PASS DRAFT | Explains evidence-oriented use case. |
| State of the field | PASS DRAFT | Stylometry/vector-space context and public benchmarks. |
| Software design | PASS DRAFT | Describes package, CLI, profile and validation architecture. |
| Research impact statement | PASS DRAFT | Describes current and planned research use without claiming validation. |
| AI usage disclosure | PASS DRAFT | Explicitly discloses generative-AI assistance and verification responsibility. |
| Acknowledgements | PASS DRAFT | No unsupported funding/endorsement claim. |
| Bibliography | PASS DRAFT | `joss/paper.bib` created from existing project references. |
| Word-count check | TODO | Run exact Pandoc/JOSS word count before submission; target 750–1750. |
| JOSS PDF build | TODO | Build with the current JOSS toolchain and fix metadata/citation issues. |

## 3. Reviewer execution path

A JOSS reviewer should be able to reproduce a useful workflow without private context.

Required reviewer path before submission:

```bash
git clone https://github.com/TakoVHS/CogniPrint-open.git
cd CogniPrint-open
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
python -m unittest tests/test_public_release_export.py -v
python scripts/check_public_benchmark_v11.py
python scripts/secret_scan.py
```

Then at least one documented research workflow must be runnable from a single command/Make target and produce inspectable artifacts.

### Remaining reviewer-path gates

- [ ] clean-room install on a fresh Linux runner at the exact candidate SHA;
- [ ] confirm Python versions actually exercised by CI match package metadata;
- [ ] run all public tests and retain machine-readable PASS evidence;
- [ ] run one seed/smoke diagnostic with no external data download;
- [ ] run one real public-data diagnostic using documented optional dependencies;
- [ ] verify every generated artifact path described in docs exists;
- [ ] verify no secret/private data is required;
- [ ] verify command failure messages are understandable to an external user;
- [ ] confirm documentation names match actual CLI/Make targets.

## 4. Documentation gates

- [x] README describes scope and non-claims.
- [x] `CITATION.cff` exists.
- [x] research vision exists.
- [x] failure charter exists.
- [x] attribution-challenge protocol exists.
- [x] evidence dossier exists.
- [x] Code of Conduct exists.
- [x] contribution guide prepared on publication branch.
- [ ] add a compact user-facing API/CLI guide if current README is insufficient for a new user;
- [ ] add an explicit `REPRODUCIBILITY.md` entry point if reproduction remains distributed across multiple docs;
- [ ] ensure all screenshots/figures are generated or provenance-documented;
- [ ] verify external links and dataset licenses at candidate SHA.

## 5. Release and archive gates

- [x] public version recorded as v0.1.2.
- [x] repository has citation metadata.
- [ ] select exact JOSS candidate release SHA/tag;
- [ ] create immutable release archive for that candidate;
- [ ] independently verify the intended Zenodo record and DOI resolves publicly;
- [ ] update citation metadata only after DOI verification;
- [ ] ensure JOSS submission version and archive version are identical;
- [ ] preserve source/data licenses separately where required.

Current DOI state must remain **recorded but direct-public-verification pending** until independently resolved.

## 6. Scientific-boundary gates

These are not all JOSS editorial requirements, but they protect CogniPrint from turning a software publication into an unsupported scientific claim.

- [x] current readiness visible as `descriptive_only`;
- [x] `UNKNOWN / insufficient evidence` preserved conceptually;
- [x] author/source/AI-origin/forensic non-claims are explicit;
- [x] software paper does not claim Attribution Challenge 001 is completed;
- [ ] external methodological review remains `0/1` until substantive response exists;
- [ ] preregister Attribution Challenge 001 before decisive analysis;
- [ ] publish negative/failure outcomes as first-class results;
- [ ] do not market a JOSS acceptance as proof that the scientific hypothesis is true.

## 7. Submission stop conditions

**DO NOT SUBMIT TO JOSS** if any of the following are true:

1. clean install/test fails at candidate SHA;
2. paper references a capability not present in that release;
3. DOI/archive metadata points at a different software state;
4. required public data cannot be legally/reproducibly accessed;
5. paper implies validated attribution/AI detection beyond `descriptive_only`;
6. AI usage disclosure is incomplete;
7. repository documentation requires maintainer-only knowledge to reproduce the central workflow.

## 8. Ready-to-submit definition

`JOSS_READY=PASS` only when:

- candidate release SHA is frozen;
- clean-room install + tests PASS;
- one end-to-end reviewer workflow PASSes;
- JOSS paper builds cleanly and is within word limit;
- archive/DOI are verified and version-aligned;
- docs/license/community files are complete;
- claim scan finds no unsupported capability;
- owner explicitly approves external submission.

Until then: `JOSS_SUBMISSION=HOLD`.
