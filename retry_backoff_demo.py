"""
Retry with exponential backoff — resilient calls to flaky dependencies.

Why SREs care: networks and downstream services fail transiently. Blindly
retrying hammers a struggling service (retry storm); the fix is exponential
backoff + jitter + a cap on attempts. This is a VERY common interview question.

Two versions are shown:
  1. A hand-rolled decorator (understand the mechanics).
  2. The `tenacity` library (what you'd use in production) — optional.

Run:  python retry_backoff_demo.py
"""

import random
import time
import functools


# ---------------------------------------------------------------------------
# 1. Hand-rolled retry decorator with exponential backoff + jitter.
# ---------------------------------------------------------------------------
def retry(max_attempts=5, base_delay=0.2, max_delay=5.0, exceptions=(Exception,)):
    """
    Retry the wrapped function on `exceptions`.

    Delay grows exponentially: base * 2**(attempt-1), capped at max_delay.
    Random "jitter" spreads retries out so many clients don't retry in lockstep
    (which would create a synchronized thundering herd on the recovering service).
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt >= max_attempts:
                        # Out of retries — re-raise so the caller sees the failure.
                        print(f"  giving up after {attempt} attempts: {e}")
                        raise
                    # exponential backoff, capped
                    delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                    # full jitter: sleep a random amount in [0, delay]
                    sleep_for = random.uniform(0, delay)
                    print(f"  attempt {attempt} failed ({e}); "
                          f"retrying in {sleep_for:.2f}s")
                    time.sleep(sleep_for)
                    attempt += 1
        return wrapper
    return decorator


# A fake dependency that fails a few times, then succeeds.
_calls = {"n": 0}


@retry(max_attempts=6, base_delay=0.1, exceptions=(ConnectionError,))
def flaky_api_call():
    _calls["n"] += 1
    if _calls["n"] < 4:
        raise ConnectionError(f"connection reset (call #{_calls['n']})")
    return "200 OK"


print("--- hand-rolled retry ---")
result = flaky_api_call()
print("Succeeded with:", result, "after", _calls["n"], "calls")


# ---------------------------------------------------------------------------
# 2. Production version with `tenacity` (pip install tenacity). Optional.
#    Same idea, but battle-tested: stop conditions, wait strategies, logging.
# ---------------------------------------------------------------------------
print("\n--- tenacity (if installed) ---")
try:
    from tenacity import (
        retry as t_retry,
        stop_after_attempt,
        wait_exponential,
        retry_if_exception_type,
    )

    _t_calls = {"n": 0}

    @t_retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=0.1, max=2),
        retry=retry_if_exception_type(TimeoutError),
        reraise=True,
    )
    def flaky_with_tenacity():
        _t_calls["n"] += 1
        if _t_calls["n"] < 3:
            raise TimeoutError(f"timed out (call #{_t_calls['n']})")
        return "done"

    print("tenacity result:", flaky_with_tenacity(), "after", _t_calls["n"], "calls")
except ImportError:
    print("tenacity not installed — run `pip install tenacity` to try it.")
