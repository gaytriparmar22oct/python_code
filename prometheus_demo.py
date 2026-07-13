"""
prometheus_client — expose custom application metrics for Prometheus/Mimir.

Why SREs care: you don't just consume metrics, you INSTRUMENT services to emit
them. This library exposes a /metrics endpoint that Prometheus scrapes. Knowing
the four core metric types (Counter, Gauge, Histogram, Summary) is expected.

Install once:  pip install prometheus_client
Run:           python prometheus_demo.py
               then open http://localhost:8000/metrics in a browser.
"""

import random
import time


def main():
    try:
        from prometheus_client import (
            start_http_server, Counter, Gauge, Histogram,
        )
    except ImportError:
        print("prometheus_client not installed. Run: pip install prometheus_client")
        return

    # -----------------------------------------------------------------------
    # The core metric types:
    #
    #  Counter   - only goes UP (total requests, errors). Rate() it in PromQL.
    #  Gauge     - goes up AND down (in-flight requests, temperature, queue size).
    #  Histogram - buckets observations (request latency) -> percentiles.
    #  Summary   - like histogram but computes quantiles client-side.
    #
    # Labels (e.g. method, endpoint, status) let you slice one metric many ways.
    # -----------------------------------------------------------------------
    REQUESTS = Counter(
        "app_requests_total", "Total HTTP requests",
        ["method", "endpoint", "status"],
    )
    IN_FLIGHT = Gauge(
        "app_in_flight_requests", "Requests currently being served",
    )
    LATENCY = Histogram(
        "app_request_latency_seconds", "Request latency in seconds",
        ["endpoint"],
        buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5),
    )

    # Expose the metrics on http://localhost:8000/metrics
    start_http_server(8000)
    print("Serving metrics on http://localhost:8000/metrics  (Ctrl+C to stop)")

    endpoints = ["/health", "/api/pay", "/api/user"]
    methods = ["GET", "POST"]

    # Simulate traffic forever, updating the metrics as "requests" happen.
    while True:
        endpoint = random.choice(endpoints)
        method = random.choice(methods)

        IN_FLIGHT.inc()  # a request started
        # Time the "work" and record it into the histogram.
        with LATENCY.labels(endpoint=endpoint).time():
            time.sleep(random.uniform(0.005, 0.4))  # simulated processing

        # Mostly 200s, occasional 500.
        status = "500" if random.random() < 0.1 else "200"
        REQUESTS.labels(method=method, endpoint=endpoint, status=status).inc()
        IN_FLIGHT.dec()  # request finished

        # Print a heartbeat so you can see it working in the terminal.
        print(f"served {method} {endpoint} -> {status}")
        time.sleep(0.3)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")
