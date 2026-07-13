"""
json — serialize/deserialize data (the bread-and-butter of SRE work).

Why SREs care: almost everything speaks JSON — Kubernetes API responses,
Prometheus/Alertmanager payloads, cloud CLIs (`aws ... --output json`),
structured logs, and REST APIs. Being fluent with this module is expected.

Run:  python json_demo.py
"""

import json

# ---------------------------------------------------------------------------
# 1. Python object  ->  JSON string  (serialize / "dumps" = dump-string)
# ---------------------------------------------------------------------------
service = {
    "name": "payments",
    "replicas": 3,
    "healthy": True,
    "endpoints": ["/health", "/metrics"],
    "owner": None,  # None becomes JSON null
}

# indent= pretty-prints; sort_keys= makes output deterministic (good for diffs).
pretty = json.dumps(service, indent=2, sort_keys=True)
print("--- JSON string ---")
print(pretty)

# ---------------------------------------------------------------------------
# 2. JSON string  ->  Python object  (deserialize / "loads" = load-string)
# ---------------------------------------------------------------------------
raw = '{"cpu": "250m", "memory": "512Mi", "burstable": false}'
parsed = json.loads(raw)
print("\n--- parsed back to Python ---")
print(type(parsed), parsed)
print("memory limit:", parsed["memory"])  # dict access

# ---------------------------------------------------------------------------
# 3. Files: dump() writes to a file object, load() reads from one.
#    (dumps/loads work on strings; dump/load work on file handles.)
# ---------------------------------------------------------------------------
with open("service.json", "w") as f:
    json.dump(service, f, indent=2)

with open("service.json") as f:
    from_file = json.load(f)
print("\n--- round-tripped through a file ---")
print(from_file["endpoints"])

# ---------------------------------------------------------------------------
# 4. Real-world touch: safely handle bad JSON (never let a parser crash a tool)
# ---------------------------------------------------------------------------
bad = '{"broken": true,,}'
try:
    json.loads(bad)
except json.JSONDecodeError as e:
    print("\n--- handled invalid JSON gracefully ---")
    print(f"Could not parse: {e}")
