# Kubernetes Operator for Managed Service Lifecycle

Declare a service once as a `ManagedService`; the operator creates it, upgrades it, schedules backups and heals it. Provisioning becomes a single `kubectl apply` instead of a multi-step manual runbook.

```yaml
apiVersion: platform.example.io/v1alpha1
kind: ManagedService
metadata: {name: demo-db}
spec: {image: postgres:16, replicas: 1, backupSchedule: "0 2 * * *"}
```

| Lifecycle | How |
|---|---|
| **Create** | Builds a headless Service, a StatefulSet (with readiness probe) and an optional backup CronJob, all owner-referenced so deleting the resource cleans up |
| **Upgrade** | Change `spec.image`; the update handler patches the StatefulSet and Kubernetes rolls it out |
| **Backup** | `spec.backupSchedule` (cron) creates a CronJob running `backupCommand` |
| **Heal** | A 30s timer re-creates deleted children and writes `status.phase` (`Ready` / `Degraded`) and `readyReplicas` |

Built with Python, [kopf](https://kopf.readthedocs.io) and the official Kubernetes client.

## Try it (kind or minikube)
```bash
kubectl apply -f deploy/crd.yaml
pip install -r requirements.txt
kopf run --standalone --all-namespaces operator/handlers.py   # terminal 1
kubectl apply -f deploy/example.yaml                          # terminal 2
kubectl get msvc,sts,svc,cronjob
kubectl delete sts demo-db                                    # it returns within ~30s
kubectl patch msvc demo-db --type merge -p '{"spec":{"image":"postgres:16.4"}}'   # rolling upgrade
```
In-cluster: build the `Dockerfile`, push it, apply `deploy/rbac.yaml`, and run it as a Deployment using that service account.

## Limitations / roadmap
Backup command is a placeholder (swap in `pg_dump` plus object storage); no persistent volume claims yet; no unit tests; add finalizers for backup-before-delete; a Go (controller-runtime) port.
