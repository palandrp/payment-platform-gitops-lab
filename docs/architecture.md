# Lab architecture — public summary

**Last documented observation:** 2026-10-29. This is an operator-supplied observation, not an independently tested availability guarantee.

## Existing, observed components

| Area | Configuration |
| --- | --- |
| Kubernetes | v1.36.2; manually installed (non-kubeadm) |
| Nodes | Four Linux VMs: two control-plane/worker plus two worker; all schedulable by design |
| Host OS/runtime | Ubuntu 22.04.5, containerd 2.2.1 |
| Cluster networking | Weave Net and kube-proxy; CoreDNS with two replicas |
| etcd | Two voters, intentionally retained for lab use |
| External entry point | Single HAProxy VM |
| API traffic | HAProxy TCP 6443 → both control-plane API servers |
| Application HTTP | HAProxy TCP 80 → NodePort 30080 on all four nodes, round-robin |
| Gateway | NGINX Gateway Fabric; existing `default/web` HTTPRoute |
| Gateway Service | `NodePort`, `externalTrafficPolicy: Cluster` |
| Metrics | Metrics Server not installed as of observation |
| Persistent storage | No StorageClass/PV/PVC observed |

Network addresses, host inventory, certificates, raw configuration and machine logs are intentionally excluded.

## Known limitations / accepted trade-offs

1. **Two-member etcd quorum:** a single voting member failure removes majority. Not production HA.
2. **Single HAProxy:** shared entry-point SPOF for API and HTTP traffic.
3. **Ingress health checks:** TCP backend checks demonstrate port reachability, not end-to-end HTTP health.
4. **Small VMs:** resources can be increased on the hypervisor; monitoring capacity will be assessed before installation.
5. **Metrics API unavailable:** HPA exercises are deferred until metrics are installed and verified.

## Planned implementation (not yet performed)

- GitLab-backed CI and container registry.
- Namespaced, least-privilege Argo CD management of `payment-demo`.
- Reuse the existing Gateway API; confirm cross-namespace `allowedRoutes` and hostname routing first.
- Test declared state reconciliation, safe rollouts, worker maintenance, and Git-based recovery.

## Evidence policy

Publish only sanitized, reproducible outcomes. Planned behavior is **not evidence**. Raw host inventories and credentials remain outside Git.
