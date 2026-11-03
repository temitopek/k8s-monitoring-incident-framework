#!/usr/bin/env bash
# Sends a fake "page" alert to Alertmanager, then shows the receiver output.
set -euo pipefail
curl -sf -X POST http://localhost:9093/api/v2/alerts -H 'Content-Type: application/json' -d '[{
  "labels": {"alertname": "TestAlert", "severity": "page", "job": "demo"},
  "annotations": {"summary": "Test alert from fire-test-alert.sh"}
}]'
echo "Sent. Alertmanager waits group_wait (30s) before notifying; then run:"
echo "  docker compose logs alert-receiver"
