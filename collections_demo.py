"""
collections — specialized containers that make code shorter and faster.

Why SREs care: counting log levels, grouping items, bounded buffers of recent
events, and readable named records show up constantly in log/metric processing.

Run:  python collections_demo.py
"""

from collections import Counter, defaultdict, deque, namedtuple

# ---------------------------------------------------------------------------
# 1. Counter — tally occurrences in one line (e.g. HTTP status codes in logs).
# ---------------------------------------------------------------------------
status_codes = [200, 200, 500, 404, 200, 500, 502, 200, 404]
counts = Counter(status_codes)
print("Counts:", counts)
print("Most common 2:", counts.most_common(2))   # [(200, 4), (500, 2)]
print("How many 500s:", counts[500])

# ---------------------------------------------------------------------------
# 2. defaultdict — grouping without checking "does the key exist yet?".
# ---------------------------------------------------------------------------
logs = [
    ("auth", "ERROR"),
    ("auth", "INFO"),
    ("payments", "ERROR"),
    ("payments", "ERROR"),
]
by_service = defaultdict(list)
for service, level in logs:
    by_service[service].append(level)   # no KeyError on first insert
print("\nGrouped:", dict(by_service))

# ---------------------------------------------------------------------------
# 3. deque — a fast double-ended queue; maxlen keeps only the N most recent
#    items (perfect for a rolling window of recent events/metrics).
# ---------------------------------------------------------------------------
recent = deque(maxlen=3)
for latency in [100, 120, 95, 210, 180]:
    recent.append(latency)              # oldest auto-drops when full
print("\nLast 3 latencies:", list(recent))   # [95, 210, 180]

# ---------------------------------------------------------------------------
# 4. namedtuple — a lightweight, immutable record with named fields
#    (more readable than tuple[0], tuple[1] ...).
# ---------------------------------------------------------------------------
Node = namedtuple("Node", ["name", "cpu", "ready"])
n = Node(name="worker-1", cpu=0.75, ready=True)
print("\nNode:", n.name, "cpu=", n.cpu, "ready=", n.ready)
