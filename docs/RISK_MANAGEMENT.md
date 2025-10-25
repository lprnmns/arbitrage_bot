# Risk Yönetimi

- **Leg-fail guard:** Hedge 300ms içinde dolmazsa retry→limit→market; olmazsa maker iptal.
- **Inventory bounds:** ±order_size USD → auto-TWAP ile nötrle.
- **Circuit breakers:** daily_loss_usd ≤ -2 → pause.
- **Rate-limit:** iptal fırtınasında eşik artır.
- **Funding-aware:** negatif fundingde notional küçült, pozitifte bekleme toleransını artırma.
- **Graceful shutdown:** açık emirleri iptal et, açık pozisyonları kapat.

