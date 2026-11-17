# Public engineering evidence

Publish an experiment only when it has been performed, with:

1. **Question / hypothesis** and relevant baseline.
2. **Commands, manifest diff or commit** required to reproduce it.
3. **Actual observed outcome** and links to pipeline, rollout, events or sanitized logs.
4. **Limitations** (what was not proven).
5. **Recovery / rollback** if a failure was induced.

Never publish raw `kubectl get -o yaml` dumps containing credentials, kubeconfig files, IP inventories, unredacted logs, etcd snapshots, private architecture handoffs, or interview preparation notes. Put raw evidence in a local directory excluded by `.gitignore` such as `evidence/private/`.

**Validated lab exercises:** [2026-11-17 — GitOps delivery, Gateway API and self-healing](2026-11-17-gitops-validation.md).
