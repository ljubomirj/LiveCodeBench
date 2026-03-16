# Pony Alpha 2 vs Qwen3.5-35B-A3B-IQ4

Comparison target:
- remote baseline: `pony-alpha-2`
- local baseline: `Qwen3.5-35B-A3B-IQ4`

Source runs:
- remote: `/home/ljubomir/rocm-glm-4.7-flash/benchmark_results_livecodebench_zai_pony_alpha2_20260315_220347`
- local: `/home/ljubomir/rocm-glm-4.7-flash/benchmark_results_livecodebench_qwen35b_recheck_20260315_171139`

## Overall

Both runs solved exactly `71 / 92` problems, so both round to the same union score:

- remote `pony-alpha-2`: `0.7717`
- local `Qwen3.5-35B-A3B-IQ4`: `0.7717`

This is a real tie, not a duplicated read of the same files.

Solved-set overlap:
- solved by both: `64`
- solved only by remote: `7`
- solved only by local: `7`

## Difficulty Breakdown

Remote `pony-alpha-2`:
- easy: `32 / 32 = 1.0000`
- medium: `29 / 39 = 0.7436`
- hard: `10 / 21 = 0.4762`

Local `Qwen3.5-35B-A3B-IQ4`:
- easy: `30 / 32 = 0.9375`
- medium: `33 / 39 = 0.8462`
- hard: `8 / 21 = 0.3810`

Interpretation:
- `pony-alpha-2` was better on easy and hard.
- `Qwen3.5-35B-A3B-IQ4` was better on medium.

## Per-Window Scores

Remote `pony-alpha-2`:
- `2024-01-01 .. 2024-02-29`: `0.7778`
- `2024-05-01 .. 2024-06-30`: `0.8636`
- `2025-04-01 .. 2025-05-31`: `0.4167`

Local `Qwen3.5-35B-A3B-IQ4`:
- `2024-01-01 .. 2024-02-29`: `0.8333`
- `2024-05-01 .. 2024-06-30`: `0.8182`
- `2025-04-01 .. 2025-05-31`: `0.4167`

## Remote-Only Solves

- `3263` | easy | `2024-01-20` | `divide-an-array-into-subarrays-with-minimum-cost-i`
- `3329` | medium | `2024-02-17` | `find-the-length-of-the-longest-common-prefix`
- `3395` | medium | `2024-05-04` | `minimum-length-of-anagram-concatenation`
- `3403` | medium | `2024-05-11` | `minimum-substring-partition-of-equal-character-frequency`
- `3438` | hard | `2024-06-15` | `peaks-in-array`
- `3460` | hard | `2024-06-22` | `count-the-number-of-inversions`
- `3469` | easy | `2024-06-29` | `maximum-height-of-a-triangle`

## Local-Only Solves

- `3292` | medium | `2024-02-24` | `earliest-second-to-mark-indices-i`
- `3297` | medium | `2024-02-03` | `minimum-time-to-revert-word-to-initial-state-i`
- `3308` | medium | `2024-02-17` | `apply-operations-to-make-string-empty`
- `3442` | medium | `2024-06-08` | `maximum-total-reward-using-operations-i`
- `3456` | medium | `2024-06-08` | `find-the-maximum-length-of-a-good-subsequence-i`
- `3464` | medium | `2024-06-22` | `maximize-total-cost-of-alternating-subarrays`
- `abc335_d` | medium | `2024-01-06` | `Loong and Takahashi`
