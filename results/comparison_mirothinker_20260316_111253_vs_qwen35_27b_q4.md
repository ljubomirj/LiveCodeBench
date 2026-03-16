# MiroThinker-1.7-mini-Q4 vs Qwen3.5-27B-Q4

Comparison target:
- local run: `MiroThinker-1.7-mini-Q4`
- reference run: `Qwen3.5-27B-Q4`

Source runs:
- MiroThinker: `/home/ljubomir/rocm-glm-4.7-flash/benchmark_results_livecodebench_mirothinker_20260316_111253`
- Qwen: `/home/ljubomir/rocm-glm-4.7-flash/benchmark_results_livecodebench_matrix_20260312_201434`

## Overall

`MiroThinker-1.7-mini-Q4` scored slightly higher on the same 92-problem subset:

- `MiroThinker-1.7-mini-Q4`: `0.7174`
- `Qwen3.5-27B-Q4`: `0.6957`

Solved counts:
- `MiroThinker-1.7-mini-Q4`: `66 / 92`
- `Qwen3.5-27B-Q4`: `64 / 92`

Delta:
- `+2` solved problems
- `+0.0217` union pass@1

## Difficulty Breakdown

`MiroThinker-1.7-mini-Q4`:
- easy: `32 / 32 = 1.0000`
- medium: `28 / 39 = 0.7179`
- hard: `6 / 21 = 0.2857`

`Qwen3.5-27B-Q4`:
- easy: `32 / 32 = 1.0000`
- medium: `26 / 39 = 0.6667`
- hard: `6 / 21 = 0.2857`

Delta:
- easy: `+0.0000`
- medium: `+0.0512`
- hard: `+0.0000`

Interpretation:
- the gain came entirely from medium problems
- easy and hard were tied

## Per-Window Scores

`MiroThinker-1.7-mini-Q4`:
- `2024-01-01 .. 2024-02-29`: `0.8056`
- `2024-05-01 .. 2024-06-30`: `0.7273`
- `2025-04-01 .. 2025-05-31`: `0.4167`

`Qwen3.5-27B-Q4`:
- `2024-01-01 .. 2024-02-29`: `0.6944`
- `2024-05-01 .. 2024-06-30`: `0.7955`
- `2025-04-01 .. 2025-05-31`: `0.3333`

Interpretation:
- MiroThinker was better in windows 1 and 3
- Qwen was better in window 2

## Runtime

`MiroThinker-1.7-mini-Q4`:
- total runtime: `9253s`

`Qwen3.5-27B-Q4`:
- total runtime: `5092s`

Runtime delta:
- MiroThinker was slower by `4161s`
- MiroThinker took about `1.82x` the Qwen wall-clock time

## Caveat

This is not a perfectly apples-to-apples speed comparison:

- `MiroThinker-1.7-mini-Q4` was run with `thinking on`
- `Qwen3.5-27B-Q4` was run with `thinking off`
- MiroThinker used `max_tokens=16384`
- Qwen used `max_tokens=4000`

So MiroThinker’s large runtime penalty is driven heavily by much longer generations, not just lower raw decode speed.

## Summary

On this 92-problem subset, `MiroThinker-1.7-mini-Q4` beat `Qwen3.5-27B-Q4` slightly on accuracy:

- `0.7174` vs `0.6957`
- `66 / 92` vs `64 / 92`

But it was much slower in wall-clock time:

- `9253s` vs `5092s`

So the tradeoff here is a small quality gain for a large runtime cost.
