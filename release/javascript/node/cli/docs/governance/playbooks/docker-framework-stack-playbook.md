# Playbook — Docker framework stack

> Issue #41

1. Open control tower + this repo.
2. Validate workflow JSON with `hath0r`.
3. Bring up redis/nginx, then `--profile apps`.
4. Healthcheck services; publish progress checkpoints to `hath0r`.
5. Tear down only via documented factory/CLI ops.
