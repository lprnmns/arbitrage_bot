# Mimari

## Bileşenler
- **frontend/**: Next.js (TS) + WebSocket; Dashboard, Opportunity Stream, Latency HUD, Parametre Paneli.
- **backend/**: FastAPI (Python, asyncio, uvloop). REST + WS:
  - HL WS/REST bağlayıcı (market data, orders).
  - Paper sim (LOB queue-based fill).
  - PnL/metrics/latency aggregator.
  - Redis pub/sub ile worker iletişimi.
- **worker/**: Strateji motoru (signal → place maker spot → hedge perp).
- **db/sqlite**: `ticks`, `orders`, `fills`, `opportunities`, `latencies`, `experiments` vb.
- **results/**: Paper CSV/TXT raporları.

## Veri Akışı (özet)
1) HL WS → backend data ingester → `ticks/orderbook_events`.
2) Worker → edge hesap → `opportunities` → karar → emir.
3) Mode=live: HL APIs; Mode=paper: simülasyon.
4) Fills & funding → PnL hesap → UI/WS stream.
5) Latency timestamps → aggregator → HUD.

## Ölçek ve Gecikme
- **asyncio + uvloop**; tek işlemci çekirdeğinde düşük gecikme.
- Redis pub/sub minimal; ağır analitik yok (v1).

