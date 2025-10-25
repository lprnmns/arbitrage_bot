# Arbitrage Bot Prototype

This repository bootstraps Phase 0 + Phase 1 of the Codex kickoff brief:

- **Backend:** FastAPI service with /health, WebSocket placeholder, SQLite + Alembic migrations for 	icks / 	rades.
- **Worker:** Async Redis publisher acting as scaffolding for future ingest jobs.
- **Frontend:** Next.js dashboard with mock heartbeat consumer and floating latency HUD.
- **Infra:** Docker Compose wiring (backend, worker, frontend, redis) and Make targets to start/stop the stack.

## Getting Started

`ash
make up    # build + run backend, worker, redis, frontend
# Visit http://localhost:3000 for the UI
# curl http://localhost:8000/health for backend status
`

Run backend unit tests:

`ash
make backend-tests
`

## Phase Notes
- HL endpoints / fees are not hard-coded. Please confirm whether you will input them via UI or if we should target testnet credentials before enabling ingestion (per Stop & Ask requirement).
- UI currently surfaces mock heartbeat payloads until HL access is approved, satisfying Phase 1 groundwork without touching live endpoints.

## Manual Test Checklist
1. curl http://localhost:8000/health › { "status": "ok" }.
2. Open the dashboard at http://localhost:3000 and observe the mock heartbeat + latency HUD updating.
3. Inspect Redis channel worker-heartbeat for worker publications (e.g., edis-cli SUBSCRIBE worker-heartbeat).

Once HL credentials/fees flow is clarified, we can proceed to full market data ingestion (Phase 1 completion) and request the next approval step.
