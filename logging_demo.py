"""
logging — proper application logging (never use print() in real tools).

Why SREs care: logs are how you debug production. Interviewers want to see you
use levels (DEBUG/INFO/WARNING/ERROR), structured output, and NOT print().
Bonus: JSON logs feed straight into Loki/ELK/CloudWatch.

Run:  python logging_demo.py
"""

import logging
import json

# ---------------------------------------------------------------------------
# 1. Basic config: set the minimum level and a format. Anything below the
#    level is dropped (here DEBUG shows because we set level=DEBUG).
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s | %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

# Use a named logger per module (never the root logger in real code).
log = logging.getLogger("payments")

# ---------------------------------------------------------------------------
# 2. The five levels, in increasing severity.
# ---------------------------------------------------------------------------
log.debug("Connecting to database...")        # dev detail
log.info("Service started on port 8080")       # normal operation
log.warning("Cache miss rate is high (40%)")    # something to watch
log.error("Failed to reach downstream API")     # a real problem
log.critical("Out of memory, shutting down")    # the sky is falling

# ---------------------------------------------------------------------------
# 3. Log exceptions WITH the traceback (exc_info=True or log.exception).
# ---------------------------------------------------------------------------
try:
    1 / 0
except ZeroDivisionError:
    log.exception("Unexpected error while computing ratio")

# ---------------------------------------------------------------------------
# 4. Structured (JSON) logging — one line per event, machine-parseable.
#    This is what you ship to Loki/CloudWatch for querying by field.
# ---------------------------------------------------------------------------
class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        })

json_log = logging.getLogger("json-demo")
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
json_log.addHandler(handler)
json_log.setLevel(logging.INFO)
json_log.propagate = False  # don't also print via the root logger

print("\n--- structured JSON logs ---")
json_log.info("request handled")
json_log.warning("high latency detected")
