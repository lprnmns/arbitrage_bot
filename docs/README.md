# HL Spot (Maker) ↔ Perp (Taker) Arbitraj Botu

Bu proje, **Hyperliquid içinde** (EVM/gas yok) **Spot (maker, post-only)** ile başlayıp **Perp (taker)** ile hedge eden düşük sermaye odaklı bir arbitraj botudur. Amaç:
- **$100** sermayede **ücret ≤ ~4 bps** maliyet bandında **net ≥ 4 bps** edge yakalayarak mikro kârlar üretmek,
- **Paper ve Live modlarının aynı stratejiyi** çalıştırması (aynı karar akışı), farkın yalnızca fill mikro-mekaniğinden gelmesi,
- **UI ile yönetim**, parametreleri kod değiştirmeden ayarlama, **tek komutla** başlatma,
- Her aşamada **test edilebilir adımlar** ve **Stop & Ask** onay geçitleriyle hataları erkenden yakalamak.

> **Önemli:** HyperEVM/contract/pool adresleri bu sürümde **kullanılmıyor**. İleride araştırma modunda açılacak. Adresleri asla hardcode etmeyin.

**Hızlı bakış**
- **Strateji:** Spot maker + Perp taker hedge; funding-aware; TWAP re-hedge; leg-fail guard.
- **Varsayılan eşik:** 4.0 bps net (UI'dan anlık ayarlanır).
- **Varsayılan notional:** $25–$40 (tek açık emir).
- **Latency HUD:** Her sayfada floating; E2E p50/p95 ms; VM karşılaştırma.

İlgili dokümanlar:
- Genel hedefler: `GOALS_AND_SCOPE.md`
- Mimari: `ARCHITECTURE.md`
- Strateji: `STRATEGY.md`, `COST_MODEL.md`, `RISK_MANAGEMENT.md`
- Paper modu: `PAPER_MODE.md` (LOB kuyruk simülatörü + kalibrasyon)
- UI: `UI_SPEC.md`, `LATENCY_HUD.md`
- Test planı & Fazlar: `TEST_PLAN.md`
- Codex kuralları: `CONTRIBUTING_AGENT_RULES.md`

