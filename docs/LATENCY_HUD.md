# Latency HUD Tasarımı

## Zaman Damgaları
- `t_tick`: WS sinyal mesajı alındı.
- `t_dec`: karar motoru hesapladı.
- `t_s_send / t_s_ack / t_s_fill`
- `t_p_send / t_p_ack / t_p_fill`

## Metrikler
- Ingest: `t_dec - t_tick`
- Spot ack/fill; Perp ack/fill
- Hedge tamamlanma: `max(t_s_fill, t_p_fill) - t_tick`
- E2E toplam = hedge tamamlanma

## Raporlama
- p50/p95/p99 + son N ortalaması
- WS ile UI'ya push (1 Hz)

