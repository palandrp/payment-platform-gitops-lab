# ADR-0001: One canonical GitOps source, with a public mirror

- **Date:** 2026-10-29
- **Status:** Accepted; implementation validated 2026-11-17

## Context

The lab needs an auditable delivery path and a public, reviewable engineering history. GitHub is used to showcase the project; GitLab provides CI, container registry and the desired state watched by Argo CD.

## Decision

1. **GitLab** is the canonical repository: code, CI pipeline, Helm manifests and Argo CD desired-state references are managed there.
2. **GitHub** mirrors the same public-safe Git history. It does not become a second deployment source of truth.
3. CI builds and publishes an immutable image reference; the desired-state commit is reconciled by Argo CD (pull-based CD).
4. CI will not receive a Kubernetes `kubeconfig` or cluster-admin token.
5. No sensitive environment details will be committed, even to a private GitLab repository if it is mirrored publicly.

## Consequences

- Public and canonical histories must be safe to share before any push.
- GitLab-to-GitHub push mirroring is configured and was confirmed working.
- CI and Argo CD configurations were implemented and verified in the lab; see [validation evidence](../evidence/2026-11-17-gitops-validation.md).
