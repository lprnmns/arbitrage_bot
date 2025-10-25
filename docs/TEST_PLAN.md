# Test Planı ve Fazlar

## Faz 0 — Repo/Ortam
- DoD: `make up` ile backend+frontend+redis ayağa kalkar, `/health=ok`.
- Test: `curl /health`; UI açılır, boş paneller.

**Stop & Ask:** "HL endpoint/fees değerlerini siz girer misiniz?"

## Faz 1 — HL Market Data
- DoD: HL WS bağlanır, HYPE/SOL/BTC L2/Trades DB'ye yazar.
- Test: UI'da canlı best bid/ask ve trade sayacı artıyor.

**Stop & Ask:** "Bu akış hız/format OK mi?"

## Faz 2 — Paper Fill Sim (LOB)
- DoD: Maker queue modeli; taker fill; latency inject.
- Test: Sim emri at, `results/` CSV'de fill-rate, ttl grafiği.

**Stop & Ask:** "`k` ve `ttl` otomatik önerileri kabul edilsin mi?"

## Faz 3 — Strateji (Spot maker → Perp hedge)
- DoD: Edge hesap, eşik≥4bps tetikleyici; leg-fail guard; TWAP.
- Test: Paper'da min 20 fill; net PnL > 0; iptal oranı < %30.

## Faz 4 — UI: Stream & HUD & Params
- DoD: Kırmızı/yeşil akış, HUD p50/p95, Parametre formu (hot-reload).
- Test: Eşik/size değişince davranış değişir; HUD güncellenir.

## Faz 5 — Pair Scoring + Rapor
- DoD: 48s paper deney; skor tablosu; "Set Live Pair" modalı.

## Faz 6 — Live Dry-Run (Emir yok)
- DoD: Live modda sadece micro-probe (maliyetsiz) ve tam akış.

**Stop & Ask:** "Gerçek emir gönderimine geçelim mi?"

## Faz 7 — Live Minimal
- DoD: `order_size=$25`, `max_open_orders=1`, günlük sınırlar aktif.
- Test: Küçük notional ile gerçek fill; hedge ve PnL hesap doğru.

## Faz 8 — Docker/Make/Runbook cilası
- DoD: `make paper` / `make live` pürüzsüz, README adımları çalışır.

