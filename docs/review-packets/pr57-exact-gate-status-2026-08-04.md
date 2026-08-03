# PR #57 exact-head M3 gate status — 4 August 2026

## Reverified identity

- PR: `#57`
- state: OPEN / Draft / not merged
- head: `6832729562d4587609bb93e5af3d4f7f96911d06`
- tree: `6d3754f3bc695c7e482c4f307316e6da99d29589`
- base: `d154b8610b182fe9110bf52fcadf02914498d356`
- changed files: `22`

## Hosted execution evidence

Deployment `dpl_2HvcX2jUduxtJLh1CABgKt8PT4Uw` used a clean clone of the immutable review-runner commit and checked out the exact PR head above.

Passed in the same hosted run:

- exact head/tree identity, 22-file scope and clean checkout;
- Ruff `0.16.1` with `E4,E7,E9,F`;
- `py_compile`;
- all 32 dossier tests twice with semantic output comparison;
- quickstart export/verification and mutation rejection;
- independent producer/verifier wheel installations;
- socket-blocked verification;
- main CLI export/verify/limits/purge;
- safe temporary-data purge;
- packaging contract;
- tracked-tree secret scan;
- sanitized public-release check (`575` selected, `25` excluded);
- rootless Buildah build under separate UID `10002` with VFS storage and chroot isolation;
- image runtime identity `10001:10001`;
- OCI CLI execution.

Observed marker:

```text
ROOTLESS_OCI_M3=PASS
```

## Remaining Nix blocker

The same run downloaded Nix `2.35.1`, but the single-user root installation stopped because the build group `nixbld` did not exist:

```text
error: the group 'nixbld' specified in 'build-users-group' does not exist
```

The next runner creates a dedicated `nixbld` group and ten build users, disables the Nix sandbox only inside the restricted Vercel build environment, and then performs:

- `nix flake check --no-write-lock-file`;
- two package builds with identical output path;
- packaged CLI execution;
- `nix develop` CLI execution;
- final scientific-boundary, exact head/tree and clean-worktree checks.

Vercel's Free API deployment quota is now exhausted. The API reports the next slot at **5 August 2026, 03:56 Asia/Ho_Chi_Minh**.

## Current status

```text
EXACT_HEAD_APPLICATION_GATES=PASS
ROOTLESS_OCI_M3=PASS
NIX_M3=PENDING_RERUN
EXACT_HEAD_M3_GATE=NOT_PASSED
GITHUB_ACTIONS=NOT_EXECUTED
```

PR #57 remains Draft. No merge, Ready transition, Stage B authorization, freeze, Research Lock, external registration or expanded scientific claim is authorized.
