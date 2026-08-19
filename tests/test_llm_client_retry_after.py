"""Regression test for src/llm_client._parse_retry_after.

Background: llm_client.complete() catches groq.RateLimitError and tries to
sleep for exactly the duration Groq's error message says to wait, instead of
a short fixed backoff -- this matters most for daily-quota (TPD) errors,
which is the whole reason this parsing exists (see commit 98715d7, "Split
LLM calls across strong/fast Groq models to spread daily token quota").

Real Groq TPD error messages format multi-minute waits with a SPACE between
the minutes and seconds components, e.g.:

    "... on tokens per day (TPD): Limit 200,000 / Used 199,336 / Requested
    1,524. Please try again in 6m 11.52s."

The original regex `r"try again in (?:(\\d+)m)?([\\d.]+)s"` required the
minutes and seconds parts to be directly adjacent (no space), so it failed
to match this real-world format and returned None -- causing complete() to
fall back to a trivial few-second backoff instead of waiting out the actual
quota reset, exhausting its retries and raising RuntimeError. That's the
exact crash this feature exists to prevent.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / "src"

os.environ.setdefault("GROQ_API_KEY", "test-dummy-key")

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from llm_client import _parse_retry_after  # noqa: E402


def test_parses_plain_seconds():
    assert _parse_retry_after("Please try again in 5.289s.") == 5.289


def test_parses_minutes_and_seconds_with_no_space():
    assert _parse_retry_after("Please try again in 2m30.5s") == 2 * 60 + 30.5


def test_parses_real_groq_daily_quota_format_with_space():
    # Real message text from a Groq TPD (tokens-per-day) 429 response.
    msg = (
        "Rate limit reached for model openai/gpt-oss-20b in organization "
        "org_01 service tier on_demand on tokens per day (TPD): Limit "
        "200,000, Used 199,336, Requested 1,524. Please try again in "
        "6m 11.52s. Need more tokens? Upgrade to Dev Tier today at "
        "https://console.groq.com/settings/billing"
    )
    assert _parse_retry_after(msg) == 6 * 60 + 11.52


def test_returns_none_when_no_wait_time_present():
    assert _parse_retry_after("Some unrelated error message.") is None


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
