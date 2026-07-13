"""
pandas — tabular data analysis (DataFrames).

Why SREs care: pandas is the fastest way to crunch CSV/JSON exports —
analyzing latency percentiles, parsing billing reports, summarizing metrics,
or turning a messy export into a clean answer during an incident review.

Install once:  pip install pandas
Run:           python pandas_demo.py
"""

import pandas as pd

# ---------------------------------------------------------------------------
# 1. A DataFrame = a table (rows + named columns). Build one from a dict.
#    Imagine this came from `kubectl get pods` or a metrics export.
# ---------------------------------------------------------------------------
data = {
    "service": ["auth", "auth", "payments", "payments", "search"],
    "region": ["eu", "us", "eu", "us", "eu"],
    "latency_ms": [120, 180, 95, 210, 340],
    "errors": [0, 2, 1, 5, 0],
}
df = pd.DataFrame(data)
print("--- full table ---")
print(df)

# ---------------------------------------------------------------------------
# 2. Inspect — the first things you run on any unfamiliar dataset.
# ---------------------------------------------------------------------------
print("\n--- shape (rows, cols) ---", df.shape)
print("\n--- summary stats ---")
print(df.describe())          # count/mean/std/min/max for numeric columns

# ---------------------------------------------------------------------------
# 3. Filter (boolean indexing) — "show me the SLO breaches".
# ---------------------------------------------------------------------------
slow = df[df["latency_ms"] > 150]
print("\n--- requests slower than 150ms ---")
print(slow)

# ---------------------------------------------------------------------------
# 4. Group + aggregate — the real power move for reporting.
#    "Average latency and total errors per service."
# ---------------------------------------------------------------------------
summary = df.groupby("service").agg(
    avg_latency=("latency_ms", "mean"),
    total_errors=("errors", "sum"),
).sort_values("avg_latency", ascending=False)
print("\n--- per-service summary ---")
print(summary)

# ---------------------------------------------------------------------------
# 5. Derived columns + I/O — add an SLO flag and save the result.
# ---------------------------------------------------------------------------
df["slo_breach"] = df["latency_ms"] > 200
df.to_csv("latency_report.csv", index=False)
print("\nSaved latency_report.csv")
print(df)
