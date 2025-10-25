# Konfigürasyon (YAML)

`config/default.yaml` (UI üzerinden hot-reload edilir)

```yaml
pairs:
  - symbol: HYPE
    enabled: true
    spot_maker:
      order_size_usd: 25
      max_open_orders: 1
      cancel_replace_ttl_sec: 3
      post_only: true
    perp_hedge:
      taker: true
      max_leverage: 1
      funding_aware: true
risk:
  min_edge_after_fees_bps: 4.0
  slippage_budget_bps: 1.5
  inventory_bounds_usd: 25
  rate_limit:
    max_cancels_10s: 3
    edge_increment_bps: 1.0
  circuit_breakers:
    daily_loss_usd: -2
paper:
  maker_simulation:
    queue_k_factor: 1.05   # 1.0–1.2 arası kalibre edilir
    inject_latency_ms: 40  # ölçtüğün p50 e2e'ye yakın
  evm_arbitrage_scan: false
ui:
  latency_hud: true
scoring:
  enabled: true
  pairs: [HYPE, SOL, BTC]
  weights: { edge_freq: 0.3, fill_rate: 0.3, pnl_per_hour: 0.3, cancel_rate: -0.1 }
```

