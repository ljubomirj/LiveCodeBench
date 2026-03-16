# LiveCodeBench Qwen Final Rerun

Run directory: `benchmark_results_livecodebench_matrix_20260312_201434`

Configuration:
- Thinking: OFF
- Chat template: `scripts/qwen3.5_chat_template.jinja`
- `CHAT_TEMPLATE_KWARGS={"enable_thinking":false}`
- `temperature=0.0`
- `top_p=1.0`
- `max_tokens=4000`

## Final union scores

Union over 92 problems:

| Model | Overall | Easy | Medium | Hard |
|---|---:|---:|---:|---:|
| Qwen3.5-35B-A3B-IQ4 | 0.7283 | 0.9688 | 0.7179 | 0.3810 |
| Qwen3.5-27B-Q4 | 0.6957 | 1.0000 | 0.6667 | 0.2857 |
| Qwen3.5-9B-Q8 | 0.6196 | 0.9062 | 0.5897 | 0.2381 |

## Per-window Pass@1

| Model | 2024-01-01..2024-02-29 | 2024-05-01..2024-06-30 | 2025-04-01..2025-05-31 |
|---|---:|---:|---:|
| Qwen3.5-35B-A3B-IQ4 | 0.7222 | 0.8182 | 0.4167 |
| Qwen3.5-27B-Q4 | 0.6944 | 0.7955 | 0.3333 |
| Qwen3.5-9B-Q8 | 0.6389 | 0.7045 | 0.2500 |

## Comparison vs prior corrected rerun

Reference run: `benchmark_results_livecodebench_matrix_20260310_110404`

Union over 92 problems:

| Model | Prior overall | Final overall | Delta |
|---|---:|---:|---:|
| Qwen3.5-35B-A3B-IQ4 | 0.7609 | 0.7283 | -0.0326 |
| Qwen3.5-27B-Q4 | 0.6087 | 0.6957 | +0.0870 |
| Qwen3.5-9B-Q8 | 0.5543 | 0.6196 | +0.0653 |

Reference union scores by difficulty:

| Model | Prior easy | Prior medium | Prior hard |
|---|---:|---:|---:|
| Qwen3.5-35B-A3B-IQ4 | 1.0000 | 0.7692 | 0.3810 |
| Qwen3.5-27B-Q4 | 0.9688 | 0.5385 | 0.1905 |
| Qwen3.5-9B-Q8 | 0.9375 | 0.5385 | 0.0000 |

## Notes

- This rerun clearly outperforms the thinking-on pilot and supports the final Qwen recipe: thinking off, special template, deterministic decoding, `max_tokens=4000`.
- Relative to the prior corrected rerun, 27B and 9B improved materially, while 35B dropped slightly.
- `Qwen3.5-35B-A3B-IQ4.run.log` contains one `timeout occured: alarm went off` during the first window, but the run completed and still produced the strongest 35B result in this run.
