# Campaign 004 Input Set

This directory is reserved for a genuinely separate empirical input set for `empirical-campaign-004`.

## Intended structure

- `original.txt`
- `edited.txt`
- `variants/`

## Rule

Campaign-004 should not reuse the earlier micro-series or the campaign-003 baseline. It should use a new baseline and controlled variants derived from that new baseline.

## Recommended steps

1. Place a new baseline text in `original.txt`.
2. Place a light edit of that same baseline in `edited.txt`.
3. Add 5 to 10 controlled variants under `variants/`.
4. Record source provenance in `workspace/input/SOURCES.md`.
5. Run `make validate-sources` before creating or running the campaign config.

## Suggested variant axes

- punctuation cleanup
- minor lexical substitution
- sentence split/merge
- word-order shift
- compressed version
- expanded version
- formalized style
- informalized style
- strong rewrite preserving the central claim
- translated or cross-lingual version
