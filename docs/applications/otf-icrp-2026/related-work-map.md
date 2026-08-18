# OTF ICRP 2026 — Related Work Map

> Working literature map for application `#22901`. This is not a claim of exhaustive coverage. The final Stage 2 proposal should re-check all citations and add host/reviewer-recommended work before submission.

## Why this map exists

OTF proposal evaluation asks whether the applicant understands existing work, known limitations, relevant communities, and how the proposed project builds on or complements prior efforts. This project sits at the intersection of internet-freedom measurement, multilingual content moderation, political/safety behavior in LLMs, summarization effects, and evidence/reproducibility practice.

The intended contribution is **not** to claim that multilingual model bias or refusal behavior has never been studied. Existing work clearly shows that language, culture, provider context, and moderation design can materially affect model behavior. The proposed ICRP contribution is narrower: a controlled Vietnamese/Russian/English study of *information after transformation* across translation, summarization, rewriting/paraphrase, moderation/refusal, and selected multi-step chains, coupled with privacy-aware evidence records and explicit failure/UNKNOWN semantics.

## A. Multilingual content moderation and guardrails

### Ye et al. (EACL 2023) — Multilingual Content Moderation: A Case Study on Reddit

This work studies multilingual content moderation and highlights cross-lingual transfer, label noise/human bias, rule variation, and challenges that are not captured by simple hate/offensive-language detection.

**Relevance to ICRP:** supports treating moderation as a rule- and context-sensitive process rather than a single universal classifier.

**Difference from proposed work:** the ICRP project is not primarily training a moderation classifier; it measures how several AI-mediated workflow classes alter sensitive information and preserves evidence of those changes.

Reference: https://aclanthology.org/2023.eacl-main.276/

### Upadhayay & Behzadan (LLMSEC 2025) — X-Guard: Multilingual Guard Agent for Content Moderation

X-Guard focuses on multilingual safety moderation and highlights the limitations of English-centric safeguards and the importance of transparency in multilingual moderation decisions.

**Relevance to ICRP:** reinforces the need for language-specific evaluation and transparent moderation evidence.

**Difference:** the proposed research studies downstream transformations and evidence sufficiency rather than building a guard model.

Reference: https://aclanthology.org/2025.llmsec-1.6/

### Fatehkia, Altinisik & Sencar (EACL 2026) — FanarGuard

FanarGuard evaluates safety and cultural alignment in Arabic/English and demonstrates that moderation evaluation can require culturally grounded benchmarks rather than generic English-centric safety criteria.

**Relevance:** supports the project's decision to avoid treating English-translated evaluation alone as sufficient for multilingual sensitive-content research.

**Difference:** the ICRP study targets Vietnamese/Russian/English transformation behavior and evidence preservation, not Arabic guardrail training.

Reference: https://aclanthology.org/2026.eacl-long.368/

### Tasawong et al. (Findings of ACL 2026) — SEA-SafeguardBench

SEA-SafeguardBench introduces a human-verified safety benchmark for Southeast Asian languages and reports that even strong models/guardrails remain challenged by locally grounded safety scenarios.

**Relevance:** strong regional motivation for native or context-grounded Southeast Asian evaluation rather than simply machine-translating English benchmarks.

**Difference:** the ICRP project includes Vietnamese but studies transformation effects across several workflow classes and languages rather than benchmarking safeguard classification alone.

Reference: https://aclanthology.org/2026.findings-acl.194/

## B. Political behavior and language dependence in LLMs

### Lim & Röttger (Findings of EACL 2026) — Bias in the East, Bias in the West

This bilingual study measures political bias on U.S.- and China-related issues and finds that prompt language and model origin systematically affect outputs, with strong language effects in some China-related topics.

**Relevance:** provides peer-reviewed evidence that political output behavior can depend on prompt language and context, supporting cross-language measurement as a first-class research question.

**Difference:** the ICRP project does not attempt to assign an ideological score to a model. It measures observable transformation effects such as omission, sanitization, drift, compression and uncertainty change.

Reference: https://aclanthology.org/2026.findings-eacl.122/

### Helwe, Balalau & Ceolin (Findings of ACL 2025) — Navigating the Political Compass

This work evaluates multilingual LLM political bias across languages/nationalities and reports that prompt language can materially influence displayed political orientation.

