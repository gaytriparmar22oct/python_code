"""
subprocess — run external commands the RIGHT way (replaces os.system).

Why SREs care: automation constantly shells out to kubectl, aws, git, curl,
etc. subprocess gives you the exit code, stdout, stderr, timeouts, and safe
argument passing — everything os.system can't do.

Run:  python subprocess_demo.py
"""

import subprocess

# ---------------------------------------------------------------------------
# 1. run() is the modern entry point. Pass args as a LIST (not a string) to
#    avoid shell-injection and quoting bugs.
# ---------------------------------------------------------------------------
result = subprocess.run(
    ["python", "--version"],
    capture_output=True,  # grab stdout + stderr instead of printing directly
    text=True,            # decode bytes -> str automatically
)
print("returncode:", result.returncode)   # 0 == success
print("stdout    :", result.stdout.strip())
print("stderr    :", result.stderr.strip())

# ---------------------------------------------------------------------------
# 2. check=True raises CalledProcessError on a non-zero exit — fail loudly.
# ---------------------------------------------------------------------------
try:
    subprocess.run(["python", "-c", "import sys; sys.exit(3)"], check=True)
except subprocess.CalledProcessError as e:
    print("\nCommand failed as expected, exit code:", e.returncode)

# ---------------------------------------------------------------------------
# 3. Timeouts stop a hung command from freezing your automation forever.
# ---------------------------------------------------------------------------
try:
    subprocess.run(
        ["python", "-c", "import time; time.sleep(5)"],
        timeout=1,
    )
except subprocess.TimeoutExpired:
    print("\nKilled the command after 1s timeout (good — no hangs).")

# ---------------------------------------------------------------------------
# 4. Capture output and act on it — the core automation loop.
# ---------------------------------------------------------------------------
out = subprocess.run(
    ["python", "-c", "print('healthy')"],
    capture_output=True, text=True,
).stdout.strip()

if out == "healthy":
    print("\nService reports:", out)
