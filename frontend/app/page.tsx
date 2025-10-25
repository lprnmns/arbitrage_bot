"use client";

import { ConnectionStatusCard } from "../components/ConnectionStatusCard";
import { LatencyHud } from "../components/LatencyHud";
import { SettingsPanel } from "../components/SettingsPanel";
import { useMockFeed } from "../hooks/useMockFeed";
import { useSettings } from "../hooks/useSettings";
import { useMarketSummary } from "../hooks/useMarketSummary";
import { useHealthMetrics } from "../hooks/useHealthMetrics";

export default function Page() {
  const feed = useMockFeed();
  const { config, save, status, loading } = useSettings();
  const markets = useMarketSummary();
  const metrics = useHealthMetrics();

  return (
    <main>
      <ConnectionStatusCard status={feed.status} heartbeat={feed.heartbeat} />
      <section className="dashboard-card">
        <h2 style={{ marginTop: 0 }}>Market Overview (HYPE / SOL / BTC)</h2>
        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ color: "#8ea2d6", textTransform: "uppercase", fontSize: "0.75rem" }}>
                <th style={{ textAlign: "left", paddingBottom: "0.5rem" }}>Symbol</th>
                <th style={{ textAlign: "left", paddingBottom: "0.5rem" }}>Best Bid</th>
                <th style={{ textAlign: "left", paddingBottom: "0.5rem" }}>Best Ask</th>
                <th style={{ textAlign: "left", paddingBottom: "0.5rem" }}>Spread (bps)</th>
                <th style={{ textAlign: "left", paddingBottom: "0.5rem" }}>Trades (1m)</th>
              </tr>
            </thead>
            <tbody>
              {markets.map((mkt) => (
                <tr key={mkt.symbol} style={{ borderTop: "1px solid rgba(255,255,255,0.08)" }}>
                  <td style={{ padding: "0.75rem 0" }}>{mkt.symbol}</td>
                  <td style={{ padding: "0.75rem 0" }}>
                    {mkt.best_bid !== null && mkt.best_bid !== undefined
                      ? `${mkt.best_bid.toFixed(4)} (${mkt.best_bid_size?.toFixed(2) ?? "--"})`
                      : "--"}
                  </td>
                  <td style={{ padding: "0.75rem 0" }}>
                    {mkt.best_ask !== null && mkt.best_ask !== undefined
                      ? `${mkt.best_ask.toFixed(4)} (${mkt.best_ask_size?.toFixed(2) ?? "--"})`
                      : "--"}
                  </td>
                  <td style={{ padding: "0.75rem 0" }}>{mkt.spread_bps ? mkt.spread_bps.toFixed(2) : "--"}</td>
                  <td style={{ padding: "0.75rem 0" }}>{mkt.trades_last_min}</td>
                </tr>
              ))}
              {markets.length === 0 && (
                <tr>
                  <td colSpan={5} style={{ padding: "1rem 0", color: "#8ea2d6" }}>
                    Waiting for ingestion...
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
      {loading ? (
        <section className="dashboard-card" style={{ marginTop: "1.5rem" }}>
          <p style={{ color: "#8ea2d6" }}>Loading settings...</p>
        </section>
      ) : (
        <SettingsPanel config={config} onSave={save} status={status} />
      )}
      <LatencyHud heartbeat={feed.heartbeat} metrics={metrics} />
    </main>
  );
}
