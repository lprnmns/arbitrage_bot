"use client";

import { useEffect, useState } from "react";

const DEFAULT_HUD = {
  latencyMs: 42,
  p50: 38,
  p95: 65,
  feed: "Mock HL"
};

export function LatencyHud({ heartbeat }: { heartbeat: string | null }) {
  const [hud, setHud] = useState(DEFAULT_HUD);

  useEffect(() => {
    const interval = setInterval(() => {
      setHud((prev) => ({
        ...prev,
        latencyMs: 30 + Math.round(Math.random() * 20),
        p50: 25 + Math.round(Math.random() * 10),
        p95: 50 + Math.round(Math.random() * 10)
      }));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="latency-hud">
      <h3>Latency HUD</h3>
      <div style={{ fontSize: "0.8rem", color: "#9fb5ff", marginBottom: "0.5rem" }}>
        Feed: {hud.feed} - Last heartbeat: {heartbeat ?? "pending"}
      </div>
      <div className="stat-grid">
        <div className="stat">
          <span>Latency</span>
          <strong>{hud.latencyMs} ms</strong>
        </div>
        <div className="stat">
          <span>p50</span>
          <strong>{hud.p50} ms</strong>
        </div>
        <div className="stat">
          <span>p95</span>
          <strong>{hud.p95} ms</strong>
        </div>
      </div>
    </div>
  );
}
