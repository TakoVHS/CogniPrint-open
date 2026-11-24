# Stage A Empirical Anchor v0.1

Status: **EXECUTED / DESCRIPTIVE_ONLY / PRE-FREEZE / MANUSCRIPT-MOTIVATION ONLY**

Purpose: define exactly what Stage A evidence may be used as a reviewer-facing
empirical anchor in the evidence-bounded-promotion manuscript.

## Source evidence

The fixed RAID development pilot used:

- 500 metadata-only records;
- five source classes: human, ChatGPT, GPT-4, Llama-chat and Mistral-chat;
- four domains: abstracts, news, reviews and wiki;
- 25 records per source-class/domain cell;
- lineage-grouped train/test split;
- 351 train records and 149 test records.

Reported balanced-accuracy values on the fixed descriptive split:

- CogniPrint 12D nearest centroid: \(0.542001\);
- character 3--5 hashed TF--IDF: \(0.590475\);
- word 1--2 hashed TF--IDF: \(0.601996\).

The conventional n-gram baselines therefore outperform the current 12D
representation on this executed pilot.

## Allowed manuscript interpretation

This evidence may be used to motivate the methodological problem:

- benchmark-bounded closed-set results are not open-world provenance claims;
- a numerical result can be informative while remaining insufficient for a
  different downstream target;
- weaker-than-baseline evidence should narrow claims rather than trigger a
  semantic upcast.

## Forbidden interpretation

This evidence must not be described as:

- a confirmatory Stage B result;
- a calibrated confidence certificate;
- proof of reliable model-family identification;
- proof of human-vs-AI detection;
- proof of provenance or authorship;
- evidence that the formal theorem is empirically validated;
- authorization to unlock Stage B.

## Manuscript wording rule

Any manuscript paragraph using these numbers must state that:

1. the run is development-only;
2. the outputs are uncalibrated closed-set labels;
3. the result is included as empirical motivation, not confirmatory evidence;
4. Stage B remains unauthorized.

## Scientific consequence

The negative baseline comparison is useful rather than embarrassing. It
demonstrates the project's central governance rule in an executed setting:
evidence that does not justify a stronger claim should narrow the claim rather
than be hidden or rhetorically upgraded.