**Relevance:** further supports language-specific evaluation rather than assuming semantic equivalence across prompts and outputs.

Reference: https://aclanthology.org/2025.findings-acl.883/

### Gurgurov et al. (Findings of IJCNLP-AACL 2025) — Multilingual Political Views of Large Language Models

This work studies political orientation across multiple languages and model families, including paraphrase robustness and steering.

**Relevance:** shows that multilingual and paraphrase conditions are meaningful experimental dimensions.

**Difference:** the proposed ICRP study uses paraphrase/rewrite as transformation conditions and examines evidence/meaning changes rather than attempting to infer a stable political ideology for a model.

Reference: https://aclanthology.org/2025.findings-ijcnlp.17/

## C. Summarization and representation effects

### Huang, Maab & Yamagishi (ACL 2026) — When Bigger Isn't Better: Political Bias in Multi-News Summarisation

This study evaluates fairness and political representation in multi-document news summarization across multiple models and metrics.

**Relevance:** directly supports treating summarization as a transformation that may change representation/emphasis rather than as a neutral compression operation.

**Difference:** the ICRP proposal expands beyond news summarization into translation, rewriting/paraphrase, moderation/refusal and repeated transformation, with explicit evidence-lineage and privacy-aware outputs.

Reference: https://aclanthology.org/2026.acl-long.894/

## D. Directly related censorship/refusal research

### Noels et al. (2025 preprint) — What Large Language Models Do Not Talk About

This empirical preprint distinguishes hard censorship (refusal/denial) from soft censorship (selective omission/downplaying) across political topics, models from multiple regions, and six UN languages.

**Relevance:** highly aligned with the proposed distinction between refusal and subtler omission/sanitization effects.

**Important status:** preprint; it should not be represented as peer-reviewed unless its publication status changes before Stage 2 submission.

**Difference:** the ICRP proposal adds matched transformation workflows, Vietnamese focus, evidence-capsule lineage, repeated transformations, privacy-aware reproducibility, and practitioner-facing outputs.

Reference: https://arxiv.org/abs/2504.03803

## E. Internet-freedom measurement and information-controls practice

### Citizen Lab — censorship and content moderation research

Citizen Lab explicitly studies how online censorship/content moderation work at a technical level and how restrictive practices affect civil society. Its historical work on WeChat demonstrates that information controls can involve monitoring and censorship behavior within application-layer communications, not only network blocking.

**Relevance:** grounds the project in established information-controls research and highlights the importance of human-rights context, technical evidence, and careful claims.

References:

- https://citizenlab.ca/focus-area/censorship/
- https://citizenlab.ca/research/we-chat-they-watch/

### OONI and Censored Planet — open censorship measurement

OONI and Censored Planet provide mature examples of transparent, reproducible censorship measurement and public evidence/data practices.

**Relevance:** methodological inspiration for run identity, open artifacts, explicit measurement scope, false-positive handling, and community reuse.

**Difference:** their primary domain is network interference; application `#22901` focuses on AI-mediated transformation of content above the access layer.

References:

- https://ooni.org/
- https://censoredplanet.org/censoredplanet

## Proposed gap statement for Stage 2

Use a bounded statement such as:

> Recent research shows that multilingual LLM moderation, political behavior, and summarization can vary materially across language and context. Internet-freedom measurement projects also demonstrate the value of transparent, reproducible evidence. The proposed research builds on these strands by studying a different operational question: what happens to sensitive information after it passes through AI-assisted translation, summarization, rewriting/paraphrase, moderation/refusal, and repeated transformation workflows, and what minimum privacy-aware evidence is needed for another reviewer to assess those changes without forcing unsupported attribution?

Avoid claiming:

- that no prior research has studied LLM censorship or multilingual bias;
- that the proposed taxonomy is the first of its kind without a systematic literature review;
- that provider/model differences establish state intent;
- that observed moderation behavior establishes censorship policy or legal responsibility.

## Literature gate before Stage 2 submission

- [ ] Re-run literature search close to submission date.
- [ ] Verify publication status/DOIs for every cited work.
- [ ] Add Vietnamese- and Russian-specific scholarship where directly relevant and methodologically sound.
- [ ] Add host-adviser recommendations.
- [ ] Cite only work actually used to motivate design or interpretation.
- [ ] Keep direct comparison claims narrow and evidence-backed.
