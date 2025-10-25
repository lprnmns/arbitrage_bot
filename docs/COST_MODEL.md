# Maliyet Modeli (bps)

Bileşenler:
- Spot maker fee: **0**
- Perp taker fee: **~1.9 bps** (UI'dan girilecek; hardcode etME)
- Perp taker slipaj: **~0.5–1.5 bps** (pair'e bağlı)
- Zamanlama/iptal tamponu: **~0.5–1.0 bps**

**Hedef maliyet:** `≤ 4.0 bps`  
**Eşik önerisi:** default `4.0 bps`; güvenli `5.0 bps`; agresif `3.5 bps` (hud p95 < 80ms ise).

