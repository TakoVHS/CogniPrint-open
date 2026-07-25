# XRPL Developer Funding — CogniPrint fit memo

Status date: 2026-07-25

## Decision

**NO-GO for the current CogniPrint roadmap.**

Do not add XRP Ledger transactions, tokens, NFTs, payments, or ledger records merely to become grant-eligible.

## Current official funding facts

Official funding overview: https://xrpl.org/community/developer-funding

As verified on 2026-07-25:

- XRPL Grants are intended for developers, teams, and startups **building directly on the XRP Ledger**;
- published grant funding is `$10,000–$200,000`;
- applicants are expected to have coding experience, a GitHub repository, a project narrative, at least one developer on the core team, and a budget/milestone plan;
- the XRPL Accelerator is for scalable XRPL startups and publishes a `$50,000` grant plus a venture-funding pitch opportunity.

The amount available is not itself a reason to use XRPL.

## Why CogniPrint is not a natural fit today

CogniPrint's current technical needs are:

- deterministic local measurement;
- reproducible evidence bundles;
- privacy-preserving/local explanation;
- controlled external benchmark evaluation;
- authenticated provenance as a separate evidence class;
- durable content-addressed evidence state where useful.

None of these currently requires XRPL's payment, token, decentralized exchange, AMM, or ledger transaction primitives.

A ledger anchor could be added, but without a real user/workflow requirement it would be ornamental architecture. That would weaken both the grant application and the research design.

## What would change the decision

Re-open XRPL only if a real CogniPrint workflow emerges where an XRPL-native property is essential, for example:

- an existing XRPL ecosystem project needs CogniPrint evidence verification;
- an XRPL-native credential/payment/workflow requires machine-readable evidence receipts;
- a funded partner requires verifiable evidence state linked to XRPL transactions;
- users need an XRPL-specific provenance or settlement feature that cannot be achieved more simply off-ledger.

Even then, the project should demonstrate the user requirement before writing an XRPL grant proposal.

## Comparison with Autonomys

For the current research roadmap, Autonomys has the clearer infrastructure fit because Auto Drive directly provides durable content-addressed storage for bounded reproducibility artifacts, and the Subspace Foundation explicitly funds verifiable/privacy-preserving AI research and integrations.

That does not make Autonomys scientifically necessary for all CogniPrint deployments; it simply gives the proposed Evidence Capsule a concrete infrastructure property to evaluate.

## Recommendation

Keep XRPL out of the active grant pipeline. Re-check the official programme only if an authentic XRPL-native use case appears.