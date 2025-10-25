# Live Mod

## Pre-flight Checklist (Stop & Ask)
1) HL endpoints & fees UI'da dolduruldu mu?
2) API key/secret test başarıyla geçti mi?
3) `order_size_usd` ≤ $40, `max_open_orders=1`?
4) Circuit breakers aktif mi? daily_loss_usd=-2?
5) Latency HUD p95 < 150ms?

## Başlat
- `make live` (UI onayı gerekir)
- İlk 10 dakika sadece **maker micro-probe**? (opsiyonel)
- Ardından normal strateji.

## İzleme
- E2E p50/p95; fill-rate; funding katkısı; net PnL.

