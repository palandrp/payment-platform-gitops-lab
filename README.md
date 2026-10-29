# Kubernetes Hard-Way → GitOps Platform

A hands-on Kubernetes operations and GitOps lab built on a **manually installed, non-kubeadm** Kubernetes cluster. The goal is to document real engineering decisions and validate deployment, reconciliation, and failure-recovery behavior with reproducible experiments.

> **Status (2026-10-29):** existing lab cluster inventoried; mock API unit tests passed. **Helm rendering, CI delivery, Argo CD installation, GitOps sync, and failure tests are not yet validated.** This repository records progress; planned capabilities are not presented as completed work. Helm lint and rendering have already been successfully verified locally using Helm 4.2.4, while GitLab CI is still awaiting confirmation.

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

Four Kubernetes nodes are schedulable by design, including the two control-plane nodes. The single HAProxy instance and two-member etcd cluster are known **lab trade-offs**, not claims of production-grade high availability. Details: [sanitized architecture](docs/architecture.md).

The cluster was set up following the manual at https://github.com/mmumshad/kubernetes-the-hard-way. Prior to this project, the following modifications were made: the taints on the control-plane nodes were removed to allow workloads to be scheduled on them as well, and a gateway was added.

## Repository contents

| Path | Purpose |
| --- | --- |
| `app/` | Deliberately non-financial mock HTTP API |
| `tests/` | Python unit tests |
| `Dockerfile` | Non-root container image |
| `charts/mock-payment-api/` | Helm chart (image values are placeholders) |
| `docs/architecture.md` | Sanitized observed architecture and limitations |
| `docs/decisions/` | Architectural decision records |
| `docs/evidence/` | Public, redacted evidence conventions |

**Not included yet:** production-ready CI, Argo CD Application / AppProject, Gateway routes, monitoring, or tested recovery automation. These will be added as distinct, reviewable changes.

## Local test

Requires Python 3.12+; no third-party Python packages are needed.

```bash
python3 -m unittest discover -s tests -v
```

Once Helm is available, validate the chart **without changing the cluster**:

```bash
helm lint charts/mock-payment-api --strict
helm template mock-payment-api charts/mock-payment-api --namespace payment-demo
```

> The default `image.repository` and `image.tag` in Helm values are placeholders; deployment requires a published image and registry access.

## Delivery design (planned)

```text
GitLab CI → GitLab Container Registry → GitOps commit
                                           ↓
                                       Argo CD
                                           ↓
                                  Helm → Kubernetes
```

**GitLab** will be the canonical repository for CI and desired state. **GitHub** will carry a public mirror of the same reviewed Git history. No raw credentials, cluster kubeconfigs, snapshots, or private lab outputs belong in either repository.

## Progress and evidence

| Milestone | Status |
| --- | --- |
| Existing hard-way cluster and external routing inventoried | Observed |
| Python mock API tests | Passed locally (3/3) |
| Helm chart lint/render | Pending local validation |
| GitLab CI image build and promotion | Planned |
| Argo CD scoped deployment | Planned |
| Git drift / failure-recovery tests | Planned |
| Prometheus / advanced observability | Optional, planned |

Only completed exercises will receive links to redacted logs, commits, pipeline runs, screenshots, and incident write-ups in [`docs/evidence/`](docs/evidence/).
