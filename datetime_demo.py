"""
datetime — work with dates, times, durations, and timezones.

Why SREs care: incident timelines, "how long has this pod been running?",
retry backoff windows, log timestamp parsing, and SLA math all need this.
Golden rule: always work in UTC for servers/logs.

Run:  python datetime_demo.py
"""

from datetime import datetime, timedelta, timezone

# ---------------------------------------------------------------------------
# 1. "Now" — always prefer timezone-aware UTC over naive local time.
# ---------------------------------------------------------------------------
now_utc = datetime.now(timezone.utc)
print("UTC now:", now_utc.isoformat())

# ---------------------------------------------------------------------------
# 2. Durations with timedelta — the answer to "how long ago / until?".
# ---------------------------------------------------------------------------
deployed_at = now_utc - timedelta(hours=26, minutes=15)
uptime = now_utc - deployed_at
print("\nDeployed at:", deployed_at.isoformat())
print("Uptime:", uptime)                       # e.g. 1 day, 2:15:00
print("Uptime (total seconds):", uptime.total_seconds())
print("Uptime (hours):", round(uptime.total_seconds() / 3600, 1))

# ---------------------------------------------------------------------------
# 3. Parsing a timestamp string from a log line (strptime = string-parse-time).
# ---------------------------------------------------------------------------
log_line_ts = "2026-07-13 14:30:05"
parsed = datetime.strptime(log_line_ts, "%Y-%m-%d %H:%M:%S")
print("\nParsed log timestamp:", parsed)

# ---------------------------------------------------------------------------
# 4. Formatting for output (strftime = string-format-time).
# ---------------------------------------------------------------------------
print("Formatted:", now_utc.strftime("%d %b %Y, %H:%M UTC"))

# ---------------------------------------------------------------------------
# 5. Unix epoch conversion — many APIs/metrics use epoch seconds.
# ---------------------------------------------------------------------------
epoch = now_utc.timestamp()
print("\nEpoch seconds:", int(epoch))
print("Back to datetime:", datetime.fromtimestamp(epoch, timezone.utc).isoformat())

# ---------------------------------------------------------------------------
# 6. SLA check example: is this incident older than our 4-hour resolution SLA?
# ---------------------------------------------------------------------------
incident_start = now_utc - timedelta(hours=5)
sla = timedelta(hours=4)
breached = (now_utc - incident_start) > sla
print("\nIncident SLA breached?", breached)
