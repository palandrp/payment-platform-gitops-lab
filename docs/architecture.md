# Lab architecture — public summary

**Observations:** initial cluster audit 2026-10-29; GitOps/Gateway validation 2026-11-17.

## Existing, observed components

| Area | Configuration |
| --- | --- |
| Kubernetes | v1.36.2; manually installed (non-kubeadm) |
| Nodes | Four Linux VMs: two control-plane/worker plus two worker; `node01` temporarily cordoned after CNI incident |
| Host OS/runtime | Ubuntu 22.04.5, containerd 2.2.1 |
| Cluster networking | Weave Net and kube-proxy; CoreDNS with two replicas |
| etcd | Two voters, intentionally retained for lab use |
| External entry point | Single HAProxy VM |
| API traffic | HAProxy TCP 6443 → both control-plane API servers |
| Application HTTP | HAProxy TCP 80 → NodePort 30080 on all four nodes, round-robin |
| Gateway | NGINX Gateway Fabric; `default/web` and `payment-demo/mock-payment-api` HTTPRoutes |
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

## Validated implementation (2026-11-17)

- GitLab CI ran unit tests and Helm validation, then built and pushed images using rootless BuildKit. A promotion job committed the full source SHA image tag to Helm values.
- Argo CD reconciled `Deployment`, `Service` and `HTTPRoute` in `payment-demo`; auto-sync and self-healing were verified.
- The existing Gateway accepts the `payment-demo` route for `payment.lab.internal`; both the payment endpoint and pre-existing `web` route returned HTTP 200. The Gateway listener change was performed outside this Application.
- After VM suspend/resume, Weave Net lost some cross-node Pod connectivity; `node01` remains cordoned. Full cluster recovery and HAProxy backend failover were **not** validated.

See [validation evidence](evidence/2026-11-17-gitops-validation.md).

## Evidence policy

Publish only sanitized, reproducible outcomes. Planned behavior is **not evidence**. Raw host inventories and credentials remain outside Git.
