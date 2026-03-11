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

    @staticmethod
    def _is_truthy_env(name: str) -> bool:
        return os.getenv(name, "").strip().lower() in ("1", "true", "yes", "on")

    @staticmethod
    def _parse_json_env(name: str, default):
        raw = os.getenv(name, "").strip()
        if not raw:
            return default
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {name}: {e}") from e

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

            extra_body = {}

            # llama.cpp can expose reasoning and final answer in different channels.
            # This optional hint asks server to include reasoning in content channel.
            if self._is_truthy_env("LCB_REASONING_IN_CONTENT"):
                extra_body["reasoning_in_content"] = True

            reasoning_format = os.getenv("LCB_REASONING_FORMAT", "").strip()
            if reasoning_format:
                extra_body["reasoning_format"] = reasoning_format

            top_k_env = os.getenv("LCB_TOP_K", "").strip()
            if top_k_env:
                extra_body["top_k"] = int(top_k_env)

            min_p_env = os.getenv("LCB_MIN_P", "").strip()
            if min_p_env:
                extra_body["min_p"] = float(min_p_env)

            chat_template_kwargs = self._parse_json_env(
                "LCB_CHAT_TEMPLATE_KWARGS_JSON", {}
            )
            if chat_template_kwargs:
                if not isinstance(chat_template_kwargs, dict):
                    raise ValueError(
                        "LCB_CHAT_TEMPLATE_KWARGS_JSON must be a JSON object"
                    )
                extra_body["chat_template_kwargs"] = chat_template_kwargs

            merged_extra_body = self._parse_json_env("LCB_EXTRA_BODY_JSON", {})
            if merged_extra_body:
                if not isinstance(merged_extra_body, dict):
                    raise ValueError("LCB_EXTRA_BODY_JSON must be a JSON object")
                extra_body.update(merged_extra_body)

            if extra_body:
                self.client_kwargs["extra_body"] = extra_body

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

            if stop_sequences:
                self.client_kwargs["stop"] = stop_sequences

    @staticmethod
    def _normalize_message_text(value) -> str:
        if value is None:
            return ""
        if isinstance(value, str):
            return value
        if isinstance(value, list):
            parts = []
            for item in value:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict):
                    text = item.get("text")
                    if isinstance(text, str):
                        parts.append(text)
            return "".join(parts).strip()
        return str(value)

    @staticmethod
    def _extract_choice_text(choice) -> str:
        message = getattr(choice, "message", None)
        if message is None:
            return ""

        # Standard content channel first.
        content = OpenAIRunner._normalize_message_text(getattr(message, "content", ""))
        if content.strip():
            return content

        # Fallback to reasoning channel for servers that keep final/code there.
        reasoning = OpenAIRunner._normalize_message_text(
            getattr(message, "reasoning_content", "")
        )
        if reasoning.strip():
            return reasoning

        model_extra = getattr(message, "model_extra", None) or {}
        reasoning_extra = OpenAIRunner._normalize_message_text(
            model_extra.get("reasoning_content", "")
        )
        if reasoning_extra.strip():
            return reasoning_extra

        return ""

    def _run_single(self, prompt: list[dict[str, str]] | str, n: int = 10) -> list[str]:
        if isinstance(prompt, list):
            return self._run_chat(prompt, n)
        return self._run_completion(prompt, n)

    def _run_chat(self, prompt: list[dict[str, str]], n: int = 10) -> list[str]:
        if n == 0:
            print("Max retries reached. Returning empty response.")
            return []

        request_messages = prompt
        final_format_constraint = os.getenv("LCB_FINAL_ANSWER_CONSTRAINT", "").strip()
        if final_format_constraint:
            request_messages = [dict(m) for m in request_messages]
            if request_messages and request_messages[0].get("role") == "system":
                request_messages[0]["content"] = (
                    request_messages[0].get("content", "") + " " + final_format_constraint
                )
            else:
                request_messages = [
                    {"role": "system", "content": final_format_constraint}
                ] + request_messages

        if self.args.model.startswith("Qwen3.5-") and self._is_truthy_env(
            "LCB_QWEN_NO_THINK_HINT"
        ):
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
        return [self._extract_choice_text(c) for c in response.choices]

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
