"""
PyYAML — read/write YAML, the config language of Kubernetes, CI, Ansible, etc.

Why SREs care: almost all infra config is YAML (k8s manifests, GitHub Actions,
Helm values, docker-compose). Programmatically reading/editing YAML lets you
validate, template, and patch configs safely.

Install once:  pip install pyyaml
Run:           python yaml_demo.py
"""

import yaml

# ---------------------------------------------------------------------------
# 1. Parse YAML string -> Python objects (safe_load avoids executing tags).
#    ALWAYS use safe_load on untrusted input, never yaml.load without a Loader.
# ---------------------------------------------------------------------------
manifest_text = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payments
  labels:
    team: platform
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: app
          image: payments:1.2.0
          resources:
            requests:
              cpu: 250m
              memory: 256Mi
"""

manifest = yaml.safe_load(manifest_text)
print("kind:", manifest["kind"])
print("name:", manifest["metadata"]["name"])
print("replicas:", manifest["spec"]["replicas"])
print("image:", manifest["spec"]["template"]["spec"]["containers"][0]["image"])

# ---------------------------------------------------------------------------
# 2. Modify the object in memory — e.g. bump replicas and the image tag.
# ---------------------------------------------------------------------------
manifest["spec"]["replicas"] = 5
manifest["spec"]["template"]["spec"]["containers"][0]["image"] = "payments:1.3.0"

# ---------------------------------------------------------------------------
# 3. Dump back to YAML (sort_keys=False keeps your field order readable).
# ---------------------------------------------------------------------------
patched = yaml.safe_dump(manifest, sort_keys=False, default_flow_style=False)
print("\n--- patched manifest ---")
print(patched)

# ---------------------------------------------------------------------------
# 4. Multi-document YAML (files with several manifests separated by '---').
# ---------------------------------------------------------------------------
multi = """
kind: Service
metadata: {name: payments}
---
kind: Deployment
metadata: {name: payments}
"""
docs = list(yaml.safe_load_all(multi))
print("Documents in file:", [d["kind"] for d in docs])

# ---------------------------------------------------------------------------
# 5. Write to / read from a file.
# ---------------------------------------------------------------------------
with open("deployment.yaml", "w") as f:
    yaml.safe_dump(manifest, f, sort_keys=False)
with open("deployment.yaml") as f:
    reloaded = yaml.safe_load(f)
print("\nReloaded replicas from file:", reloaded["spec"]["replicas"])
