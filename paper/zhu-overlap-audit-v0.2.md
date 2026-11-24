# Zhu 2026 Overlap Audit v0.2

Target:
Yaohui Zhu, *Proxy Evidence Certificates and World-Model Validation:
Evidence Fibers, Sharp Envelopes, and Counterworld Realization*,
Zenodo 20646079, version v1, published June 11, 2026.

Status: **FULL PUBLIC LATEX SOURCE REVIEWED / HIGH OVERLAP / NO PRIORITY CLAIM**

Reviewed public files from the Zenodo reproducibility ZIP:

- \`source/main.tex\`;
- \`source/theory/fiber_channel_theorem_package.tex\`;
- archive manifest and experiment filenames.

The direct PDF download path was rate-limited during this audit, but the full
public LaTeX source used to build the paper was retrievable from the Zenodo
container endpoint. The overlap conclusions below are therefore based on the
paper source, not only on the abstract.

## Confirmed direct overlap

### Target-relative proxy validation

Zhu explicitly frames validation as a proxy-evidence problem in which the
deployment target is generally not observed directly. The paper defines an
evidence map \(E\), a target map \(\Phi\), and requires target agreement across
worlds in the same evidence fiber.

**Verdict:** direct conceptual collision with any broad claim that CogniPrint
invented compatible-world or target-relative certificate semantics.

### No-promotion rule

The introduction and linear-claim section state a no-promotion principle:
proxy evidence may certify only target directions controlled by the declared
evidence unless the missing directions are covered by additional evidence or
an envelope.

**Verdict:** direct collision with a broad claim that "proxy certificate does
not automatically justify a stronger target" is unique to CogniPrint.

### Sharp target images and envelopes

Zhu proves the sharp target image of an evidence fiber and exact envelope
results for representation-induced compatible lift classes.

Relevant labels in the source include:

- \`thm:arxiv-optimal-certificate\`;
- \`thm:arxiv-exact-envelope\`;
- \`thm:arxiv-bounded-envelope\`;
- \`thm:exact-fiber-envelope\`;
- \`thm:bounded-ratio-envelope\`.

**Verdict:** direct collision.

### Audit/refinement repair

Zhu derives minimal quotient-closing audits and a coarsest
validation-sufficient refinement.

Relevant labels include:

- \`thm:arxiv-minimal-audit\`;
- \`thm:arxiv-coarsest-refinement\`;
- \`thm:minimal-audit\`.

**Verdict:** strong collision. CogniPrint must not claim evidence refinement or
audit closure as an original general idea.

### Counterworld realization

Zhu turns compatible-world ambiguity into finite-horizon world-model
counterexamples with identical latent evidence and separated deployment
targets.

Relevant labels include:

- \`thm:arxiv-realization\`;
- \`thm:fiber-channel-realization\`.

**Verdict:** direct collision.

### Frequentist coverage and union-bound reasoning

The theorem package contains a latent-transcript indistinguishability theorem.
For two indistinguishable models, a random interval certificate with
\(1-\alpha\) coverage in each model is shown, via the union bound, to contain
both separated target values with probability at least \(1-2\alpha\).

Relevant label:

- \`thm:latent-transcript-indistinguishability\`.

**Verdict:** partial but important collision. CogniPrint cannot use the mere
presence of frequentist \(1-\alpha\) coverage or union-bound reasoning as a
distinction from Zhu.

## Constructs not found as the same explicit interface

The complete reviewed Zhu source was searched for the corresponding explicit
constructs. The following were not found as the same named/formulated runtime
interface:

1. a family of heterogeneous certificate tuples
   \((E_i,\mathcal W_{\kappa_i}^{A},\rho_i,B_i,\alpha_i)\) feeding a distinct
   downstream claim risk \(\rho_c\);
2. a conjunctive static deployment-scope coverage obligation
   \[
   \mathcal W_c\subseteq
   \mathcal W_T\cap\bigcap_i\mathcal W_{\kappa_i}^{A};
   \]
3. a realized feasible-bound domain separated from the numerical envelope,
   with a nonnumeric fail-closed result on an empty compatible set;
4. the operational outcomes \`PROMOTE / ABSTAIN / UNRESOLVED\` with distinct
   reason codes for scope, feasibility and computation failures;
5. a general false-promotion budget formed by composing marginal validity
   guarantees from an arbitrary family of certificates.

This is an **absence observation about the reviewed Zhu source only**. It is
not a claim that these constructs are absent from all prior literature, and it
is not a priority claim for CogniPrint. aHL, Eris, assurance-case work, partial
identification and other formal methods remain relevant prior art.

## Updated overlap matrix

| Aspect | Zhu full-source evidence | CogniPrint | Verdict |
| --- | --- | --- | --- |
| Compatible worlds / evidence fibers | Explicit | Yes | **Direct collision** |
| Target-relative proxy validation | Explicit | Yes | **Direct collision** |
| No-promotion under target mismatch | Explicit | Yes | **Direct collision** |
| Sharp target image / envelope | Explicit | Yes | **Direct collision** |
| Audit / refinement repair | Explicit | Related | **Strong collision** |
| Counterworld realization | Explicit | Yes | **Direct collision** |
| Frequentist \(1-\alpha\) coverage | Explicit in two-world interval theorem | Yes | **Partial collision** |
| Union-bound confidence reasoning | Explicit \(1-2\alpha\) result | Yes | **Partial collision** |
| Heterogeneous multi-certificate tuple | Not found as same construct | Yes | **Potential distinction; no priority claim** |
| Explicit conjunctive deployment-scope gate | Not found as same construct | Yes | **Potential distinction; no priority claim** |
| Partial feasible-bound domain with nonnumeric bottom | Not found as same construct | Yes | **Potential distinction; no priority claim** |
| PROMOTE / ABSTAIN / UNRESOLVED reason-coded runtime | Not found as same construct | Yes | **Operational distinction; no priority claim** |
| AI-attribution application | Zhu application is learned representations/world models | Yes | **Different application** |

## Consequence for manuscript positioning

The manuscript should no longer present Zhu merely as "conceptually close".
It is **direct prior art for much of the semantic core**.

The defensible paper position is therefore:

- not a new compatible-world theory;
- not a new sharp-envelope principle;
- not a new no-promotion principle in the broad sense;
- not a new counterworld principle;
- not a new use of frequentist coverage or union bounds;
- instead, an ML-facing multi-certificate promotion interface that makes
  target, scope, feasibility, runtime diagnostics and false-promotion
  accounting explicit, plus an AI-attribution application.

If broader prior-art search finds the same explicit multi-certificate
fail-closed interface, the manuscript should be reframed as an application /
methodology paper or withheld until a genuinely additional result exists.

## Submission disposition

**HOLD.**

The Zhu full-source blocker is now substantially resolved, but the result is a
stronger overlap warning, not a green light. Before submission:

1. run a targeted broader search for the exact multi-certificate / scope /
   fail-closed interface;
2. preserve the application-first framing;
3. keep the Stage A empirical material descriptive-only;
4. obtain the required independent methodological review;
5. keep Stage B unauthorized.
