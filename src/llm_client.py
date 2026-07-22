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

import groq

# Good default: fast + capable enough for Lean tactic synthesis, and cheap
# to iterate with during development. Swap to a bigger model (e.g.
# "llama-3.3-70b-versatile" -> "deepseek-r1-distill-llama-70b" or whatever
# Groq's current top reasoning model is) once you're past the prototyping
# stage and want higher first-attempt pass rates. Check
# https://console.groq.com/docs/models for the current lineup -- Groq adds
# and deprecates models often.
MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

_client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY"))


def complete(prompt: str, max_tokens: int = 2000, temperature: float = 0.2, retries: int = 3) -> str:
    """Send a single-turn prompt, return the raw text response."""
    last_err = None
    for attempt in range(retries):
        try:
            resp = _client.chat.completions.create(
                model=MODEL,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.choices[0].message.content or ""
        except groq.RateLimitError as e:
            last_err = e
            time.sleep(2 ** attempt)
        except groq.APIStatusError as e:
            last_err = e
            time.sleep(1)
    raise RuntimeError(f"LLM call failed after {retries} retries: {last_err}")


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
