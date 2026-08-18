# OTF ICRP 2026 — Budget and Contracting Readiness

> Draft only. No award or contract exists.

## Core stipend

The 2026 ICRP solicitation states a fixed monthly stipend of USD 7,000 for eligible 3, 6, 9 or 12 month research periods.

For the submitted 12-month scope:

```text
USD 7,000 × 12 months = USD 84,000
```

The stipend is performance-based and released subject to satisfactory monthly progress and OTF/host oversight.

## Conservative optional direct-cost envelope

To preserve consistency with the prepared application package, the Stage 2 readiness budget uses:

```text
Core stipend:          USD 84,000
Equipment:             up to USD 3,000
Travel:                up to USD 3,500
Working maximum:       USD 90,500
```

The current OTF solicitation permits higher program maxima for equipment/travel in some cases, but this draft does not increase the working request merely because additional headroom exists.

Any equipment or travel line is optional and must be tied to a direct research need.

## Proposed equipment rationale

Equipment should be requested only if existing hardware cannot safely/reliably execute the contracted work. Permissible working categories may include:

- encrypted local research storage/backup media;
- replacement or dedicated compute/storage needed for reproducible local processing;
- security-relevant hardware directly necessary to separate restricted research data from public development data.

Not justified by this project:

- luxury upgrades;
- unrelated personal electronics;
- gaming/entertainment hardware;
- general business overhead.

Before Stage 2 submission, each requested item must have:

1. direct link to a research activity/deliverable;
2. estimated cost and procurement basis;
3. explanation of why existing equipment is insufficient;
4. host/OTF approval status where required.

## Proposed travel rationale

Travel is not a default requirement. It may be justified only for research activities such as:

- an agreed in-person host research period;
- a specific practitioner workshop/interview block that materially improves the study;
- a research dissemination/review activity requested or approved within the program.

Remote work remains the baseline assumption unless a concrete research benefit justifies travel.

## Costs intentionally excluded

This readiness budget does not include:

- overhead or general administration;
- profit/margin;
- unrelated hosting/services;
- speculative subcontractors;
- staff positions not in the submitted research scope;
- duplicated payment for existing CogniPrint assets;
- GitHub Pro or unrelated SaaS subscriptions solely for convenience;
- expenses without a mapped objective/deliverable.

## Monthly payment readiness

The workplan is structured so each month produces a reviewable deliverable package. A monthly package should include:

- completed activity summary;
- deliverable links/hashes;
- deviations and blockers;
- risks/remediation;
- host adviser review / traffic-light input;
- next-month work plan.

Payment status is determined by OTF/host under the eventual contract, not by this repository.

## Contracting information confirmed by OTF correspondence

OTF staff stated on August 18, 2026 that if the project is selected, contracting will require:

- applicant address;
- banking details;
- W-8 form supplied by OTF.

OTF also stated that Russian citizenship by itself does not prevent ICRP funding/contracting if selected.

These applicant-specific confirmations are correspondence records, not an award.

## Sensitive-data rule

The following must **never** be committed to this public repository:

- full residential address unless already intentionally public and specifically required in a public artifact;
- bank account/routing/SWIFT details;
- tax forms or tax identifiers;
- passport/identity-document scans;
- signatures;
- passwords, API keys, recovery codes;
- private host agreements containing confidential information.

Public readiness files may record only completion state, for example:

```text
ADDRESS_READY=YES/NO
BANKING_ROUTE_READY=YES/NO
W8_RECEIVED_FROM_OTF=YES/NO
W8_COMPLETED=YES/NO
HOST_AGREEMENT_READY=YES/NO
```

## Contracting checklist

### Before Stage 2 invitation

- [x] Applicant identity/public research profile prepared.
- [x] 12-month full-time scope drafted.
- [x] Core stipend math fixed at USD 84,000.
- [x] Conservative optional equipment/travel envelope documented.
- [x] Existing-vs-funded work boundary drafted.
- [x] Sensitive-contracting-data exclusion rule established.
- [ ] Stage 2 invitation received.

### After Stage 2 invitation, before proposal submission

- [ ] Capture exact portal fields and limits.
- [ ] Incorporate OTF determination/reviewer feedback.
- [ ] Confirm proposed host and named adviser, or follow OTF's instructions if host remains pending.
- [ ] Map every budget line to a workplan activity/deliverable.
- [ ] Validate whether optional equipment/travel is still needed.
- [ ] Confirm no overlapping funding pays for the same future deliverable.
- [ ] Run final factual/claim audit.

### If selected for legal/financial review

- [ ] Receive OTF contracting instructions.
- [ ] Provide address through OTF's authorized private channel.
- [ ] Provide banking information through OTF's authorized private channel.
- [ ] Receive and complete the OTF-provided W-8 form.
- [ ] Complete sanctions/debarment/compliance checks requested by OTF.
- [ ] Review host obligations and monthly oversight arrangement.
- [ ] Review contract scope, deliverables, reporting and payment terms.
- [ ] Keep signed/private contracting documents outside public GitHub.

## Budget consistency gate

`BUDGET_READY=PASS` only when the final Stage 2 portal request:

- matches the selected duration;
- contains no duplicated prior work;
- contains no unsupported overhead;
- maps optional direct costs to specific activities;
- is consistent with OTF's then-current instructions;
- is reconciled against any host-provided resources or overlapping support.
