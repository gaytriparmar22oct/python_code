"""
os — interact with the operating system (files, paths, env vars, processes).

Why SREs care: automation scripts constantly read environment variables,
build file paths safely across OSes, walk directories, and shell out to other
commands. This is core scripting glue.

Run:  python os_demo.py
"""

import os

# ---------------------------------------------------------------------------
# 1. Environment variables — how config/secrets reach a process at runtime.
# ---------------------------------------------------------------------------
# os.getenv returns None (or a default) if the var is missing — never crashes.
region = os.getenv("AWS_REGION", "eu-west-1")
print("Region:", region)

# Set one for the current process (children inherit it).
os.environ["APP_ENV"] = "dev"
print("APP_ENV:", os.environ["APP_ENV"])

# ---------------------------------------------------------------------------
# 2. Paths — always build paths with os.path (or pathlib) for portability.
# ---------------------------------------------------------------------------
cwd = os.getcwd()
print("\nCurrent dir:", cwd)

# os.path.join uses the right separator for the OS (\ on Windows, / on Linux).
log_path = os.path.join(cwd, "logs", "app.log")
print("Joined path:", log_path)
print("Base name:", os.path.basename(log_path))   # app.log
print("Dir name :", os.path.dirname(log_path))    # .../logs
print("Exists?  :", os.path.exists(log_path))

# ---------------------------------------------------------------------------
# 3. Directories — create, list, and walk a tree.
# ---------------------------------------------------------------------------
demo_dir = os.path.join(cwd, "os_demo_tmp")
os.makedirs(demo_dir, exist_ok=True)  # exist_ok avoids errors on re-run
with open(os.path.join(demo_dir, "note.txt"), "w") as f:
    f.write("hello")

print("\nContents of cwd (first 5):", os.listdir(cwd)[:5])

# os.walk yields (dirpath, dirnames, filenames) for every folder in the tree.
print("\nWalking os_demo_tmp:")
for dirpath, dirnames, filenames in os.walk(demo_dir):
    print(" ", dirpath, "->", filenames)

# ---------------------------------------------------------------------------
# 4. Running another command (useful, but prefer subprocess for real work).
# ---------------------------------------------------------------------------
# os.system returns the exit code; 0 means success.
exit_code = os.system("echo ran a shell command")
print("\nShell exit code:", exit_code)

# Clean up what we created.
os.remove(os.path.join(demo_dir, "note.txt"))
os.rmdir(demo_dir)
print("Cleaned up temp dir.")
