# PR #57 exact-head M3 gate status — 4 August 2026

## Reverified identity

- PR: `#57`
- state: OPEN / Draft / not merged
- head: `6832729562d4587609bb93e5af3d4f7f96911d06`
- tree: `6d3754f3bc695c7e482c4f307316e6da99d29589`
- base: `d154b8610b182fe9110bf52fcadf02914498d356`
- changed files: `22`

## Rerun result

The prepared clean-checkout runner used:

- Ruff `0.16.1` with `E4,E7,E9,F`;
- two executions of all 32 dossier tests with semantic output comparison;
- quickstart and independent producer/verifier installations;
- socket-blocked verification;
- main CLI and safe purge;
- packaging contract, secret scan and sanitized public-release check;
- Buildah under separate unprivileged UID `10002`, VFS storage and chroot isolation;
- Nix flake/package/dev-shell checks;
- final exact head/tree/scope/worktree checks.

No deployment was created. The Vercel connector rejected the large inline runner at its transport safety layer, and the endpoint did not accept local file references as an alternative.

This is an infrastructure/tooling blocker before execution, not a repository test failure. It does not produce new PASS evidence.

## Current status

```text
EXACT_HEAD_M3_GATE=NOT_PASSED
ROOTLESS_OCI_M3=NOT_EXECUTED_IN_RERUN
NIX_M3=NOT_EXECUTED_IN_RERUN
GITHUB_ACTIONS=NOT_EXECUTED
```

Earlier hosted evidence for the same content tree remains limited to application-layer gates through secret scan and sanitized public-release check. PR #57 must remain Draft. No merge, Ready transition, Stage B authorization, freeze, Research Lock, external registration or expanded scientific claim is authorized.
