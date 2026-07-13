"""
kubernetes — the official Python client for the Kubernetes API.

Why SREs care: automating cluster operations (list pods, read logs, scale
deployments, react to events) without shelling out to kubectl. This is how you
build controllers, health-check bots, and remediation scripts.

Install once:  pip install kubernetes
Run:           python kubernetes_demo.py   (needs a reachable cluster + kubeconfig)

NOTE: this talks to a real cluster. It is READ-ONLY here (safe). It will simply
print a friendly message if no cluster/kubeconfig is available.
"""

from kubernetes import client, config


def load_kube_config():
    """
    Two ways to authenticate:
      * in-cluster   -> when running INSIDE a pod (uses the pod's service account)
      * kubeconfig   -> when running on your laptop (~/.kube/config)
    Try in-cluster first, fall back to local kubeconfig.
    """
    try:
        config.load_incluster_config()
        print("Loaded in-cluster config (running inside a pod).")
    except config.ConfigException:
        config.load_kube_config()
        print("Loaded local kubeconfig (~/.kube/config).")


def main():
    try:
        load_kube_config()
    except Exception as e:
        print(f"No cluster available, skipping live calls: {e}")
        return

    # CoreV1Api covers pods, services, nodes, namespaces, configmaps, secrets...
    core = client.CoreV1Api()

    # 1. List pods across all namespaces (like `kubectl get pods -A`).
    print("\n--- Pods (all namespaces) ---")
    pods = core.list_pod_for_all_namespaces(watch=False)
    for p in pods.items[:10]:  # cap output
        print(f"{p.metadata.namespace:20} {p.metadata.name:40} {p.status.phase}")

    # 2. List nodes and their readiness (a basic cluster health check).
    print("\n--- Nodes ---")
    for node in core.list_node().items:
        # Each node has a list of conditions; find the "Ready" one.
        ready = next(
            (c.status for c in node.status.conditions if c.type == "Ready"),
            "Unknown",
        )
        print(f"{node.metadata.name:30} Ready={ready}")

    # 3. AppsV1Api handles deployments/replicasets/statefulsets.
    apps = client.AppsV1Api()
    print("\n--- Deployments (all namespaces) ---")
    for d in apps.list_deployment_for_all_namespaces().items[:10]:
        ready = d.status.ready_replicas or 0
        desired = d.spec.replicas
        print(f"{d.metadata.namespace:20} {d.metadata.name:30} {ready}/{desired} ready")


if __name__ == "__main__":
    main()
