# CogniPrint — GitHub Sponsors launch package

Status date: 2026-09-06

Launch state: **PREPARED / NOT PUBLISHED**

Purpose: fund open-source maintenance and research infrastructure without selling scientific conclusions or paywalling the evidence record.

## 1. Recommended account strategy

Use the maintainer's personal GitHub Sponsors profile first, with CogniPrint as the featured open-source work. Vietnam is currently listed by GitHub as a supported region for receiving sponsorships.

Before activation GitHub requires the normal Sponsors onboarding flow, including profile details, payout setup or fiscal host choice, tax information, 2FA, and GitHub review/approval.

Do not publish `.github/FUNDING.yml` until the actual Sponsors profile is approved and the final account slug is verified.

## 2. Short profile bio

> Independent researcher-engineer building CogniPrint, an open-source evidence lab for reproducible statistical text profiles, transformation robustness, and synthetic-language provenance research. I publish the code, protocols, failure boundaries, and negative results so the work can be inspected rather than trusted on authority.

## 3. Long profile description

> I maintain CogniPrint, an open-source research framework for measuring statistical traces in text and testing what evidence survives across human and AI-mediated transformation chains.
>
> The project is intentionally evidence-gated. Current scientific readiness is `descriptive_only`: the software can construct and compare reproducible text profiles and run controlled diagnostics, but it does not claim author identity, definitive AI origin, a unique source model, or forensic provenance.
>
> Sponsorship supports the open research process: reproducibility engineering, public benchmark maintenance, documentation, negative-result reporting, evidence tooling, independent review preparation, and the infrastructure needed to keep the project available to researchers and developers.
>
> Funding supports the research process, not the outcome. Sponsors cannot buy a favorable result, threshold, benchmark interpretation, review, citation, or scientific conclusion.

## 4. Suggested monthly tiers

Keep the initial tier set small. GitHub supports more tiers, but launching four clear levels is easier to understand and maintain.

### $5 / month — Supporter

For people who want to keep the public project alive.

Benefits:
- optional name on a public supporters page;
- sponsor badge/acknowledgement where appropriate;
- access to sponsor-only thank-you updates if enabled.

No scientific or product-access promise is required.

### $15 / month — Research Backer

Benefits:
- everything in Supporter;
- concise monthly research/engineering log;
- roadmap notes explaining what was measured, what failed, and what remains unknown;
- early notice of public challenge/release milestones.

The research log may be early-access, but the underlying scientific record, final protocols, code, benchmark results, and negative results remain public.

### $49 / month — Lab Member

Benefits:
- everything in Research Backer;
- monthly group demo/Q&A or recorded lab walkthrough;
- early preview of public UI/research-tool releases;
- ability to suggest non-binding usability/documentation questions for future demos.

No private scientific verdicts and no priority access to unsupported attribution claims.

### $149 / month — Lab Sponsor

Benefits:
- everything in Lab Member;
- quarterly sponsor briefing for a group/team;
- optional organization/name acknowledgement on the sponsor page;
- quarterly engineering/research roadmap discussion.

Explicit policy: sponsor input can influence priorities such as documentation, usability, packaging, or reproducibility tooling, but cannot dictate scientific outcomes or suppress negative results.

## 5. Optional one-time tiers

### $10 — Buy the lab a test run

One-time support for public benchmark/reproducibility infrastructure.

### $50 — Reproducibility boost

One-time support toward CI, hosting, dataset handling, and release archives.

### $250 — Open research patron

One-time acknowledgement plus invitation to the next public/group sponsor briefing, subject to platform capability and scheduling.

## 6. Sponsor independence policy

Publish this policy verbatim or substantially unchanged:

> **Sponsor independence policy**
>
> CogniPrint sponsorship funds maintenance, reproducibility, documentation, open benchmarking, and research infrastructure. Sponsorship does not purchase scientific endorsement, a favorable result, a model/author attribution, threshold selection, review outcome, citation, or suppression of negative findings. Scientific claims remain evidence-gated and public non-claims remain in force regardless of sponsor preference.

## 7. What must remain public

Never place these behind a sponsor paywall:

- source code required to reproduce the public release;
- JOSS software paper and accepted review record;
- mathematical/research manuscripts once publicly released;
- frozen/preregistered benchmark protocols;
- decisive benchmark results and negative results;
- evidence dossier and current scientific-readiness label;
- license/provenance information;
- corrections and retractions.

Sponsor-only material may include earlier commentary, educational walkthroughs, roadmap discussion, live Q&A, and release previews, provided public evidence is not delayed to manufacture exclusivity.

## 8. Candidate repository Sponsor button configuration

Only after GitHub Sponsors approval and slug verification, add:

```yaml
# .github/FUNDING.yml
github: [TakoVHS]
```

If the approved sponsored account uses another slug, replace it with the exact approved account. Do not merge a broken or unapproved funding link.

## 9. Profile assets/content checklist

- [ ] verify GitHub Sponsors eligibility dashboard for the actual account;
- [ ] enable/confirm 2FA;
- [ ] complete payout/fiscal-host decision;
- [ ] complete tax information accurately;
- [ ] set profile headline and long description from this package;
- [ ] feature `TakoVHS/CogniPrint-open`;
- [ ] create four monthly tiers;
- [ ] optionally create one-time tiers;
- [ ] publish Sponsor independence policy on the website/repository;
- [ ] verify all benefits are realistically deliverable;
- [ ] after approval, add and test Sponsor button in a separate PR;
- [ ] keep sponsor names/logos opt-in and privacy-respecting.

## 10. Launch stop conditions

Do not launch if:

1. payout/tax identity is not accurate;
2. the Sponsors profile implies university/institutional affiliation not actually held;
3. benefits promise scientific conclusions, private attribution results, or high-stakes determinations;
4. the public site hides `descriptive_only` or `external review 0/1` to improve conversion;
5. the sponsor button points at an unapproved or wrong account.

## 11. Positioning line

Use consistently on sponsor surfaces:

> **Funding supports the research process, not the outcome.**

## 12. Official references checked 2026-09-06

- GitHub Sponsors overview and supported regions: https://docs.github.com/en/sponsors/getting-started-with-github-sponsors/about-github-sponsors
- Personal-account setup: https://docs.github.com/en/sponsors/receiving-sponsorships-through-github-sponsors/setting-up-github-sponsors-for-your-personal-account
- Tier management: https://docs.github.com/en/sponsors/receiving-sponsorships-through-github-sponsors/managing-your-sponsorship-tiers

