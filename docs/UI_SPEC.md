# UI Spesifikasyonu

## Sayfalar
1) **Dashboard**
   - Net PnL, günlük PnL, funding katkısı.
   - Inventory ve açık pozisyon.
   - Latency HUD (floating her sayfada).
2) **Opportunities Stream**
   - Kırmızı: edge < threshold; Yeşil: gerçekleşen trade + net bps + notional.
   - Arama/filtre: symbol, min_edge_bps.
3) **Parameters**
   - YAML form (schema-valide), hot-reload.
   - Mode switch (paper/live) → **Stop & Ask** onay penceresi.
4) **Pair Scoring**
   - HYPE/SOL/BTC karşılaştırma tablosu; Edge freq, Fill-rate, Net PnL/h.
   - "Set Live Pair" butonu → onay modali.

## Latency HUD (floating)
- Sağ üst küçük panel:
  - `E2E p50/p95`: 42ms / 85ms
  - Mini barlar: ingest, spot-ack, spot-fill, perp-ack, perp-fill.
  - VM etiketi: kullanıcı tarafından girilir; raporda görünür.

## Görsel
- Temiz, koyu tema; shadcn/ui bileşenleri; ECharts ile grafikler.

