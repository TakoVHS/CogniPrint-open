# External methodological review outreach — M2/M2.1

Status: `DRAFTS_ONLY / NOT_SENT`

These drafts are designed for one-to-one outreach. Do not send all of them at
once.

The request is for criticism, not endorsement.

## Common evidence links to include

Repository:

https://github.com/TakoVHS/CogniPrint-open

Reviewer-facing result:

`reviewer-bundle/m2-results.md`

Scientific Claim Review:

`docs/scientific-claim-review-m2-2026-11-24.md`

## Draft A — evidence / human-decision researcher

Subject:

`Request for a narrow methodological critique of an AI-text evidence study`

Body:

Hello,

I am developing CogniPrint, an open research project on evidence-bounded
statistical text profiling.

I am reaching out because your work on the gap between AI-text classification
and evidence used in human decisions is closely related to a problem our latest
experiment exposed.

We ran a fixed Stage A study comparing a compact 12-feature profile with
character and word n-gram baselines. The compact representation did not win.
A follow-up uncertainty analysis also found weak max-confidence OOD separation
and a conformal regime that almost always abstained through multi-class
ambiguity rather than true empty-set rejection.

We preserved the negative result and currently keep the project
`descriptive_only`.

Could I ask one narrow question?

**Do you think our decision to frame the current output as evidence/abstention
research rather than a source-attribution detector is methodologically
justified, and is there any part of our interpretation that still overclaims
what these experiments show?**

The reviewer summary is intentionally short and includes the exact failure
modes and evidence hashes. A critical or negative answer is completely useful;
I am not asking for endorsement.

Thank you for considering it.

Roman Adriashkin
CogniPrint Research Initiative

## Draft B — uncertainty / stylistic detector researcher

Subject:

`Methodological question: threshold generalisation in an executed AI-text study`

Body:

Hello,

I am working on an open research project called CogniPrint that uses compact
interpretable text features and explicit abstention/evidence gates.

Our latest fixed Stage A experiment produced a negative/mixed result: lexical
n-gram baselines had stronger aggregate point estimates than the compact 12D
representation, and a confidence threshold selected for at least 60% coverage
on a development partition did not maintain that coverage consistently on held
out data.

Could I ask for a narrow methodological critique?

**Given this result, would you treat a global confidence threshold as the wrong
object for this problem, or would a conditional/context-dependent threshold add
too many degrees of freedom for a dataset of this size?**

We have deliberately not retuned the original result after inspection. A
post-result diagnostic is labelled exploratory and preserved separately.

I can send the short reviewer bundle or the exact machine-readable evidence if
useful. A critical answer is welcome; this is not a request for endorsement.

Thank you,

Roman Adriashkin
CogniPrint Research Initiative

## Draft C — calibration / conformal researcher

Subject:

`Question on temperature scaling of cosine scores and conformal ambiguity`

Body:

Hello,

I would value a narrow methodological opinion on a calibration/conformal result
from an open text-profiling study.

The experiment uses cosine-nearest-centroid score vectors for three
representations and applies scalar temperature scaling on a separate
calibration partition.

Two unexpected results appeared:

1. For n-gram representations, every original fit hit the lower temperature
   bound `T=0.05`; a separately frozen post-result diagnostic grid selected
   `0.01–0.02`.
2. Class-conditional conformal prediction at alpha `0.05` produced almost no
   empty sets for held-out unknown families. Instead, nearly every unknown was
   a multi-class ambiguous set, and known examples were also mostly ambiguous.

The compact 12D representation behaved differently: widening the lower
temperature range did not rescue its held-out calibration.

My question is:

**Is treating cosine-centroid similarities as logit-like inputs to scalar
temperature scaling defensible here, and what probability/conformal design
would you preregister before a genuinely sealed follow-up?**

The original result is preserved unchanged, and the diagnostic analysis is
explicitly post-result exploratory.

I am asking for criticism, not endorsement. A short negative assessment would
be genuinely useful.

Thank you,

Roman Adriashkin
CogniPrint Research Initiative

## Sending rule

Before any email is sent:

1. choose one recipient/team;
2. verify the current public contact channel;
3. attach/link only the minimal reviewer bundle;
4. do not imply affiliation or prior interest;
5. do not send follow-up spam;
6. preserve the response with permission appropriate to its use;
7. do not increment the review counter for acknowledgement/decline/referral.

