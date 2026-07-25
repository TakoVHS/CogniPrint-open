# Open Technology Fund Internet Freedom Fund — Concept Note skeleton

## HOLD — practitioner evidence required

Do not submit this Concept Note until `docs/grants/otf-practitioner-discovery.md` reaches a documented GO decision.

Current status: **NO-GO / insufficient practitioner evidence**.

## Programme facts to re-check immediately before submission

As verified on 2026-07-25, OTF's Internet Freedom Fund:

- accepts Concept Notes on a rolling basis;
- supports technology development, applied research, digital security, and related internet-freedom work;
- publishes awards of `$10,000–$900,000` for up to 24 months;
- describes `$50,000–$200,000` over 6–12 months as an ideal range for many projects;
- evaluates remit fit, real-world problem, cost-effectiveness, sustainability, and complementarity;
- explicitly includes user research on the needs of people living under repressive surveillance and censorship.

Official source: https://www.opentech.fund/funds/internet-freedom-fund/

Do not rely on this cached summary when actually submitting; re-open the current guide and form.

---

## 1. Project title

**Placeholder — must be rewritten after discovery**

Working internal title:

`Local Evidence Workstation for High-Risk Digital Investigations`

Avoid leading with "AI detector" or "model fingerprinting" in the final title unless practitioners identify that as the actual problem.

## 2. Existing problem

**BLOCKED pending interviews.**

Required evidence before writing:

- repeated practitioner problem in their own terms;
- who experiences it;
- why the environment involves censorship, repressive surveillance, or another OTF-remit information-control risk;
- what decision/workflow is currently impaired;
- why current tools/workarounds are insufficient;
- why local/private processing changes the feasibility or safety of the workflow.

Do not write a hypothetical problem here.

## 3. Intended users

**BLOCKED pending interviews.**

Choose one primary user group, not "everyone":

- independent-media digital-forensics teams;
- human-rights digital-documentation investigators;
- frontline media-integrity / synthetic-media responders;
- another group directly supported by practitioner evidence.

Record deployment constraints, languages, connectivity, and risk model.

## 4. Proposed approach

Candidate architecture to validate, not a fixed promise:

1. sensitive text is processed locally;
2. deterministic CogniPrint measurements and SHA-256 are produced without embedding raw text in the evidence output;
3. statistical signals are labelled as hypotheses/measurements, not provenance facts;
4. hashes, revision history, signed credentials, or authenticated records are represented separately when available;
5. output can abstain with `insufficient evidence`;
6. no automatic author/actor/intent attribution;
7. only practitioner-required languages/features are prioritised.

Remove components that interviews show are not useful.

## 5. Internet-freedom outcome

**BLOCKED pending discovery.**

The final note must state a concrete outcome for people affected by censorship or surveillance, for example:

- safer local triage of contested material before sharing it externally;
- reduced need to upload sensitive investigation material to centralized AI services;
- a more explicit separation between weak content signals and authenticated provenance in a high-risk investigation workflow;
- another outcome directly reported by practitioners.

Do not claim that CogniPrint "fights censorship" merely because the software is privacy-preserving.

## 6. Complementary efforts

Required final mapping:

- provenance standards such as C2PA;
- existing synthetic-content/detection approaches;
- existing digital-forensics or verification workflows used by the chosen practitioners;
- local/offline AI or analysis tooling where relevant;
- OTF-supported projects that overlap with the final use case.

The note must explain what CogniPrint adds and what it deliberately does not replace.

## 7. Proposed activities / work packages

Only activate work packages supported by discovery.

### WP1 — Practitioner workflow and threat model

- validate workflow with intended users;
- define sensitive-data boundary;
- define high-cost failure modes;
- publish only approved anonymised findings.

### WP2 — Local evidence workstation

- deterministic local profiling;
- bounded evidence bundle;
- privacy-preserving local explanation where useful;
- no remote ingestion requirement for sensitive source text.

### WP3 — Relevant-language validation

- validate only languages practitioners need;
- compare simple baselines;
- test translation/human-edit robustness;
- publish negative results.

### WP4 — Provenance fusion

- hashes and revision history;
- signed credentials where available;
- separate observed-content evidence from declared/authenticated provenance;
- conflict/missing-evidence representation.

### WP5 — Independent safety/evaluation review

- methodological review;
- practitioner usability review;
- false-positive/misuse assessment;
- explicit abstention policy.

## 8. Success criteria

Final criteria must be workflow outcomes, not flattering model metrics alone.

Possible measures after discovery:

- practitioners can run the relevant workflow without uploading sensitive material;
- evidence bundles are reproducible from input hashes and software versions;
- users correctly distinguish measurement from authenticated provenance in usability testing;
- system abstains on predeclared insufficient-evidence cases;
- no raw sensitive content appears in exported evidence by default;
- external review findings and negative benchmark results are tracked publicly where safe.

## 9. Risks

Must include at least:

- false confidence / false attribution;
- use against journalists or sources;
- multilingual/domain bias;
- model drift;
- sensitive metadata leakage;
- provenance spoofing or missing provenance;
- high-risk users mistaking exploratory output for forensic proof.

Mitigations should include claim boundaries, abstention, local processing, evidence separation, versioned artifacts, and independent review.

## 10. Budget and duration

**Do not invent yet.**

Only budget after the scope is validated. OTF's published ideal range is not a target that must be maximised.

Prepare costs from actual work packages, including:

- engineering;
- practitioner/user research;
- independent review;
- multilingual data/evaluation where justified;
- documentation/localisation;
- project management;
- necessary infrastructure.

## 11. Current evidence available

Safe current facts:

- MIT-licensed open-source CogniPrint repository;
- deterministic versioned 12-dimensional text profile;
- hashes, reproducibility tooling and bounded evidence artifacts;
- external RAID model-family pilot infrastructure with pinned data revision;
- QVAC local-evidence prototype with a whitelist privacy boundary;
- privacy-boundary test: 3/3 PASS for removal of deliberately inserted raw/path fields;
- current scientific readiness remains `descriptive_only`;
- external methodological review gate remains `0/1`;
- no practitioner discovery result exists yet.

## Submission gate

Change HOLD to READY only when:

- [ ] at least three practitioner conversations are completed;
- [ ] at least two independent practitioners identify a substantially similar OTF-remit problem;
- [ ] a local/private-processing requirement is demonstrated;
- [ ] one primary intended user group is selected;
- [ ] existing-tool gap is documented;
- [ ] high-cost failure modes and abstention rule are documented;
- [ ] at least one non-sensitive evaluation scenario is available;
- [ ] work packages and budget derive from the evidence above;
- [ ] actual applicant/payment eligibility is re-checked against current OTF/OFAC requirements;
- [ ] current OTF Concept Note guide/form is re-read on submission day.
