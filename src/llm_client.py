"""Thin wrapper around the Groq API used by every pipeline stage.

Keeping this in one place means swapping models, adding retries-on-rate-limit,
or logging token usage only needs to happen once.

Groq's API is OpenAI-compatible (chat completions), which is a different
request/response shape than Anthropic's messages API -- notably:
  - messages still use {"role": ..., "content": ...} but content is a plain
    string, not a list of content blocks
  - the response text lives at resp.choices[0].message.content, not
    resp.content[i].text
  - rate limit / server errors are groq.RateLimitError / groq.APIStatusError,
    mirroring the openai-python exception names
"""
from __future__ import annotations

import json
import os
import re
import time
from collections.abc import Callable
from dataclasses import dataclass

import groq

# Two-tier model setup: reasoning-heavy stages (formalizing NL -> Lean,
# sketching the proof strategy) need the strong model to get well-typed
# output; the repair loop (Stage C/D) is higher-volume and more mechanical,
# so it runs on a separate model with its own daily token quota. Splitting
# this way roughly doubles usable daily budget on Groq's free/on-demand tier
# since TPD limits are tracked per-model.
STRONG_MODEL = (
    os.environ.get("GROQ_MODEL_STRONG")
    or os.environ.get("GROQ_MODEL")
    or "llama-3.3-70b-versatile"
)
FAST_MODEL = os.environ.get("GROQ_MODEL_FAST", "llama-3.1-8b-instant")

# Back-compat: if something still imports MODEL directly, keep it pointing
# at the strong model.
MODEL = STRONG_MODEL

_client: groq.Groq | None = None


class MissingGroqApiKeyError(RuntimeError):
    """Raised when an API-backed completion is requested without credentials."""


def _get_client() -> groq.Groq:
    global _client
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise MissingGroqApiKeyError(
            "GROQ_API_KEY is not set. Configure it in the environment before "
            "running an API-backed completion."
        )
    if _client is None:
        _client = groq.Groq(api_key=api_key)
    return _client

# Matches Groq's rate-limit error body, e.g.:
#   "Please try again in 13m17.472s."
#   "Please try again in 8m41.856s."
#   "Please try again in 45.2s." (no minutes)
_RETRY_AFTER_RE = re.compile(r"try again in (?:(\d+)m\s*)?([\d.]+)s")


@dataclass(frozen=True)
class CompletionResult:
    content: str
    metadata: dict[str, object]


def reasoning_effort_for_model(model: str) -> str | None:
    """Limit GPT-OSS reasoning overhead for code-oriented synthesis calls."""
    if model in {"openai/gpt-oss-20b", "openai/gpt-oss-120b"}:
        return "low"
    return None


def _optional_int(value: object) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int):
        return None
    return value


