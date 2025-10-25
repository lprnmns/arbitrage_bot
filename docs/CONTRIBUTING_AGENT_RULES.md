# Codex İçin Kurallar (Çok Önemli)

1) **Asla tek hamlede hepsini yapma.** Yalnızca `TEST_PLAN.md`'deki **aktif faz**ı uygula.
2) Her faz sonunda **raporla** ve **"Stop & Ask"** sorularını kullanıcıya yönelt; onay gelmeden ilerleme.
3) **HyperEVM/contract/pool adresleri**: Bu sürümde KULLANMA. Ekleme taleplerinde kullanıcıdan yazılı onay al.
4) **HL ücretleri/endpoints**: Kullanıcı UI'dan girecek. Hardcode etME.
5) Her değişiklik **kısa diffs** ve **manuel test adımları** ile gelsin.
6) Riskli/Destrüktif işlemler için **onay modalı** koy (DB reset, live mode).
7) Her modül için **Unit test** (mümkün olan yerlerde), ve **manual test** talimatı yaz.
8) **Log seviyeleri**: INFO varsayılan; hata durumunda kullanıcıya sade özet + "log ID" ver.

