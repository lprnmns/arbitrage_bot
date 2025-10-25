"use client";

import { useEffect, useState } from "react";
import type { HeartbeatPayload } from "../hooks/useMockFeed";
import type { HealthMetrics } from "../hooks/useHealthMetrics";

const DEFAULT_HUD = {
  latencyMs: 42,
  p50: 38,
  p95: 65
};

interface LatencyHudProps {
  heartbeat: HeartbeatPayload | null;
  metrics: HealthMetrics | null;
}

export function LatencyHud({ heartbeat, metrics }: LatencyHudProps) {
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

  const statusBadge = (label: string, ok: boolean) => (
    <span
      key={label}
      className="status-pill"
      style={{
        background: ok ? "rgba(78, 225, 173, 0.1)" : "rgba(255, 102, 102, 0.12)",
        borderColor: ok ? "rgba(78, 225, 173, 0.3)" : "rgba(255, 102, 102, 0.4)",
        color: ok ? "#4ee1ad" : "#ff8c8c"
      }}
    >
      <span
        style={{
          width: 8,
          height: 8,
          borderRadius: "50%",
          background: ok ? "#4ee1ad" : "#ff6b6b"
        }}
      />
      {label}
    </span>
  );

  const buildLabel = metrics?.build ?? heartbeat?.build ?? "dev";
  const envLabel = metrics?.hl_env ?? heartbeat?.hl_env ?? "--";

  return (
    <div className="latency-hud">
      <h3>Latency HUD</h3>
      <div style={{ fontSize: "0.8rem", color: "#9fb5ff", marginBottom: "0.5rem" }}>
        Env: {envLabel} - Build: {buildLabel}
      </div>
      <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", marginBottom: "0.75rem" }}>
        {statusBadge("HL WS", Boolean(metrics?.hl_ws_ok))}
        {statusBadge("Redis", Boolean(metrics?.redis_ok))}
        {statusBadge("DB", Boolean(metrics?.db_ok))}
      </div>
      <div className="stat-grid">
        <div className="stat">
          <span>Latency</span>
          <strong>{heartbeat?.latency_mock_ms ?? hud.latencyMs} ms</strong>
        </div>
        <div className="stat">
          <span>p50</span>
          <strong>{hud.p50} ms</strong>
        </div>
        <div className="stat">
          <span>p95</span>
          <strong>{hud.p95} ms</strong>
        </div>
        <div className="stat">
          <span>Msgs (1m)</span>
          <strong>
            {metrics ? `${metrics.msgs_1m.l2} L2 / ${metrics.msgs_1m.trades} trades` : "--"}
          </strong>
        </div>
      </div>
      <p style={{ fontSize: "0.8rem", color: "#9fb5ff", marginTop: "0.75rem" }}>
        Last tick:{" "}
        {metrics?.last_tick_ts ??
          (heartbeat?.ts ? new Date(heartbeat.ts).toISOString() : "--")}{" "}
        - Uptime: {metrics ? `${metrics.uptime_s}s` : "--"}
      </p>
    </div>
  );
}
