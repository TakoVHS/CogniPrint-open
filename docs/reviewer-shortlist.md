# Independent methodological reviewer shortlist

Status: outreach planning only. Inclusion here does not imply endorsement, participation, or affiliation with CogniPrint.

## Selection criteria

Prefer reviewers with recent work in at least one of:

- AI-generated text detection;
- stylometry or interpretable text features;
- human–AI coauthoring detection;
- uncertainty calibration / abstention;
- adversarial robustness and distribution shift;
- synthetic-content provenance or trustworthy AI evaluation.

Avoid asking anyone to “support” the project. The request is for criticism, failure modes, and methodological corrections.

## Priority targets

### 1. HACo-Det research team — fine-grained human–AI coauthoring

Paper: *HACo-Det: A Study Towards Fine-Grained Machine-Generated Text Detection under Human-AI Coauthoring*, ACL 2025.

Authors: Zhixiong Su, Yichen Wang, Herun Wan, Zhaohan Zhang, Minnan Luo.

Why relevant: the paper directly studies word- and sentence-level human/AI coauthored text and reports that fine-grained detection remains far from solved. This is closely aligned with CogniPrint's proposed human–AI intervention track.

Public reference: https://aclanthology.org/2025.acl-long.1069/

Suggested ask: critique the intervention-map protocol, labeling strategy, context-window assumptions, and whether the proposed pilot can produce a meaningful negative result.

### 2. MoSEs research team — stylometry, uncertainty, conditional thresholds

Paper: *MoSEs: Uncertainty-Aware AI-Generated Text Detection via Mixture of Stylistics Experts with Conditional Thresholds*, EMNLP 2025.

Authors include Junxi Wu, Jinpeng Wang, Zheng Liu, Bin Chen, Dongjian Hu, Hao Wu, Shu-Tao Xia.

Why relevant: CogniPrint currently uses interpretable statistical/stylometric signals and corpus-relative thresholds. MoSEs is directly relevant to uncertainty-aware thresholding and stylistics-aware detection.

Public reference: https://aclanthology.org/2025.emnlp-main.294/

Suggested ask: critique calibration, conditional thresholds, reference-corpus design, and the danger of treating a static threshold as a transferable scientific boundary.

### 3. Pin-Yu Chen — trustworthy AI / robustness / interpretable detection context

Current public role: Principal Research Scientist and Manager at IBM Research; research interests include trustworthy AI, adversarial robustness, AI testing, and generative AI.

Why relevant: the model-fingerprint programme must survive adversarial transformations, distribution shift, and open-world conditions rather than optimize only closed-set accuracy. Recent work coauthored by Pin-Yu Chen also studies interpretable signals for AI-generated text detection.

Public profile: https://research.ibm.com/people/pin-yu-chen

Suggested ask: critique the robustness track, open-world abstention requirement, calibration, and whether the proposed falsification criteria are strong enough.

## Methodology references, not endorsement targets

### NIST GenAI Text 2026

NIST's current text evaluation explicitly evaluates text discriminators using discrimination and probability-quality metrics such as ROC-AUC and Brier score. CogniPrint should use this as evaluation context, not claim NIST compatibility or approval.

Reference: https://ai-challenges.nist.gov/text-2026

### NIST synthetic-content transparency report

NIST treats detection, provenance, authentication, watermarking, and related transparency methods as complementary approaches. This supports CogniPrint's separation between content-derived evidence and provenance records.

Reference: https://doi.org/10.6028/NIST.AI.100-4

### C2PA

C2PA provides a standards context for cryptographically bound content provenance. CogniPrint should treat such provenance as a separate evidence channel rather than infer it from style.

Reference: https://spec.c2pa.org/

## Outreach order

1. Send a compact reviewer request to one human–AI coauthoring specialist.
2. Send a separate request to one uncertainty/stylometry specialist.
3. Send a robustness-focused request to one trustworthy-AI researcher.
4. Do not mass-email large lists.
5. Preserve declines/referrals but do not count them as completed methodological review.
6. Count the gate only after a substantive independent critique is archived with permission.

## Reviewer bundle

Send only the minimum useful bundle:

- `docs/grant-one-pager.md`
- `docs/current-state-summary.md`
- `docs/model-fingerprint-benchmark-v0.1.md`
- `docs/external-review.md`
- `docs/reviewer-response-template.md`
- repository URL

The full manuscript and evidence dossier can be provided if requested.
