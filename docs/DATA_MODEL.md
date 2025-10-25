# Veri Modeli (SQLite)

## Tablolar
- `ticks(id, ts_ns, symbol, venue, best_bid, best_ask, best_bid_sz, best_ask_sz)`
- `trades(id, ts_ns, symbol, venue, side, px, sz)`
- `opportunities(id, ts_ns, symbol, edge_bps_raw, edge_bps_net, reason)`
- `orders(id, ts_ns, symbol, venue, side, px, sz, type, status, mode, client_id)`
- `fills(id, ts_ns, order_id, px, sz, fee_bps, slip_bps, mode)`
- `balances(id, ts_ns, asset, free, locked, venue)`
- `funding(id, ts_ns, symbol, rate_bps)`
- `latencies(id, ts_ns, symbol, ingest_ms, spot_ack_ms, spot_fill_ms, perp_ack_ms, perp_fill_ms, e2e_ms)`
- `experiments(id, started_at, ended_at, config_hash, pair, mode, notes)`

## İndeksler
- `ticks(ts_ns, symbol)`, `orders(ts_ns)`, `fills(order_id)`

## Notlar
- Zaman damgaları `ns` (monotonic snapshot + wall-clock) çift yazılır.

