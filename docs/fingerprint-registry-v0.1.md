# CogniPrint Fingerprint Registry v0.1

Status: **research registry specification; no production model registry is claimed.**

## Purpose

A model fingerprint is not timeless.

Model providers update weights, safety layers, system prompts, routing, decoding defaults and serving infrastructure. Open-weight communities publish new checkpoints and fine-tunes. The observable distribution of outputs can therefore drift even when the public family name appears unchanged.

The CogniPrint Fingerprint Registry is a versioned research index for **observed benchmark reference distributions**, not a database of unique model identities.

## Registry principle

Every reference fingerprint must answer:

- **what source/version was observed?**
- **when was it observed?**
- **under which prompts/domains/settings?**
- **which feature/extractor version produced it?**
- **which dataset/manifest generated the distribution?**
- **what transformations were included/excluded?**
- **how well did it separate from simple baselines?**
- **when should the reference be considered stale?**

A bare label such as `model=gpt-x` is insufficient provenance for a fingerprint.

## Conceptual registry key

`family → source/version → observation window → benchmark configuration → feature-map version`

Each unique combination produces a separate registry entry.

## Minimum entry fields

A future machine-readable registry entry should contain at least:

- `registry_schema`;
- `entry_id`;
- `family_label`;
- `source_label`;
- `source_version_or_checkpoint` where known;
- `provider_or_repository`;
- `observation_start`;
- `observation_end`;
- `dataset_id`;
- `dataset_revision`;
- `prompt_manifest_sha256`;
- `generation_config_sha256`;
- `sample_manifest_sha256`;
- `feature_map_version`;
- `extractor_commit_sha`;
- `sample_count`;
- `domain_strata`;
- `length_strata`;
- `transformation_scope`;
- `reference_summary`;
- `baseline_results`;
- `calibration_context` where applicable;
- `known_limitations`;
- `drift_status`;
- `supersedes_entry_id` where applicable;
- `evidence_sha256` or Evidence Capsule reference.

## Reference summary

The registry should not reduce an entry to a single centroid unless evidence supports that representation.

Possible stored summaries include:

- per-feature mean/variance;
- robust quantiles;
- covariance where sample size permits;
- class centroid for transparent baselines;
- calibration parameters;
- distribution-distance references;
- classifier-independent diagnostic statistics.

Learned model weights belong in separately versioned artifacts, not hidden inside the registry record.

## Drift states

Each entry should expose one of:

- `CURRENT_REFERENCE` — recently validated under its declared scope;
- `DRIFT_CHECK_DUE` — reference age or upstream change requires re-test;
- `DRIFT_DETECTED` — statistically/materially changed reference distribution;
- `SUPERSEDED` — replaced by a newer registry entry;
- `RETIRED` — no longer suitable for attribution experiments;
- `INSUFFICIENT_EVIDENCE` — reference never reached the evidence threshold required for use.

## Drift experiment

A drift check should compare two time/version windows using the same frozen protocol where possible.

At minimum report:

- feature-level distribution changes;
- within-version versus between-version distances;
- family classification degradation when old references evaluate new outputs;
- calibration degradation;
- UNKNOWN/false-known behaviour;
- prompt/domain interaction effects.

A drift claim should not be based on a handful of anecdotal prompts.

## Temporal attribution boundary

A future experiment may ask:

> “Is this artifact more consistent with reference distribution R1 observed in period X than with R2 observed in period Y?”

This is a benchmark-bounded distribution comparison.

It is **not** proof that the artifact was generated during period X or by a uniquely identified model.

## Staleness rule

No registry entry should be used indefinitely.

A release using fingerprint references must define at least one revalidation trigger, such as:

- elapsed observation time;
- known upstream model/checkpoint update;
- provider behaviour change;
- significant calibration degradation;
- drift metric crossing a preregistered threshold;
- new benchmark evidence showing the reference is no longer discriminative.

## Relationship to UNKNOWN

Stale references increase the risk that an unseen or updated model is forced into the nearest known class.

The registry therefore exists partly to support safer abstention.

If no current reference distribution fits the evidence sufficiently well, the preferred output is:

`UNKNOWN / OUT OF REFERENCE SPACE`

not the nearest historical label.

## Relationship to provenance

The Fingerprint Registry contains observed statistical reference evidence.

It must remain separate from authenticated provenance such as:

- signed model/provider attestations;
- C2PA-style credentials;
- execution logs;
- repository/checkpoint records;
- API/tool records.

A registry similarity can support a hypothesis. An authenticated record can support a declared event. Neither should be silently converted into the other.

## Attribution Challenge 001

Challenge 001 should seed the first experimental registry entries.

Those entries must be labelled as **challenge references**, carry the exact challenge protocol and observation window, and must not be marketed as universal permanent fingerprints.

## Publication rule

A public registry should expose enough metadata to reproduce or audit the reference while avoiding redistribution of restricted or sensitive source content.

Hashes, manifests, feature summaries, configuration records and Evidence Capsules should be preferred where raw data cannot be redistributed.
