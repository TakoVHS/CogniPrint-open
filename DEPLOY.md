# CogniPrint deployment and rollback

CogniPrint's public web presence is a static reviewer-facing site. It is not a database-backed API service, so deployment readiness is defined by exact-artifact provenance, reviewer-contract checks, static availability, and rollback capability rather than synthetic server endpoints.

## Canonical artifact

The intended canonical public artifact is the `web/` directory from the exact approved `main` commit.

Target production surface:

- Vercel project: `cogniprint-public-site`
- Vercel project ID: `prj_n8WGeckWl8Xkn6lCv8C4ERMtVSKJ`
- production domain: `cogniprint.org`
- canonical repository: `TakoVHS/CogniPrint-open`
- canonical source directory: `web/`

As of 2026-09-06, the production surfaces are not yet proven to be sourced from one identical repository artifact. Treat that as deployment drift until the domain, Vercel deployment, and `main:web/` are verified against the same approved commit.

## Pre-deployment gate

Do not promote a deployment merely because Vercel reports `READY`. On the exact candidate commit:

```bash
make verify
```

At minimum preserve evidence for:

- exact commit SHA;
- Python version(s) used for verification;
- full test-discovery result;
- Ruff result;
- reviewer web contract result;
- public benchmark contract result;
- tracked-tree secret scan result;
- sanitized export check result;
- package build result.

If the GitHub-hosted runner does not reach executable steps, record the run as `NOT_EXECUTED`/`NOT_VERIFIED`; do not convert an infrastructure failure into a code PASS or FAIL.

## Production deployment procedure

1. Start from a complete checkout of the approved `main` commit.
2. Confirm `git rev-parse HEAD` is the approved SHA and the worktree is clean.
3. Run the pre-deployment gate above.
4. Deploy only `web/` to the configured `cogniprint-public-site` Vercel project. Keep Vercel tokens and account credentials outside the repository.
5. Record the resulting Vercel deployment ID and the source commit SHA together.
6. Verify the generated Vercel production URL returns HTTP 200 and visually matches `web/index.html` from that SHA.
7. Verify `https://cogniprint.org` resolves to the same content before declaring deployment synchronized.
8. Re-run `python scripts/check_reviewer_web_contract.py` against the repository artifact whenever the reviewer narrative changes.

DNS or production-domain changes are separate production mutations and require explicit approval. Do not switch the domain merely to make an audit appear green.

## Rollback

Rollback is artifact-based:

1. identify the last known-good Vercel deployment and its source commit SHA;
2. promote/reassign that known-good deployment in Vercel rather than rebuilding an unknown worktree;
3. verify both the Vercel production URL and `cogniprint.org` after rollback;
4. record the rollback deployment ID, source SHA, reason, and verification result.

If the previous deployment cannot be tied to a repository SHA, it is not a fully auditable rollback target; preserve it only as an emergency availability fallback and restore commit-to-deployment provenance immediately afterward.

## Monitoring appropriate to this architecture

For the current static site, the minimum production checks are:

- deployment state is `READY`;
- build logs contain no errors;
- production URL and custom domain return HTTP 200;
- content corresponds to the approved `web/` artifact;
- reviewer-contract checks still pass in the repository.

Postgres, Redis, rate limiting, `/health`, `/ready`, Prometheus server, and OpenTelemetry collectors are not current CogniPrint dependencies and should not be added solely to satisfy a generic backend checklist.
