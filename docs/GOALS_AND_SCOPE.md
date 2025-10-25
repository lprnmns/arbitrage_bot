# Amaçlar ve Kapsam

## Ana Amaçlar
1. **Tek kod tabanı**, `mode=paper|live` ile yalnızca iletim/sim katmanında fark.
2. **Hyperliquid içi** spot↔perp arbitraj (gas yok). EVM mod **devre dışı**.
3. **UI** üzerinden parametre yönetimi (hot-reload), canlı log ve PnL.
4. **Latency HUD** ile E2E ms ölçümü; en iyi VM'i seçebilmek.
5. **Paper = Live davranışı**: LOB kuyruk temelli maker fill simülasyonu + opsiyonel mikro-kalibrasyon.
6. **Aşamalı geliştirme**: Her fazda test, `Stop & Ask` onayları.

## Kapsam Dışı (v1)
- HyperEVM on-chain işlemler (gas/contract/pool adresleri).
- Çoklu eşzamanlı maker emri (v1'de `max_open_orders=1`).
- Kaldıraçlı yüksek risk modları (max 1–2x sınırı UI ile kilitli).

