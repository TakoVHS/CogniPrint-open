# External reviewer response template

Reviewer name and affiliation (optional):

Date:

Public link or email reference (optional):

Review classification:

- substantive methodological review;
- informal methodological comment;
- decline/referral;
- acknowledgement only.

## 1. Claim boundaries

Are CogniPrint's current claims appropriately bounded at `descriptive_only`?

Does any wording still read as authorship, exact-model identity, universal
AI-origin or reliable OOD detection despite the explicit non-claims?

## 2. M1/M2 interpretation

The current 12D representation did not lead the tested lexical baselines on the
fixed M1 comparison or M2 aggregate point estimates.

Is the project's negative/mixed interpretation sufficiently conservative?

Are we making too much or too little of the fact that the predeclared per-fold
proper-score intervals all include zero?

## 3. Five-role / leave-one-family-out design

Is the lineage-disjoint separation into:

- training/reference;
- probability calibration;
- conformal calibration;
- threshold development;
- held-out development evaluation

methodologically defensible?

Is leave-one-machine-family-out useful Stage A evidence when every family is
already visible to the research programme?

## 4. Probability mapping and temperature scaling

M2 treats cosine-centroid similarity vectors as logit-like scores before scalar
temperature scaling.

M2/M2.1 found:

- 12D calibration-selected temperatures worsened held-out NLL on average;
- n-gram M2 fits all hit `T=0.05`;
- an exploratory wider grid selected `T=0.01–0.02` for n-grams;
- score scales differ greatly across representations.

Would you retain this probability mapping in a future sealed study?

If not, what fixed/prospectively specified alternative would you recommend?

## 5. Selective prediction

M2.1's exploratory risk-coverage analysis did not reveal a hidden 12D
advantage.

Does the current evidence justify further selective-prediction work with this
representation?

What risk/coverage operating point would be scientifically meaningful?

## 6. Conformal prediction

M2.1 found:

- unknown empty-set rate `0.0` in every fold/representation;
- almost all unknown outcomes were multi-class ambiguous sets;
- known examples were also overwhelmingly ambiguous;
- duplicate declared lineage groups were absent.

Is the correct conclusion that this conformal layer is presently a conservative
ambiguity mechanism rather than an OOD detector?

What conformal target/design, if any, would be appropriate for a future sealed
study?

## 7. Cross-fold inference

The same Stage A corpus participates in multiple leave-one-family-out folds.

Is any pooled cross-fold inferential estimand defensible here?

If yes, what would you predefine?

## 8. Falsification

Does the current evidence already justify retiring the 12D representation from
attribution research and keeping it only as an interpretable diagnostic
baseline?

What future result should terminate the broader model-family fingerprint
hypothesis?

## 9. Stage B

What must be frozen before a genuinely sealed Stage B study is scientifically
worth running?

Please identify required:

- unseen source-family design;
- calibration approach;
- OOD/UNKNOWN rule;
- sample size;
- baseline set;
- negative controls;
- preregistration choices;
- stopping/falsification criteria.

## 10. Overall recommendation

Choose one if useful:

- Current descriptive framing is responsibly bounded.
- Current descriptive framing needs corrections.
- M1/M2/M2.1 interpretation is methodologically reasonable with corrections.
- Probability/calibration design should be replaced before Stage B.
- Current 12D representation should remain only a diagnostic baseline.
- The model-family fingerprint hypothesis should not proceed to Stage B.
- I am not the appropriate reviewer.

Additional comments:

---

A response does not imply endorsement.

A critical or negative independent methodological review is useful evidence and
may satisfy the external review gate.

Scientific readiness remains `descriptive_only` unless later evidence and a
separate claim review justify a change.
