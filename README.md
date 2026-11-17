# Kubernetes Hard-Way → GitOps Platform

A hands-on Kubernetes operations and GitOps lab built on a **manually installed, non-kubeadm** Kubernetes cluster. The goal is to document real engineering decisions and validate deployment, reconciliation, and failure-recovery behavior with reproducible experiments.

> **Validated 2026-11-17:** GitLab CI, image promotion, Argo CD automatic synchronization and self-healing, plus Gateway API routing, passed the documented lab checks. See [validation evidence](docs/evidence/2026-11-17-gitops-validation.md). A Weave Net incident remains partially unresolved; production HA is **not** claimed.

## Why this project?

- Practice Kubernetes operations on a real multi-node, self-managed cluster rather than a disposable local distribution.
- Implement pull-based GitOps with GitLab CI, container registry, Helm, and Argo CD.
- Record architecture trade-offs, controlled failure tests, diagnostics, and evidence for technical review.

## Lab architecture (sanitized)

```text
                operator / clients
                       |
                external HAProxy
                  /          \
         API :6443         HTTP :80
             |                 |
        2 API servers    NodePort :30080 on 4 nodes
             |                 |
       etcd (2 voters)   NGINX Gateway Fabric
                               |
                          HTTPRoute(s)
                               |
                         mock-payment-api
```

Four Kubernetes nodes are eligible for workloads by design, including the two control-plane nodes; `node01` is temporarily cordoned following a CNI incident. The single HAProxy instance and two-member etcd cluster are known **lab trade-offs**, not claims of production-grade high availability. Details: [sanitized architecture](docs/architecture.md).

The cluster was set up following the manual at https://github.com/mmumshad/kubernetes-the-hard-way. Prior to this project, the following modifications were made: the taints on the control-plane nodes were removed to allow workloads to be scheduled on them as well, and a gateway was added.

## Repository contents

| Path | Purpose |
| --- | --- |
| `app/` | Deliberately non-financial mock HTTP API |
| `tests/` | Python unit tests |
| `Dockerfile` | Non-root container image |
| `charts/mock-payment-api/` | Helm chart: Deployment, Service, HTTPRoute and optional HPA |
| `docs/architecture.md` | Sanitized observed architecture and limitations |
| `docs/decisions/` | Architectural decision records |
| `docs/evidence/` | Public, redacted evidence conventions |

**Implemented and validated:** GitLab CI/CD, GitOps promotion, scoped Argo CD Application/AppProject, HTTPRoute, and self-healing. **Not yet validated:** runtime autoscaling, full CNI recovery, and production-grade HA.

## Local test

Requires Python 3.12+; no third-party Python packages are needed.

```bash
python3 -m unittest discover -s tests -v
```

Validate the chart **without changing the cluster**:

```bash
helm lint charts/mock-payment-api --strict
helm template mock-payment-api charts/mock-payment-api --namespace payment-demo
```

> CI updates `image.repository` and `image.tag` in Helm values to the published registry image and full source commit SHA. The GitLab registry image must be pullable by the cluster.

## Delivery workflow (validated)

```text
GitLab CI → GitLab Container Registry → GitOps commit
                                           ↓
                                       Argo CD
                                           ↓
                                  Helm → Kubernetes
```

**GitLab** is the canonical repository for CI and desired state. **GitHub** receives a public push mirror of the same reviewed Git history. No raw credentials, cluster kubeconfigs, snapshots, or private lab outputs belong in either repository.

## Progress and evidence

| Milestone | Status |
| --- | --- |
| Existing hard-way cluster and external routing inventoried | Observed |
| Python mock API tests | Passed locally (3/3) |
| Helm chart lint/render | Passed (including optional HPA template rendering; runtime HPA untested) |
| GitLab CI image build and promotion | Passed: tests, rootless BuildKit, GitLab Registry, GitOps values commit |
| Argo CD scoped deployment | Passed: Deployment, Service, HTTPRoute; Synced / Healthy |
| Automated delivery and drift recovery | Passed: source commit → automated rollout; replica drift 1 → 2 self-healed |
| Prometheus / advanced observability | Not implemented |

Completed tests and their limits are recorded in [docs/evidence/2026-11-17-gitops-validation.md](docs/evidence/2026-11-17-gitops-validation.md).
