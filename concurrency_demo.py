"""
concurrent.futures — run many I/O tasks in parallel (huge speedup for SRE work).

Why SREs care: health-checking 100 endpoints or hitting many APIs one-by-one is
slow. A ThreadPoolExecutor runs them concurrently — ideal for I/O-bound work
(network calls, disk). For CPU-bound work you'd use ProcessPoolExecutor instead.

Run:  python concurrency_demo.py
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def health_check(service: str) -> tuple[str, str]:
    """Pretend to call a service's /health endpoint (simulated latency)."""
    time.sleep(0.5)  # stand-in for a network round-trip
    # Fake a couple of unhealthy services for the demo.
    healthy = service not in {"payments", "search"}
    return service, "UP" if healthy else "DOWN"


services = ["auth", "payments", "orders", "search", "inventory", "shipping"]

# ---------------------------------------------------------------------------
# 1. Sequential (the slow way) — 6 services x 0.5s = ~3s.
# ---------------------------------------------------------------------------
start = time.perf_counter()
for s in services:
    health_check(s)
print(f"Sequential took {time.perf_counter() - start:.2f}s")

# ---------------------------------------------------------------------------
# 2. Parallel with a thread pool — all run at once, ~0.5s total.
#    map() keeps input order; as_completed() yields results as they finish.
# ---------------------------------------------------------------------------
start = time.perf_counter()
results = {}
with ThreadPoolExecutor(max_workers=8) as pool:
    # Submit all jobs, then collect them as each completes.
    futures = {pool.submit(health_check, s): s for s in services}
    for future in as_completed(futures):
        service, status = future.result()
        results[service] = status

print(f"Parallel took {time.perf_counter() - start:.2f}s")

# ---------------------------------------------------------------------------
# 3. Act on the results — report anything DOWN.
# ---------------------------------------------------------------------------
down = [s for s, status in results.items() if status == "DOWN"]
print("\nAll results:", results)
print("Unhealthy services:", down or "none")
