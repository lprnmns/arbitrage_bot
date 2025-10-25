# Ortam Değişkenleri

Aşağıdaki değişkenler `.env` içinde tanımlanır (UI'da maskeli gösterilir):

- `HL_API_KEY` / `HL_API_SECRET` : Hyperliquid API kimlik bilgileri.
- `HL_ENV` : `mainnet` veya `testnet`. **Stop & Ask:** Codex, URL'leri otomatik set ETME; kullanıcıdan onayla.
- `MODE` : `paper` veya `live`.
- `DB_PATH` : `./db/arb.sqlite`
- `RESULTS_DIR` : `./results`
- `REDIS_URL` : `redis://redis:6379/0`
- `PORT_BACKEND` : `8080`
- `PORT_FRONTEND` : `3000`

> **Stop & Ask:** HL endpoint'leri ve ücret oranları için **kullanıcıdan onay almadan** sabit değer koyma. UI'da "Fees/Endpoints" formu olacak; kullanıcı dolduracak.

