# Independent methodological reviewer shortlist

Status: outreach planning only.

Inclusion here does not imply endorsement, participation, affiliation or agreement with CogniPrint.

## Review target after M2/M2.1

The request is no longer primarily:

> Is the proposed benchmark a good idea?

The useful question is now:

> Given the executed negative/mixed M1/M2 evidence and the post-result M2.1 failure analysis, is the interpretation scientifically sound, and what must be redesigned before any sealed Stage B study is worth running?

Priority expertise:

- calibration and proper scoring rules;
- selective prediction / abstention;
- conformal prediction-set usefulness;
- open-set / OOD failure;
- AI-generated text detection under distribution shift;
- evidence-grounded decision support;
- statistical dependence and evaluation design.

Do not ask anyone to “support”, “validate” or “endorse” CogniPrint.

Ask for criticism.

## Priority 1 — classification-to-evidence gap in AI-text detection

### Jiatao Li, Mao Ye, Xinyu Hu, Cheng Peng, Xunjian Yin, Xiaojun Wan

Paper:

*When AI-Text Detectors Become Evidence: Rethinking Detection for Human Decisions* — Findings of EMNLP 2026.

Public reference:

https://aclanthology.org/2026.findings-emnlp.1539/

Why this team is unusually relevant:

The work explicitly argues that detector outputs are often used as **evidence**
rather than merely classifier labels, and that score-only interfaces can invite
overtrust and turn false positives into accusations.

This is directly aligned with CogniPrint's current evidence-first direction and
Claim Firewall.

Suggested reviewer question:

> Does the M1/M2/M2.1 evidence justify our decision to treat the current system
> as evidence/abstention research rather than a source-attribution detector, and
> are we still over-interpreting any statistical output?

Priority: **highest**.

## Priority 2 — uncertainty-aware stylistic AI-text detection

### MoSEs research team

Authors:

Junxi Wu, Jinpeng Wang, Zheng Liu, Bin Chen, Dongjian Hu, Hao Wu, Shu-Tao Xia.

Paper:

*MoSEs: Uncertainty-Aware AI-Generated Text Detection via Mixture of Stylistics
Experts with Conditional Thresholds* — EMNLP 2025.

Public reference:

https://aclanthology.org/2025.emnlp-main.294/

Why relevant:

CogniPrint M2 exposed weak max-confidence OOD behavior, poor generalisation of a
development-coverage threshold, and representation-dependent score scales.

MoSEs explicitly studies stylistic modeling, uncertainty and conditional
thresholds.

Suggested reviewer question:

> Are our max-confidence threshold failure, score-scale problem and current
> abstention design being interpreted correctly, and what probability/threshold
> methodology would you preregister before a sealed evaluation?

Priority: **highest**.

## Priority 3 — temperature scaling and conformal interaction

### Lahav Dabah and Tom Tirer

Paper:

*On Temperature Scaling and Conformal Prediction of Deep Classifiers* — ICML
2025.

Public reference:

https://proceedings.mlr.press/v267/dabah25a.html

Why relevant:

M2/M2.1 exposed an interaction between score scaling, temperature scaling and
very large conformal prediction sets:

- n-gram M2 fits hit the temperature lower bound;
- M2.1 showed substantially smaller diagnostic temperatures;
- 12D calibration-selected temperatures generalised worse than `T=1`;
- conformal outputs were almost entirely ambiguous rather than empty-set OOD
  rejections.

Suggested reviewer question:

> Is our use of scalar temperature scaling on cosine-centroid score vectors
> methodologically defensible, and how should calibration and conformal-set
> efficiency be separated in a future sealed design?

Priority: **high**.

## Priority 4 — context-aware thresholding for synthetic-text detection

### Haorong Li, Ruitao Ni, Haihui Yang, Shiping Gao, Yang Liu, Xiaojun Quan

Paper:

*Adaptive Boundaries: Context-Aware Detection for Synthetic Text* — EMNLP 2026.

Public reference:

https://aclanthology.org/2026.emnlp-main.1649/

Why relevant:

The paper explicitly addresses fixed-boundary failures across topics, styles and
model variants and studies calibration with context-aware thresholding.

Suggested reviewer question:

> Does the failure of our frozen global coverage/threshold policy indicate that
> a static confidence boundary is the wrong object, or would context-aware
> thresholding merely add degrees of freedom that our current Stage A sample
> cannot support?

Priority: **high**.

## Secondary target — human–AI coauthoring track

### HACo-Det research team

Paper:

*HACo-Det: A Study Towards Fine-Grained Machine-Generated Text Detection under
Human-AI Coauthoring* — ACL 2025.

Authors:

Zhixiong Su, Yichen Wang, Herun Wan, Zhaohan Zhang, Minnan Luo.

Reference:

https://aclanthology.org/2025.acl-long.1069/

Why relevant:

This remains useful for the proposed human–AI intervention track, but it is not
the first reviewer target for the immediate M2 calibration/open-set problem.

## Secondary context — robustness and shortcut control

A recent EMNLP 2026 paper, *Shortcut-Controlled Evaluation for AI-Generated Text
Detection*, reports that simple surface shortcuts can produce strong benchmark
classification performance.

Reference:

https://aclanthology.org/2026.emnlp-main.2177/

This is relevant context for deciding whether any compact surface-profile
representation should be interpreted as source evidence rather than benchmark
signal.

## Outreach order

1. Contact **one** Priority-1 evidence/decision-support researcher or team.
2. Contact **one** Priority-2 uncertainty/stylometry researcher or team.
3. Contact **one** Priority-3 calibration/conformal researcher or team.
4. Only if there is no response, add Priority-4.
5. Do not mass-email.
6. Do not ask for endorsement.
7. Ask one or two narrow methodological questions, not “please review my whole project”.
8. Preserve decline/referral responses but do not count them as methodological review.
9. Count the review gate only after a substantive independent critique is received and preserved with an appropriate permission boundary.

## Minimum reviewer bundle

Send:

1. `reviewer-bundle/executive-summary.md`
2. `reviewer-bundle/m2-results.md`
3. `reviewer-bundle/limitations.md`
4. `reviewer-bundle/reviewer-questions.md`
5. `docs/scientific-claim-review-m2-2026-11-24.md`
6. repository URL

Optional on request:

- full M2/M2.1 protocols and machine-readable summaries;
- manuscript draft;
- exact workflow/evidence hashes.

Do **not** lead with a grant one-pager.

The immediate request is methodological criticism of executed evidence.
