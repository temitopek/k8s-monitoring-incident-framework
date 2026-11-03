# Runbooks
## TargetDown
1. Check `up{job="..."}` in Prometheus and the target's Loki logs.
2. Is the host/pod running? Check network, DNS, certs.
3. Restore, then add findings to the incident postmortem.
