# CogniPrint redesign preview — QA record

Date: 2026-09-09

Branch: `gpt6-evidence-lab-preview-20260909`

Implementation commit before this QA record: `ebbf7925ab8706cd7ff393b294e9918fccb2fb8b`

Production state: **UNCHANGED**

## Scope

This record audits the branch-only evidence-lab homepage implementation. It is not a production approval and does not claim browser/device testing that has not actually occurred.

## Implemented requirements

- [x] hero: `Measure the trace. Keep the uncertainty.`
- [x] visible `descriptive_only` state;
- [x] live local 12D descriptive instrument;
- [x] browser feature calculations aligned to the current Python v2 feature map for the displayed coordinates;
- [x] Unicode-aware punctuation handling for Russian/English text;
- [x] `OBSERVED / INFERRED / ATTESTED / UNKNOWN` evidence classes;
- [x] evidence status strip;
- [x] `Can currently support` / `Does not currently establish` boundary;
- [x] explicit publication states;
- [x] negative Stage A result shown as first-class evidence;
- [x] sponsor section below evidence/research material;
- [x] sponsor section explicitly states that funding does not determine outcomes;
- [x] skip-to-content link;
- [x] visible `:focus-visible` treatment for links/buttons/textarea;
- [x] `prefers-reduced-motion` handling;
- [x] responsive layout breakpoints;
- [x] preview page sets `noindex,nofollow` so branch/preview content is not intended as a production scholarly record.

## Static color-contrast audit

WCAG contrast calculations against paper background `#F5F2EA`:

| Foreground | Role | Contrast | Static verdict |
|---|---|---:|---|
| `#111318` | primary text | 16.61:1 | PASS AA/AAA |
| `#4D525C` | muted text | 7.01:1 | PASS AA/AAA |
| `#2457FF` | cobalt accent | 4.84:1 | PASS AA normal text |
| `#A55A00` | HOLD/warning | 4.62:1 | PASS AA normal text |
| `#157347` | PASS/verified | 5.25:1 | PASS AA normal text |
| `#A32A2A` | failure/negative result | 6.42:1 | PASS AA normal text |
| `#173FCA` | links | 7.22:1 | PASS AA/AAA |
| `#EEF2FF` on `#111318` | dark vector panel | 16.62:1 | PASS AA/AAA |

These values do not replace visual inspection of every final state, hover/focus state, or browser rendering.

## Scientific/UI integrity checks

- [x] no `AI probability` gauge;
- [x] no `Who wrote this?` UI;
- [x] no unique-model verdict;
- [x] no forensic/legal verdict;
- [x] current external review shown as `0/1 · pending`;
- [x] DOI shown as `verification pending`;
- [x] Challenge 001 shown as `PRE-FREEZE`;
- [x] JOSS shown as preparation/HOLD rather than submitted/published;
- [x] GitHub Sponsors shown as prepared/not launched.

## Remaining browser QA — NOT YET EXECUTED

The following require an actual deployed preview or local browser run and therefore remain HOLD:

- [ ] visual regression at desktop width;
- [ ] 360 px mobile;
- [ ] 390 px mobile;
- [ ] 430 px mobile;
- [ ] tablet width;
- [ ] 200% browser zoom;
- [ ] full keyboard-only traversal;
- [ ] screen-reader smoke on live instrument updates;
- [ ] browser console error check;
- [ ] runtime verification of all twelve browser coordinates against Python golden fixtures;
- [ ] performance/Lighthouse measurement;
- [ ] actual Vercel preview deployment for this branch.

## Deployment limitation

The existing Vercel project `cogniprint-public-site` is not currently exposed by the connector as a Git-linked project for this repository, and the available deploy action does not accept a repository branch/project selection. Therefore this audit does **not** invoke a deployment action that could target the wrong project or production.

Required next deployment step: create a branch-specific preview using a verified Git/Vercel linkage or an explicitly scoped preview deployment mechanism, then run the browser QA list above. Do not point `cogniprint.org` or production aliases at this branch until a separate approval after browser QA.

## Verdict

`REDESIGN_CODE = IMPLEMENTED_IN_BRANCH`

`STATIC_ACCESSIBILITY = PASS_WITH_BROWSER_QA_PENDING`

`VERCEL_PREVIEW = NOT_DEPLOYED`

`PRODUCTION = UNCHANGED`
