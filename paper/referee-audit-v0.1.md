# TMLR Referee Audit v0.1 — Evidence-Bounded Promotion

Status: **REVIEWER-FACING PASS / CORE FROZEN / NO NEW THEORY**

Audited artifact: compiled TMLR PDF from exact-head CI, 9 pages.

Audit goal: identify where a technically competent TMLR reviewer could say
"trivial", "unclear", "already known", "why ML?", or "what is the practical
value?" and either repair the presentation or explicitly retain the issue as a
limitation.

## Executive referee verdict

The current manuscript is technically coherent enough to justify continued
review rather than desk rejection on mathematical grounds. The main acceptance
risk is not a false theorem. It is whether the paper makes the methodological
lesson sufficiently useful and ML-specific to satisfy TMLR's "interest" and
"what can readers learn?" criterion.

The Canonical Least Warrant theorem is mathematically elementary. The paper
must not sell it as a deep new theorem. Its defensible role is to canonicalize
the interface: exact sharp envelope first, tractable warrants second.

The AI-attribution example is logically valid but intentionally synthetic. It
supports the non-transfer claim, not empirical detector performance.

## Page 1 — title, abstract, introduction

### Risk R1 — "Why is this ML?"

**Severity:** critical presentation risk.

A reviewer could read the first page as generic partial-identification language
with an AI-attribution label attached afterward.

**Disposition:** ACCEPTED / FIXED.

The Introduction now contains an explicit "Why this is a machine-learning
problem" paragraph. It names the benchmark-to-deployment promotion failure in
ML terms: task-specific metrics, calibration, selective risk, OOD scores, and
closed-set source-family performance versus open-world semantic claims.

### Risk R2 — the contribution list sounds like novelty claims

**Severity:** moderate.

Items such as a fail-closed rule and sharp envelope could be misread as claims
that their ingredients are historically new.

**Disposition:** ACCEPTED / ALREADY NARROWED.

The contributions block explicitly labels the first three items as a
methodological organization of existing statistical/formal ideas rather than
new partial-identification or union-bound theory.

### Risk R3 — LLM disclosure rendered with footnote marker "0"

**Severity:** format/professionalism.

