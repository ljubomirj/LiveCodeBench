# MiroThinker-1.7-mini-Q4 vs Qwen3.5-35B-A3B-IQ4

Comparison target:
- local run: `MiroThinker-1.7-mini-Q4`
- reference run: `Qwen3.5-35B-A3B-IQ4`

Source runs:
- MiroThinker: `/home/ljubomir/rocm-glm-4.7-flash/benchmark_results_livecodebench_mirothinker_20260316_111253`
- Qwen: `/home/ljubomir/rocm-glm-4.7-flash/benchmark_results_livecodebench_qwen35b_recheck_20260315_171139`

## Overall

`Qwen3.5-35B-A3B-IQ4` remained clearly stronger on the same 92-problem subset:

- `MiroThinker-1.7-mini-Q4`: `0.7174`
- `Qwen3.5-35B-A3B-IQ4`: `0.7717`

Solved counts:
- `MiroThinker-1.7-mini-Q4`: `66 / 92`
- `Qwen3.5-35B-A3B-IQ4`: `71 / 92`

Delta:
- `-5` solved problems for MiroThinker
- `-0.0543` union pass@1

## Difficulty Breakdown

`MiroThinker-1.7-mini-Q4`:
- easy: `32 / 32 = 1.0000`
- medium: `28 / 39 = 0.7179`
- hard: `6 / 21 = 0.2857`

`Qwen3.5-35B-A3B-IQ4`:
- easy: `30 / 32 = 0.9375`
- medium: `33 / 39 = 0.8462`
- hard: `8 / 21 = 0.3810`

Delta:
- easy: `+0.0625`
- medium: `-0.1283`
- hard: `-0.0953`

Interpretation:
- MiroThinker was better on easy
- Qwen was substantially better on medium and hard
- the overall loss came from medium and hard

## Per-Window Scores

`MiroThinker-1.7-mini-Q4`:
- `2024-01-01 .. 2024-02-29`: `0.8056`
- `2024-05-01 .. 2024-06-30`: `0.7273`
- `2025-04-01 .. 2025-05-31`: `0.4167`

`Qwen3.5-35B-A3B-IQ4`:
- `2024-01-01 .. 2024-02-29`: `0.8333`
- `2024-05-01 .. 2024-06-30`: `0.8182`
- `2025-04-01 .. 2025-05-31`: `0.4167`

Interpretation:
- Qwen was better in windows 1 and 2
- window 3 was tied

## Runtime

`MiroThinker-1.7-mini-Q4`:
- total runtime: `9253s`

`Qwen3.5-35B-A3B-IQ4`:
- total runtime: `2988s`

Runtime delta:
- MiroThinker was slower by `6265s`
- MiroThinker took about `3.10x` the Qwen wall-clock time

## Caveat

This is not a perfectly apples-to-apples speed comparison:

- `MiroThinker-1.7-mini-Q4` was run with `thinking on`
- `Qwen3.5-35B-A3B-IQ4` was run with `thinking off`
- MiroThinker used `max_tokens=16384`
- Qwen used `max_tokens=10000`

So MiroThinker’s runtime penalty is driven heavily by much longer generations, not only raw decode throughput.

## Summary

On this 92-problem subset, `MiroThinker-1.7-mini-Q4` did reasonably well but did not beat the best local `Qwen3.5-35B-A3B-IQ4` setup:

- `0.7174` vs `0.7717`
- `66 / 92` vs `71 / 92`

And it was much slower in wall-clock time:

- `9253s` vs `2988s`

So the current best local baseline still remains `Qwen3.5-35B-A3B-IQ4`.
