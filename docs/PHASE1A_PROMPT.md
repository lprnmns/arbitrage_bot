📄 Faz‑1a Prompt



Apply Phase‑1a mini‑improvements only. Do not start Phase‑2 yet.

Tasks:



Enable SQLite WAL \& add indexes (idx\_ticks\_symbol\_ts, idx\_trades\_symbol\_ts). Set WAL pragmas on connect.



Add GET /metrics/health returning: build, hl\_env, hl\_ws\_ok, redis\_ok, db\_ok, msgs\_1m (l2/trades), last\_tick\_ts, uptime\_s.



Wire build version from BUILD\_VERSION build‑arg/env; show in HUD.



Add logger.info lines for HL Info WS connect/disconnect and worker heartbeats.



Frontend HUD badges read from /metrics/health.

Keep Stop \& Ask rules: no hardcoded endpoints/fees, no order submission, no Phase‑2 code yet.

Report: curl samples, WAL status, index existence, example /metrics/health payload, screenshot of HUD with green badges.

