# Strateji

## Akış (sell-arb örneği)
1) Edge hesap: `(SpotAsk - PerpBid)/mid`
2) `edge_net ≥ min_edge_after_fees_bps` ise:
   - Spot **maker post-only** limit yerleştir (top-of-book üstüne).
3) Fill olursa → Perp tarafında **taker market** hedge (limit→market fallback).
4) Leg fail guard: hedge 300ms içinde dolmazsa retry; başarısızsa spot emri iptal.
5) Inventory bounds aşılırsa **TWAP re-hedge**.

## Parametreler (default)
- `min_edge_after_fees_bps = 4.0`
- `slippage_budget_bps = 1.5`
- `order_size_usd = 25–40`
- `cancel_replace_ttl = 3s`
- `rate_limit`: 10s'de ≤3 iptal, aşılırsa eşiğe +1 bps
- `funding_aware`: Çok negatif funding → notional küçült

