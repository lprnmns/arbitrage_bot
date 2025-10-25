Faz‑2 Prompt



Implement Phase‑2: paper fill simulation + real latency capture + opportunity stream.

Scope:



Maker fill simulator (queue‑based): record Q0 at place, accumulate Vt from trades at price and L2 same‑level deltas; fill when Vt ≥ k\*(Q0+size); TTL → cancel/replace.



Taker fill (VWAP) across L2 up to slippage budget; leg‑fail guard path.



Latency: record t\_tick, t\_dec, t\_s\_send/ack/fill, t\_p\_send/ack/fill; write to DB; HUD p50/p95 from DB (1 Hz).



Opportunities stream: compute edge\_net\_bps (fees/slippage via current config); red (<thr) vs green (executed sim).



CSV outputs in results/ for 15/60‑min paper sessions.

Constraints: respect Stop \& Ask; no live orders; no EVM.

Acceptance: ≥20 fills on HYPE in paper, CSVs generated, HUD p50/p95 live, stream shows red/green lines.

Report: dataset counts, example CSV head, latency percentiles, screenshots.

