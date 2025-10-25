# Codex Kickoff Prompt (Yalnızca Faz 0 + Faz 1)

Aşağıdaki kurallara UY:
- `docs/CONTRIBUTING_AGENT_RULES.md`'yi **bire bir** uygula.
- Şu an SADECE `TEST_PLAN.md` Faz 0 ve Faz 1'i uygula. İleri gitME.
- HyperEVM/contract/pool adresleri KULLANMA. HL ücret/endpoint HARDOCDE ETME.

### Görevler (Faz 0 + Faz 1)
1) Proje iskeletini oluştur (dizinler + boş yerleşim dosyaları).
2) Docker Compose iskeleti: backend, worker, frontend, redis (tag'leri sabitle ama değiştirmeden önce onay sor).
3) Backend minimal:
   - FastAPI `/health`
   - WS altyapısı placeholder (henüz veri yok)
   - SQLite bağlan (tablo migrasyonları boş şema ile)
4) Frontend minimal:
   - Next.js uygulaması, boş Dashboard sayfası
   - WebSocket bağlanabilirlik testi (mock channel)
   - Floating Latency HUD placeholder bileşeni (dummy sayılar)
5) HL WS Market Data (Faz 1):
   - **Stop & Ask:** "HL endpoint/fees değerlerini UI'dan siz girer misiniz, yoksa testnet mi kullanalım?" diye sor.
   - Kullanıcı testnet isterse WS'e bağlan; HYPE/SOL/BTC L2+Trades stream'ini alıp `ticks/trades` tablolarına yaz.
   - UI'da best bid/ask ve trade sayacı canlı göster.
6) Raporla:
   - Çalışan servisler, erişim URL'leri
   - Manuel test adımları (`curl /health`, UI'da canlı sayaç)
   - Sonraki faz için "hazır" olduğunda **onay iste**.

### Çıkış Kriteri
- `make up` → `/health=ok`, UI açılıyor, canlı market data akışı görülüyor.

**Unutma:** Bir sonraki faza GEÇME; kullanıcıdan onay gelmeden ilerleme.

