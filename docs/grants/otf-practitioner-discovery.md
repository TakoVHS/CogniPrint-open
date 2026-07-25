# OTF practitioner discovery protocol

Status: discovery instrument for Grant Track B. This is not evidence that CogniPrint currently fits OTF's remit.

## Objective

Determine whether a real internet-freedom workflow exists where a local, open-source CogniPrint evidence layer would materially help journalists, human-rights investigators, or digital-security practitioners working under censorship, surveillance, or repressive information controls.

The discovery question is deliberately narrower than "Do you like CogniPrint?"

> **When sensitive or contested digital text appears in a high-risk investigation, is there a decision that practitioners cannot make safely or confidently with existing tools, and would a local uncertainty-aware evidence/provenance layer improve that decision?**

A negative answer is a useful outcome and should result in an OTF NO-GO rather than forcing a grant narrative.

## Research ethics and safety boundary

Do not request or collect:

- names of vulnerable sources;
- unpublished case material;
- raw documents that may expose a source or investigation;
- credentials, account identifiers, private URLs, access tokens, or device information;
- operational security details that are not necessary to understand the workflow;
- information that would identify a person facing repression;
- material a practitioner is not already authorized to discuss.

Practitioners should be invited to answer using **abstract or synthetic examples**. If a concrete example is useful, it should be sanitized by the practitioner before sharing.

By default, discovery notes should record no personal data beyond the organisation/contact role already public or voluntarily supplied.

## Consent language

Before substantive questions, state:

> This is early product/research discovery, not a request for endorsement. Please do not send sensitive case data. I am trying to understand whether the problem exists and what would make a tool unsafe or useless. I will not quote you or identify your organisation in a grant application without explicit permission.

## 20-minute interview structure

### 1. Current workflow

1. In investigations involving contested or suspicious digital text, what decision are you actually trying to make?
2. What evidence do you currently trust enough to affect that decision?
3. Which tools or manual steps do you already use?
4. Where does the workflow currently fail, become too slow, or become unsafe?

### 2. Privacy and threat model

5. Is there material you would avoid uploading to a third-party AI/analysis service? Why?
6. Would local/offline processing meaningfully change whether you could use a tool?
7. Which metadata must never be stored in an analysis artifact?
8. Who is the realistic adversary: platform, government, malicious actor, employer, opposing party, or someone else?

### 3. Evidence and provenance

9. Would a statistical text profile be useful if it was explicitly presented as a hypothesis rather than proof?
10. Which provenance signals matter in your workflow: hashes, revision history, signed credentials, publication records, tool logs, timestamps, or other records?
11. When content-derived signals and declared provenance disagree, what would you want the tool to show?
12. Which conclusion would be too dangerous for a tool to make automatically?

### 4. Failure cost

13. What is worse in your context: a false accusation, a missed manipulation, or an inconclusive answer?
14. When should the tool abstain and say "insufficient evidence"?
15. Would you ever use a model-family suggestion? If yes, for triage, investigation, publication, legal evidence, or something else?

### 5. Deployment reality

16. Which languages and writing systems matter most?
17. What hardware/connectivity constraints are common?
18. Is a desktop CLI/workstation acceptable, or would a browser/mobile workflow be necessary?
19. Does the tool need to operate without internet after installation?
20. What one output would make you try a prototype in a non-sensitive test case?

## Post-interview note template

Record only:

- interview ID: `P01`, `P02`, ...;
- date;
- organisation category (for example: human-rights archive, independent-media digital forensics, frontline AI/media integrity);
- role category, not necessarily a personal name;
- permission boundary: private notes / anonymised aggregate / organisation may be named / direct quote permitted;
- problem statement in the practitioner's terms;
- current tools/workaround;
- privacy requirement;
- high-cost failure modes;
- relevant languages/domains;
- desired output;
- explicit reasons CogniPrint would **not** help;
- follow-up experiment, if any.

Do not commit private interview notes to the public repository. Only an approved anonymised synthesis may become public evidence.

## GO / NO-GO scoring rubric

Evaluate after at least three independent practitioner conversations, preferably from at least two organisation/workflow types.

### GO requires all of the following

- at least two practitioners describe substantially similar real problems within censorship/surveillance/internet-freedom work;
- local/private processing is a material requirement, not a cosmetic preference;
- there is a concrete decision or workflow step the proposed evidence output could improve;
- current tools leave a documented gap;
- the most valuable output can be delivered without unsafe automated attribution;
- practitioners accept uncertainty/abstention as part of the workflow;
- a prototype can be evaluated with non-sensitive or synthetic test material.

### NO-GO if any of the following dominates

- practitioners only want a universal "AI detector";
- the use case is primarily academic integrity, marketing, plagiarism, or generic enterprise compliance;
- the workflow does not relate to people affected by censorship or repressive surveillance;
- practitioners require definitive author/model attribution that the evidence cannot support;
- local processing provides no meaningful safety benefit;
- existing tools already solve the problem sufficiently;
- meaningful evaluation would require publishing sensitive case data.

## Minimum discovery evidence before an OTF Concept Note

Do not submit until the repository can truthfully state, without exposing practitioner identities:

1. number and broad categories of practitioners consulted;
2. repeated problem pattern(s);
3. privacy/threat-model requirement;
4. existing-tool gap;
5. proposed bounded workflow;
6. high-cost failure modes and abstention rule;
7. languages/deployment constraints;
8. at least one non-sensitive evaluation scenario;
9. explicit GO/NO-GO decision.

The practitioner evidence should shape the technical work packages. It must not be retrofitted after a grant narrative has already been decided.