The first compiled PDF displayed a superscript zero because the TMLR style
resets the footnote counter and \`\\footnotetext\` was used directly.

**Disposition:** ACCEPTED / FIXED.

The disclosure is now an unnumbered first-page footnote, preserving TMLR's
transparency requirement without a bogus marker.

## Pages 2–4 — setup and Canonical Least Warrant

### Risk R4 — "This theorem is trivial"

**Severity:** critical positioning risk.

The theorem follows directly from set inclusion and monotonicity. A reviewer is
right to call the proof elementary.

**Disposition:** ACCEPTED / REFRAMED, NOT DEFENDED AS DEEP.

A new remark states explicitly that the theorem is an elementary
canonicalization result. The value claimed is organizational: all monotone
warrants are placed above one sharp compatible-world envelope, so exact versus
conservative implementations have a common reference object.

### Risk R5 — empty compatible set accidentally permits promotion

**Severity:** critical correctness risk.

A total numerical extension such as zero could make
\(s_T^\star(b)\le\delta_c\) true on an infeasible model.

**Disposition:** FIXED BEFORE THIS AUDIT.

The numerical envelope is partial on \(\mathcal B_T\); the infeasible branch is
\(\bot\) and cannot be compared with a claim threshold.

### Risk R6 — why is conjunctive scope an intersection?

**Severity:** moderate clarity risk.

A reader may wonder whether different certificates can cover different pieces
of the deployment population.

**Disposition:** RETAINED AND EXPLAINED.

The current rule uses all certificates conjunctively at each deployment world,
so every certificate invoked by the warrant must be valid there. Piecewise
regional composition would be a different calculus and is intentionally not
introduced in this paper.

## Pages 4–6 — ternary outcomes and fail-closed soundness

### Risk R7 — "Ternary judgment" is being sold as a new three-valued logic

**Severity:** moderate novelty risk.

**Disposition:** REJECTED AS A NOVELTY CLAIM.

The manuscript calls PROMOTE / ABSTAIN / UNRESOLVED operational verification
outcomes. UNRESOLVED is not treated as a third decision-theoretic action unless
an action and loss are separately defined.

### Risk R8 — what does a practitioner actually do?

**Severity:** critical usefulness risk.

Without an operational reading, the framework could look like notation around
partial identification.

**Disposition:** ACCEPTED / FIXED.

A practitioner paragraph now states the required order of questions:
(1) what target does the certificate control, (2) on which worlds, and
(3) what validated argument transports that control to the desired claim?
Missing answers produce abstention/unresolved rather than stronger confidence.

### Risk R9 — union-bound accounting double-counts shared events

**Severity:** moderate limitation.

**Disposition:** DISCLOSED, NOT SOLVED.

The paper says the sum can be conservative when downstream claims reuse the
same validity event. Dependence/event-identity accounting is explicitly left
outside the present paper and is not claimed as novelty.

### Risk R10 — soundness theorem depends on hidden independence

**Severity:** correctness concern.

**Disposition:** REJECTED.

The proof uses only the intersection of validity events plus the union bound.
No independence assumption is used or claimed.

## Page 6 — AI-attribution application

### Risk R11 — the example is too synthetic

**Severity:** critical interest risk.

A reviewer may ask why a two-world construction is useful for ML practice.

**Disposition:** PARTIALLY ACCEPTED.

The paper is explicit that the construction establishes logical non-transfer,
not real detector performance. Its ML value is to expose an error pattern:
closed-set family performance can coexist with unresolved membership or
provenance risk.

**Remaining strengthening opportunity:** if included later, an already-executed
development benchmark may be used only as an empirical motivation/anchor, not
as evidence for the theorem and not as a Stage B result. Any such addition must
preserve the current descriptive-only boundary.

## Pages 6–8 — prior work and limitations

### Risk R12 — compatible worlds / sharp envelopes / counterworlds are already Zhu

**Severity:** critical novelty risk.

**Disposition:** ACCEPTED AS PRIOR ART.

The manuscript explicitly treats these components as prior art rather than
claiming them as unique to CogniPrint.

### Risk R13 — aHL/Eris already have error resources

**Severity:** critical novelty risk.

**Disposition:** ACCEPTED AS PRIOR ART.

No novelty is claimed for additive confidence/error budgets, probabilistic
effects, or first-class error resources.

### Risk R14 — BHL/StatWhy already formalize statistical program requirements

**Severity:** critical novelty risk.

**Disposition:** ACCEPTED AS PRIOR ART.

The paper does not claim invention of formal statistical pre/postconditions or
verification of test interpretations.

### Risk R15 — assurance cases already relate evidence to claims

**Severity:** critical novelty risk.

**Disposition:** ACCEPTED AS PRIOR ART.

The paper positions itself as a narrower certificate-to-semantic-claim
methodology with explicit frequentist targets/scopes, not generic
evidence-to-claim reasoning.

## Page 8 — broader impact and conclusion

### Risk R16 — attribution framing can be read as a forensic tool

**Severity:** ethical/practical risk.

**Disposition:** ACCEPTED / FIXED IN CURRENT TEXT.

The paper explicitly says the construction is not a validated forensic
attribution system and recommends domain-specific evidence, due process, and
qualified human review for consequential uses.

## Current acceptance-risk summary

### Strongest points

- mathematical core is internally coherent;
- empty-set semantics are fail closed;
- novelty boundaries are unusually explicit;
- TMLR fit is plausible because technical correctness and reader learning are
  emphasized over headline novelty;
- the paper is short (9 pages) and focused.

### Weakest points

- Canonical Least Warrant is elementary and must remain framed as
  canonicalization;
- the application is currently a formal counterexample rather than an empirical
  evaluation;
- the strongest historical collision, Zhu (2026), has not yet been verified
  against the complete full text in this audit;
- practical value depends on readers accepting "claim promotion" as a useful
  explicit interface rather than ordinary partial-identification hygiene.

## Referee-style recommendation at v0.1

**Recommendation: continue revision; not yet submit.**

Reason: I would not reject the present draft for a visible mathematical error,
but I would request a precise Zhu comparison and a clearer statement of the
incremental ML-methodology value before recommending acceptance.

No new theorem is required to address these concerns.
