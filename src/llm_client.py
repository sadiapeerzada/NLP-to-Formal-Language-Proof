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

import os
import re
import time
from collections.abc import Callable

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

_client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Matches Groq's rate-limit error body, e.g.:
#   "Please try again in 13m17.472s."
#   "Please try again in 8m41.856s."
#   "Please try again in 45.2s." (no minutes)
_RETRY_AFTER_RE = re.compile(r"try again in (?:(\d+)m\s*)?([\d.]+)s")


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
    if retries < 1:
        raise ValueError("retries must be at least 1")
    if max_retry_after_seconds < 0 or max_total_wait_seconds < 0:
        raise ValueError("retry wait budgets must be non-negative")

    model = model or STRONG_MODEL
    sleep = sleep or time.sleep
    total_wait_seconds = 0.0
    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            resp = _client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.choices[0].message.content or ""
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
            sleep(1)
    raise RuntimeError(
        f"LLM call failed after {retries} attempts and {total_wait_seconds:.0f}s "
        f"of retry waiting: {last_err}"
    ) from last_err


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