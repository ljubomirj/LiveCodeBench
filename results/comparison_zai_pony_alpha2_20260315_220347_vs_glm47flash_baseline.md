# Pony Alpha 2 vs GLM-4.7-Flash-Q4

Comparison target:
- remote baseline: `pony-alpha-2`
- local baseline: `GLM-4.7-Flash-Q4`

Source runs:
- remote: `/home/ljubomir/rocm-glm-4.7-flash/benchmark_results_livecodebench_zai_pony_alpha2_20260315_220347`
- local: `/home/ljubomir/rocm-glm-4.7-flash/benchmark_results_livecodebench_glm_baseline_20260310_151117`

## Overall

Remote `pony-alpha-2` was clearly stronger on the same 92-problem subset:

- remote `pony-alpha-2`: `0.7717`
- local `GLM-4.7-Flash-Q4`: `0.4891`

Solved counts:
- remote `pony-alpha-2`: `71 / 92`
- local `GLM-4.7-Flash-Q4`: `45 / 92`

Delta:
- `+26` solved problems
- `+0.2826` union pass@1

## Difficulty Breakdown

Remote `pony-alpha-2`:
- easy: `32 / 32 = 1.0000`
- medium: `29 / 39 = 0.7436`
- hard: `10 / 21 = 0.4762`

Local `GLM-4.7-Flash-Q4`:
- easy: `30 / 32 = 0.9375`
- medium: `12 / 39 = 0.3077`
- hard: `3 / 21 = 0.1429`

Delta:
- easy: `+0.0625`
- medium: `+0.4359`
- hard: `+0.3333`

Interpretation:
- `pony-alpha-2` was better across all three difficulty buckets.
- The largest gap was on medium problems.

## Per-Window Scores

Remote `pony-alpha-2`:
- `2024-01-01 .. 2024-02-29`: `0.7778`
- `2024-05-01 .. 2024-06-30`: `0.8636`
- `2025-04-01 .. 2025-05-31`: `0.4167`

Local `GLM-4.7-Flash-Q4`:
- `2024-01-01 .. 2024-02-29`: `0.5556`
- `2024-05-01 .. 2024-06-30`: `0.5000`
- `2025-04-01 .. 2025-05-31`: `0.2500`

Interpretation:
- `pony-alpha-2` was ahead in every window.
- The gap was largest in the middle window.

## Runtime

Remote `pony-alpha-2`:
- total runtime: `3269s`

Local `GLM-4.7-Flash-Q4`:
- total runtime: `7457s`

Runtime delta:
- remote was faster by `4188s`
- remote took about `44%` of the GLM wall-clock time

## Summary

On this 92-problem LiveCodeBench subset, `pony-alpha-2` was decisively better than the best recorded `GLM-4.7-Flash-Q4` run:

- much higher union score
- better on easy, medium, and hard
- better in every time window
- substantially faster end-to-end
