# Where CogniPrint fails

Status: **failure charter and reporting contract.**

This document is intentionally written before stronger attribution results exist.

CogniPrint should not earn trust by hiding uncertain or negative cases. Any future attribution capability must publish the conditions under which it fails, degrades, or should abstain.

## Current boundary

The current public release is `descriptive_only`.

It does not currently establish:

- exact neural-model identity;
- definitive AI origin;
- authorship identity;
- a commissioning actor;
- intent or responsibility;
- legal or forensic provenance.

Therefore the present failure statement is simple: **CogniPrint is not yet a validated attribution system.**

## Failure classes that must be measured

Any future model-family or lineage result must report at least the following regimes separately.

### 1. Short-input failure

Very short text may not contain enough stable measurable structure to support a useful comparison.

The project must estimate the shortest useful regime empirically and permit `INSUFFICIENT EVIDENCE` below it.

### 2. Domain shift

A fingerprint learned on one domain may capture genre conventions rather than source behaviour.

Required controls include cross-domain holdouts and prompt/task balancing.

### 3. Prompt leakage

Models answering the same prompt can share prompt-induced structure. Related prompt/source lineages must not leak across train and evaluation partitions.

### 4. Length confounding

If a classifier succeeds primarily because one source produces longer or shorter outputs, that is not a useful model fingerprint.

Length-only baselines are mandatory.

### 5. Surface/n-gram confounding

If character or word n-grams explain the result, the project should say so rather than attributing the gain to a deeper cognitive signature.

### 6. Paraphrase degradation

Paraphrasing can erase or replace surface signals. Report clean and paraphrased performance separately.

### 7. Human-edit degradation

Substantial human rewriting can change the observable profile. The system must not treat human editing as nuisance noise when the intended use case includes mixed production.

### 8. Translation degradation

Translation may introduce the signature of a translation system or target-language conventions while destroying source-generation signals.

### 9. AI-to-AI rewrite ambiguity

A second model can overwrite the observable signature of the first. A final-text-only system may be unable to recover the earlier source.

### 10. Unseen-model failure

Closed-set attribution can force an unseen model into the nearest known class.

`UNKNOWN / OUT OF DISTRIBUTION` is therefore mandatory before a model-family suggestion can be considered responsible.

### 11. Model drift

Providers update models. Fine-tunes, checkpoints, safety layers, system prompts, and decoding defaults change.

Reference fingerprints can become stale and must carry observation/version metadata.

### 12. Multilingual failure

The current lightweight feature map is not automatically language-neutral. A feature that is meaningful in English may not transfer cleanly to Russian, Vietnamese, German, Czech, or another language.

Language-specific validation is required.

### 13. Adversarial rewriting

An actor may deliberately rewrite content to defeat a detector or imitate another style. Robustness should be tested, not assumed.

### 14. Calibration failure

A classifier can rank classes correctly while assigning misleading confidence.

Uncalibrated scores must be labelled as such, and abstention thresholds must be evaluated independently.

### 15. Provenance conflict

Content-derived evidence may disagree with signed/declarative provenance.

CogniPrint must show the conflict rather than silently choosing one evidence class as truth.

### 16. Missing provenance

Absence of a signed credential or workflow log is not evidence that a workflow did not happen.

Missing evidence must remain `missing`.

### 17. Actor-inference failure

Prose alone cannot reliably reveal who commissioned, approved, or deployed a generation action.

No actor identity should be inferred without independent actor evidence.

## Required failure table for future releases

Any release that introduces an attribution capability should publish a table containing at least:

- evaluation regime;
- dataset/source revision;
- minimum/median length;
- known versus unseen source status;
- transformation type;
- coverage after abstention;
- balanced accuracy / macro F1 where applicable;
- false-known rate on unknown sources;
- calibration metric;
- dominant failure explanation;
- whether the result is considered usable, exploratory, or failed.

## Examples are mandatory

Aggregate metrics are not enough.

A public failure report should contain representative false positives, false negatives, mistaken family assignments, correct UNKNOWN decisions, and cases where the system should have abstained but did not.

Sensitive source content must not be published merely to provide an example. Synthetic or appropriately licensed examples should be preferred.

## Failure-driven product principle

A result should become **less specific** as evidence weakens.

Conceptually:

`measured profile → candidate family → candidate list → unknown → insufficient evidence`

The system should never become more certain merely because the interface demands a single answer.

## Scientific stop rule

If the strongest observed signal is unstable, trivial, non-replicable, dominated by simple baselines, or unsafe under open-world evaluation, the correct scientific result is to narrow the capability claim.

The existence of the CogniPrint project does not depend on every fingerprint hypothesis being true.

A reliable map of **where attribution is impossible or unsafe** is itself valuable provenance research.
