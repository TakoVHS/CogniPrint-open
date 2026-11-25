# Human Verification Checklist

Status: **REQUIRED BEFORE TMLR SUBMISSION**

Purpose: ensure that every central idea, proof, citation boundary, and scientific
claim in the evidence-bounded promotion manuscript is independently understood
and defensible by the human author. This is a research-quality gate, not a
stylistic checklist.

## A. Definitions that must be reproducible from memory

The author should be able to define and explain, without reading the manuscript:

1. A certificate
   \[
   \kappa_i=(E_i,\mathcal W_{\kappa_i}^{A},\rho_i,B_i,\alpha_i)
   \]
   and the meaning of uniform frequentist validity.
2. A downstream claim
   \[
   c=(C,\mathcal W_c,\rho_c,\delta_c,\bar\alpha_c).
   \]
3. The difference between the certificate target \(\rho_i\) and claim target
   \(\rho_c\).
4. Why conjunctive use of all certificates requires
   \[
   \mathcal W_c
   \subseteq
   \mathcal W_T\cap\bigcap_i\mathcal W_{\kappa_i}^{A},
   \]
   not a union of certificate scopes.
5. The compatible-world set \(\mathcal V_T(b)\).
6. The feasible-bound domain \(\mathcal B_T\).
7. The sharp claim-risk envelope \(s_T^\star(b)\).
8. Why \(s_T^\star\) is intentionally a partial numerical object and why the
   infeasible branch is represented operationally by \(\bot\).

## B. Proofs that must be reproducible on a whiteboard

### B1. Monotonicity

Given \(b\le b'\), prove
\[
\mathcal V_T(b)\subseteq\mathcal V_T(b')
\]
and therefore
\[
s_T^\star(b)\le s_T^\star(b')
\]
whenever \(b\in\mathcal B_T\).

The author must be able to explain why feasibility of \(b\) implies feasibility
of \(b'\).

### B2. Feasible-domain sharp-envelope minimality

Define a feasible-domain warrant
\[
h:\mathcal B_T\to[0,1]
\]
that is coordinatewise nondecreasing and satisfies
\[
\rho_c(D)\le h(\rho_1(D),\ldots,\rho_m(D))
\]
for every deployment world.

Prove first that the risk vector
\((\rho_1(D),\ldots,\rho_m(D))\) lies in \(\mathcal B_T\), then prove
that \(s_T^\star\) is itself such a warrant, and only then prove
\[
s_T^\star(b)\le h(b).
\]

The author must explain why the older full-domain comparison statement was
underspecified and why the corrected result is elementary rather than a
novelty claim.

### B3. Conservative approximation

Prove that
\[
\widehat s_T(b)\ge s_T^\star(b)
\]
implies
\[
D\in\mathcal V_T(b)\Rightarrow
\rho_c(D)\le\widehat s_T(b).
\]

### B4. False-promotion soundness

Define certificate validity events \(G_i(D)\). On
\(\bigcap_iG_i(D)\), show that an unsafe deployment world belongs to the
compatible set and therefore cannot satisfy the promotion threshold. Conclude
using the union bound that
\[
\Pr_D(\mathrm{PROMOTE})\le \sum_i\alpha_i.
\]

The author must explicitly state that independence is not required.

### B5. Counterworld characterization

Prove that, for nonempty \(\mathcal V_T(b)\),
\[
D^\star\in\mathcal V_T(b),\ \rho_c(D^\star)>\delta_c
\]
exists if and only if
\[
s_T^\star(b)>\delta_c.
\]

## C. Failure modes that must be explainable

The author should be able to give a concrete example for each of:

- SCOPE_GAP;
- MODEL_OR_BOUND_INCONSISTENCY;
- NO_WARRANT_COMPUTED;
- DEPENDENCE_UNKNOWN.

For each case, explain why the correct output is unresolved rather than safe.

## D. AI-attribution counterexample

Without reading the paper, reconstruct the two-world example:

- the closed-set target is \(0.05\) in both worlds;
- the realized certificate bound is \(0.08\);
- downstream membership risk is \(0\) in one world and \(0.35\) in the other;
- the claim tolerance is \(0.10\).

Explain why the certificate remains valid while the downstream claim cannot be
promoted.

Then answer the reviewer question:

> What new evidence would be required to close this gap?

The answer must name an actual identification, transport, or additional evidence
channel; “more confidence in the same closed-set score” is not sufficient.

## E. Prior-art boundaries

The author must be able to explain, in one or two sentences each, why the paper
does **not** claim the following as novel:

- identified sets and partial identification;
- union-bound confidence accounting;
- error probability as a compositional logical resource;
- formal verification of statistical test requirements;
- machine-checkable evidence-to-claim assurance structures;
- compatible-world / sharp-envelope / counterworld reasoning in general.

Required works to understand before submission:

- Manski (2000);
- Imbens and Manski (2004);
- Stoye (2009);
- Bates et al. (2021), RCPS;
- Angelopoulos et al. (2025), Learn-then-Test;
- Angelopoulos et al. (2024), Conformal Risk Control;
- Pearl and Bareinboim (2014), transportability;
- Barthe et al. (2016), aHL;
- Aguirre et al. (2024), Eris;
- Kawamoto, Sato, and Suenaga (2024), BHL;
- Kawamoto, Kobayashi, and Suenaga (2025), StatWhy;
- Bloomfield and Rushby (2020), Assurance 2.0;
- Foster et al. (2021), Isabelle/SACM;
- Zhu (2026) full preprint, once the full text can be inspected.

## F. Claims the author must refuse to make

Before submission, the author should be comfortable explicitly rejecting these
overclaims:

- “CogniPrint introduces a new type theory.”
- “The sharp envelope theorem is a new risk-control result.”
- “The paper introduces a new probability theorem.”
- “The paper invents partial identification.”
- “A small closed-set error rate proves semantic provenance.”
- “An empty compatible set proves safety.”
- “The union of certificate scopes is enough for conjunctive composition.”
- “The confidence budgets require independence.”
- “The provenance-tagged failure-event idea is already established as novel.”

## G. Likely reviewer questions

The author should prepare concise answers to:

1. Why is this in scope for machine learning rather than only statistics or
   formal methods?
2. What does a practitioner gain beyond standard partial-identification
   language?
3. Is the Canonical Least Warrant theorem mathematically deep, or mainly a
   normalization result?
4. Why is the AI-attribution example informative if it is synthetic?
5. What is genuinely learned from the paper if the probability algebra is
   standard?
6. How does the framework differ from BHL/StatWhy?
7. How does it differ from assurance cases?
8. How does it differ from Zhu's proxy-evidence framework?
9. When is \(s_T^\star\) computationally tractable?
10. What empirical evidence would be needed for a future real deployment claim?

## H. Submission gate

Do not submit until all of the following are true:

- every proof in Section 3 and the fail-closed proposition can be reproduced
  independently by the author;
- every bibliography entry used in a novelty-boundary sentence has been checked
  against the source;
- the Zhu full-text comparison is complete or the manuscript is worded so that
  no unsupported distinction from Zhu is claimed;
- the TMLR PDF builds from a clean checkout with no undefined citations or
  references;
- the paper is anonymous in the review PDF;
- the first-page LLM-use disclosure is present;
- the author has read the final PDF end to end and can defend every scientific
  statement.

Passing this checklist is part of the scientific result: the goal is not merely
to possess a manuscript, but to be able to stand behind it as its author.
