# Backend API (REST + WS)

## REST
- `GET /health` → `{status:"ok"}`
- `GET /config` / `PUT /config` (hot-reload)
- `GET /metrics/latency` (p50/p95/p99; son N)
- `GET /pnl/summary`
- `POST /mode` body:`{mode:"paper"|"live"}`  # Stop & Ask: sadece kullanıcı onayı ile
- `POST /pause` / `POST /resume`
- `POST /calibration/micro-probe` → kısa seans başlatır (paper/live maker maliyetsiz).

## WS Kanalları
- `/ws/logs` → trade log (kırmızı/yeşil satırlar)
- `/ws/opportunities` → edge stream
- `/ws/latency` → anlık HUD metrikleri

