# Paper Modu

## Fill Simülatörü (Maker)
- Emri koyduğunda o seviyedeki kuyruk derinliği `Q0` kaydedilir.
- Sonraki trade ve L2 akışından **o seviyeye isabet eden hacim** `Vt` biriktirilir.
- **Fill koşulu:** `Vt ≥ k*(Q0 + size)` ; `k` kalibrasyon katsayısı (1.0–1.2).
- `inject_latency_ms`: canlı p50'ye yakın gecikme enjekte edilir.

## Taker Fill
- Top-of-book ± slippage bütçesi; fee bps düşülür.

## Mikro-Kalibrasyon (opsiyonel)
- **post-only min $1–$2** kısa seans; gerçekleşenler perpte küçük hedge ile kapanır.
- `k` ve `ttl` otomatik önerilir. **Stop & Ask:** Kullanıcı onayı olmadan değiştirme.

## Raporlama
- `results/` CSV: fill-rate, net bps, iptal oranı, ttl dağılımı, e2e p50/p95.

