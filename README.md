# Monitoring, Alerting & Incident Analysis Framework

A reproducible observability stack (Prometheus, Alertmanager, Grafana, Loki) with **actionable alerting** and a **post-incident analysis process**.

## Why
Noisy alerts slow down incident response. This setup follows three rules:
1. **Page only on symptoms** (SLO burn, target down); open tickets for causes (CPU, disk trend).
2. **Group and inhibit** so one outage produces one notification, not fifty (see `alertmanager/alertmanager.yml`).
3. **Learn from every incident** using `docs/postmortem-template.md` and per-alert runbooks.

## Run locally
```bash
docker compose up -d
# Prometheus :9090   Alertmanager :9093   Grafana :3000 (admin/admin)   Loki :3100
./scripts/fire-test-alert.sh          # sends a fake page-level alert
docker compose logs alert-receiver    # after ~30s you will see it routed and delivered
```
In Grafana, open **Explore -> Loki** and query `{container=~".+"}` to see container logs shipped by Grafana Alloy.

## What's inside
| Path | Purpose |
|---|---|
| `prometheus/alerts.yml` | Availability, SLO burn-rate, saturation and Kubernetes alerts |
| `alertmanager/alertmanager.yml` | Severity-based routing, grouping, inhibition |
| `grafana/provisioning` | Auto-provisioned Prometheus and Loki datasources |
| `receiver/` | Demo alert receiver that prints notifications (swap for Slack/PagerDuty/email) |
| `alloy/config.alloy` | Grafana Alloy config shipping Docker container logs to Loki |
| `scripts/fire-test-alert.sh` | Sends a test alert end to end |
| `docs/` | Postmortem template and runbooks |

## Notes
Kubernetes alerts need kube-state-metrics; the burn-rate alert assumes an `http_requests_total` metric. Adjust to your services. The demo receiver only prints alerts; configure a real receiver in `alertmanager/alertmanager.yml` for production. Alloy mounts the Docker socket read-only, which is fine locally but should be reviewed before use elsewhere.
