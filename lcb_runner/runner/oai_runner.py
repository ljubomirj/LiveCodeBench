import json
import os
from time import sleep

try:
    import openai
    from openai import OpenAI
except ImportError as e:
    pass

from lcb_runner.lm_styles import LMStyle
from lcb_runner.runner.base_runner import BaseRunner


class OpenAIRunner(BaseRunner):
    _default_client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

    def __init__(self, args, model):
        base_url = os.getenv("OPENAI_API_BASE") or os.getenv("OPENAI_BASE_URL")
        super().__init__(args, model)
        if base_url:
            self.client = OpenAI(
                api_key=os.getenv("OPENAI_KEY") or "EMPTY",
                base_url=base_url,
            )
        else:
            self.client = OpenAIRunner._default_client

        if model.model_style == LMStyle.OpenAIReasonPreview:
            self.client_kwargs: dict[str, str] = {
                "model": args.model,
                "max_completion_tokens": 25000,
            }
        elif model.model_style == LMStyle.OpenAIReason:
            assert (
                "__" in args.model
            ), f"Model {args.model} is not a valid OpenAI Reasoning model as we require reasoning effort in model name."
            model_name, reasoning_effort = args.model.split("__")
            self.client_kwargs = {
                "model": model_name,
                "reasoning_effort": reasoning_effort,
            }
        else:
            self.client_kwargs = {
                "model": args.model,
                "temperature": args.temperature,
                "max_tokens": args.max_tokens,
                "top_p": args.top_p,
                "frequency_penalty": 0,
                "presence_penalty": 0,
                "n": args.n,
                "timeout": args.openai_timeout,
            }

            # For local ChatML/Qwen servers, explicit stop sequences prevent runaway
            # generation when the model emits follow-up turns.
            stop_env = os.getenv("LCB_STOP_SEQUENCES")
            stop_sequences = None
            if stop_env:
                try:
                    parsed = json.loads(stop_env)
                    if isinstance(parsed, list):
                        stop_sequences = [str(x) for x in parsed if str(x)]
                    elif isinstance(parsed, str):
                        stop_sequences = [parsed]
                except json.JSONDecodeError:
                    stop_sequences = [x for x in stop_env.split("|||") if x]
            elif args.model.startswith("Qwen3.5-"):
                stop_sequences = ["\n```", "<|im_end|>", "<|im_start|>", "<|endoftext|>"]

            if stop_sequences:
                self.client_kwargs["stop"] = stop_sequences

    def _run_single(self, prompt: list[dict[str, str]] | str, n: int = 10) -> list[str]:
        if isinstance(prompt, list):
            return self._run_chat(prompt, n)
        return self._run_completion(prompt, n)

    def _run_chat(self, prompt: list[dict[str, str]], n: int = 10) -> list[str]:
        if n == 0:
            print("Max retries reached. Returning empty response.")
            return []

        request_messages = prompt
        if self.args.model.startswith("Qwen3.5-"):
            request_messages = [dict(m) for m in prompt]
            no_think_hint = (
                " Do not output <think> tags. "
                "Return only the final answer/code."
            )
            if request_messages and request_messages[0].get("role") == "system":
                request_messages[0]["content"] = (
                    request_messages[0].get("content", "") + no_think_hint
                )
            else:
                request_messages = [
                    {
                        "role": "system",
                        "content": "Do not output <think> tags. Return only the final answer/code.",
                    }
                ] + request_messages

        try:
            response = self.client.chat.completions.create(
                messages=request_messages,
                **self.client_kwargs,
            )
        except (
            openai.APIError,
            openai.RateLimitError,
            openai.InternalServerError,
            openai.OpenAIError,
            openai.APIStatusError,
            openai.APITimeoutError,
            openai.InternalServerError,
            openai.APIConnectionError,
        ) as e:
            print("Exception: ", repr(e))
            print("Sleeping for 30 seconds...")
            print("Consider reducing the number of parallel processes.")
            sleep(30)
            return self._run_chat(prompt, n=n - 1)
        except Exception as e:
            print(f"Failed to run the model for {prompt}!")
            print("Exception: ", repr(e))
            raise e
        return [c.message.content for c in response.choices]

    def _run_completion(self, prompt: str, n: int = 10) -> list[str]:
        if n == 0:
            print("Max retries reached. Returning empty response.")
            return []

        try:
            response = self.client.completions.create(
                prompt=prompt,
                **self.client_kwargs,
            )
        except (
            openai.APIError,
            openai.RateLimitError,
            openai.InternalServerError,
            openai.OpenAIError,
            openai.APIStatusError,
            openai.APITimeoutError,
            openai.InternalServerError,
            openai.APIConnectionError,
        ) as e:
            print("Exception: ", repr(e))
            print("Sleeping for 30 seconds...")
            print("Consider reducing the number of parallel processes.")
            sleep(30)
            return self._run_completion(prompt, n=n - 1)
        except Exception as e:
            print(f"Failed to run the model for {prompt}!")
            print("Exception: ", repr(e))
            raise e
        return [c.text for c in response.choices]