def _optional_text(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _response_metadata(resp: object, model: str, content: str) -> dict[str, object]:
    """Return safe scalar completion diagnostics; never include response text.

    Absent optional provider fields are ``None`` (unavailable), never zero.
    """
    choices = getattr(resp, "choices", None) or []
    choice = choices[0] if choices else None
    message = getattr(choice, "message", None)
    usage = getattr(resp, "usage", None)
    reasoning_value = None
    reasoning_field = None
    for field in ("reasoning", "reasoning_content"):
        value = getattr(message, field, None)
        if value is not None:
            reasoning_field = field
            reasoning_value = value
            break
    try:
        reasoning_length = len(reasoning_value) if reasoning_value is not None else 0
    except TypeError:
        reasoning_length = None
    tool_calls = getattr(message, "tool_calls", None)
    return {
        "provider": "groq",
        "model": model,
        "finish_reason": getattr(choice, "finish_reason", None),
        "completion_tokens": getattr(usage, "completion_tokens", None),
        "prompt_tokens": _optional_int(getattr(usage, "prompt_tokens", None)),
        "total_tokens": _optional_int(getattr(usage, "total_tokens", None)),
        "response_model": _optional_text(getattr(resp, "model", None)),
        "system_fingerprint": _optional_text(
            getattr(resp, "system_fingerprint", None)
        ),
        "content_empty": not content.strip(),
        "refusal_present": getattr(message, "refusal", None) is not None,
        "reasoning_present": reasoning_field is not None,
        "reasoning_field": reasoning_field,
        "reasoning_length": reasoning_length,
        "tool_calls_present": bool(tool_calls),
    }


def complete_with_metadata(
    prompt: str,
    max_tokens: int = 2000,
    temperature: float = 0.2,
    retries: int = 3,
    model: str | None = None,
    max_retry_after_seconds: float = 300,
    max_total_wait_seconds: float = 600,
    sleep: Callable[[float], None] | None = None,
    reasoning_effort: str | None = None,
) -> CompletionResult:
    """Send a chat completion and return text with safe scalar diagnostics."""
    if retries < 1:
        raise ValueError("retries must be at least 1")
    if max_retry_after_seconds < 0 or max_total_wait_seconds < 0:
        raise ValueError("retry wait budgets must be non-negative")

    model = model or STRONG_MODEL
    client = _get_client()
    sleep = sleep or time.sleep
    total_wait_seconds = 0.0
    last_err: Exception | None = None
    retry_events: list[dict[str, object]] = []

    def record_retry(attempt: int, error: Exception, delay: float) -> None:
        retry_events.append(
            {
                "api_attempt": attempt + 1,
                "error_type": type(error).__name__,
                "status_code": _optional_int(getattr(error, "status_code", None)),
                "delay_seconds": delay,
            }
        )

    for attempt in range(retries):
        try:
            request: dict[str, object] = {
                "model": model,
                "max_completion_tokens": max_tokens,
                "temperature": temperature,
                "messages": [{"role": "user", "content": prompt}],
            }
            if reasoning_effort is not None:
                request["reasoning_effort"] = reasoning_effort
            request_started = time.monotonic()
            resp = client.chat.completions.create(**request)
            latency_seconds = round(time.monotonic() - request_started, 3)
            choices = getattr(resp, "choices", None) or []
            message = getattr(choices[0], "message", None) if choices else None
            raw_content = getattr(message, "content", None)
            content = raw_content if isinstance(raw_content, str) else ""
            metadata = _response_metadata(resp, model, content)
            metadata.update(
                {
                    "max_completion_tokens": max_tokens,
                    "temperature": temperature,
                    "reasoning_effort": reasoning_effort,
                    "latency_seconds": latency_seconds,
                    "api_attempts": attempt + 1,
                    "retry_events": retry_events,
                }
            )
            if metadata["content_empty"]:
                print(
                    "[llm_client] empty_response "
                    + json.dumps(metadata, sort_keys=True)
                )
            return CompletionResult(content=content, metadata=metadata)
        except groq.RateLimitError as e:
            last_err = e
            wait_s = _parse_retry_after(str(e))
            if wait_s is not None:
                if wait_s > max_retry_after_seconds:
                    raise RuntimeError(
                        f"Groq requested a {wait_s:.0f}s retry delay, exceeding "
                        f"the {max_retry_after_seconds:.0f}s per-retry budget."
                    ) from e
                delay = wait_s
            else:
                delay = float(2 ** attempt)

            if attempt == retries - 1:
                break
            if total_wait_seconds + delay > max_total_wait_seconds:
                raise RuntimeError(
                    f"Retry wait budget of {max_total_wait_seconds:.0f}s would be "
                    "exceeded."
                ) from e
            total_wait_seconds += delay
            record_retry(attempt, e, delay)
            print(
                f"[llm_client] rate limit hit on {model}, "
                f"sleeping {delay:.0f}s before retry {attempt + 2}/{retries}..."
            )
            sleep(delay)
        except groq.APIStatusError as e:
            last_err = e
            if attempt == retries - 1:
                break
            if total_wait_seconds + 1 > max_total_wait_seconds:
                raise RuntimeError(
                    f"Retry wait budget of {max_total_wait_seconds:.0f}s would be "
                    "exceeded."
                ) from e
            total_wait_seconds += 1
            record_retry(attempt, e, 1)
            sleep(1)
    raise RuntimeError(
        f"LLM call failed after {retries} attempts and {total_wait_seconds:.0f}s "
        f"of retry waiting: {last_err}"
    ) from last_err


def _parse_retry_after(msg: str) -> float | None:
    """Extract the wait time Groq tells us to use, in seconds. Returns None
    if the message doesn't contain a parseable wait time (e.g. some other
    kind of 429, or a transient server-side rate limit rather than the
    daily token cap)."""
    m = _RETRY_AFTER_RE.search(msg)
    if not m:
        return None
    minutes = int(m.group(1)) if m.group(1) else 0
    seconds = float(m.group(2))
    return minutes * 60 + seconds


def complete(
    prompt: str,
    max_tokens: int = 2000,
    temperature: float = 0.2,
    retries: int = 3,
    model: str | None = None,
    max_retry_after_seconds: float = 300,
    max_total_wait_seconds: float = 600,
    sleep: Callable[[float], None] | None = None,
) -> str:
    """Send a single-turn prompt, return the raw text response.

    model defaults to STRONG_MODEL; pass FAST_MODEL explicitly for
    high-volume, lower-stakes calls (e.g. the repair loop) to spread load
    across Groq's per-model daily quota. ``retries`` is the total number of
    API attempts, including the initial request, matching the prior
    ``range(retries)`` behavior.
    """
    return complete_with_metadata(
        prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        retries=retries,
        model=model,
        max_retry_after_seconds=max_retry_after_seconds,
        max_total_wait_seconds=max_total_wait_seconds,
        sleep=sleep,
    ).content


_LEAN_BLOCK_RE = re.compile(r"```lean\s*(.*?)```", re.DOTALL)


def extract_lean_block(text: str) -> str:
    """Pull the code out of a ```lean ... ``` fenced block. Falls back to the
    raw text (stripped) if the model forgot to fence it -- this happens more
    often than you'd hope, so don't assume compliance. Groq's smaller/faster
    models in particular are more likely to add a stray sentence before or
    after the block than Claude tends to -- worth keeping an eye on this in
    data/results/attempts/*.jsonl if pass@1 looks lower than expected; a
    parsing miss looks identical to a real proof failure unless you check."""
    match = _LEAN_BLOCK_RE.search(text)
    if match:
        return match.group(1).strip()
    return text.strip()