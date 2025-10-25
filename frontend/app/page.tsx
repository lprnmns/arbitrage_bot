import { ConnectionStatusCard } from "../components/ConnectionStatusCard";
import { LatencyHud } from "../components/LatencyHud";
import { useMockFeed } from "../hooks/useMockFeed";

export default function Page() {
  const feed = useMockFeed();

  return (
    <main>
      <ConnectionStatusCard status={feed.status} lastMessage={feed.message} />
      <section className="dashboard-card">
        <h2 style={{ marginTop: 0 }}>Market Overview</h2>
        <div className="stat-grid">
          {[
            { label: "Best Bid", value: "--" },
            { label: "Best Ask", value: "--" },
            { label: "Trades", value: "0" }
          ].map((stat) => (
            <div key={stat.label} className="stat">
              <span>{stat.label}</span>
              <strong>{stat.value}</strong>
            </div>
          ))}
        </div>
        <p style={{ marginTop: "1.5rem", color: "#8ea2d6" }}>
          Live best bid/ask and trade counters will activate once HL market data credentials are provided.
        </p>
      </section>
      <LatencyHud heartbeat={feed.message} />
    </main>
  );
}
