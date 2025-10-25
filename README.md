# Arbitrage Bot Prototype

Phase 0 + Phase 1 scaffolding for the Codex kickoff brief:

- **Backend:** FastAPI with /health, /config, /markets/summary, /metrics/health, WebSocket heartbeats/logs, SQLite (WAL) + Alembic migrations, and an HL Info WS ingestion worker (HYPE/SOL/BTC).
- **Worker:** Async Redis heartbeat publisher placeholder with logging.
- **Frontend:** Next.js dashboard surfacing best bid/ask + trade counters, Latency HUD (fed by /metrics/health), and a Settings panel for manual HL endpoint/fee inputs.
- **Infra:** Docker Compose wiring (backend, worker, frontend, redis) and Make targets for common flows.

## Getting Started

`ash
make up          # build + run backend, frontend, worker, redis
# Visit http://localhost:3000 for the UI
# curl http://localhost:8000/health for backend status
# curl http://localhost:8000/metrics/health for subsystem metrics
`

Quick checks:

`ash
make backend-tests   # pytest smoke suite
make check           # alias that runs backend smoke tests
npm --prefix frontend run lint
`

## Settings & Stop & Ask decisions
- **Network switch:** Choose mainnet (default) or 	estnet; API base URL auto-populates from hyperliquid.utils.constants.
- **Fees:** Enter Spot/Perp fee bps manually in the UI (never hard-coded). Saved values hot-reload backend config (config/default.yaml).
- **Info WS:** Phase 1 ingest connects to mainnet Info/WS in read-only mode (no trade/exec calls) and writes ticks/trades to SQLite per DATA_MODEL.md.

## Manual Test Checklist
1. curl http://localhost:8000/health → { "status": "ok" }.
2. make up → visit http://localhost:3000:
   - Dashboard table shows live best bid/ask + 1m trade counts for HYPE/SOL/BTC.
   - Latency HUD badges stay green using /metrics/health (HL WS, Redis, DB, build label).
   - Settings panel → select network, input fees, click Save (observe toast + updated config via GET /config).
3. Inspect db/arbitrage.db (e.g., sqlite3 db/arbitrage.db 'SELECT COUNT(*) FROM ticks;') to confirm rows increasing; WAL + indexes keep reads smooth.
4. Tail logs via websocat ws://localhost:8000/ws/logs (connect/disconnect messages when HL WS restarts).

Once these pass, Phase 1 acceptance criteria are met: /health + /metrics/health stable, HL Info WS populates ticks/trades, UI reflects best bid/ask + trade counters, and fees remain user-provided. Request approval before moving to Phase 2.
