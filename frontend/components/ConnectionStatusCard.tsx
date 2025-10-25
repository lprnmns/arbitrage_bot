"use client";

interface ConnectionStatusCardProps {
  status: string;
  lastMessage?: string | null;
}

export function ConnectionStatusCard({ status, lastMessage }: ConnectionStatusCardProps) {
  return (
    <div className="dashboard-card" style={{ marginBottom: "1.5rem" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h1 style={{ margin: 0 }}>Dashboard</h1>
          <p style={{ color: "#91a9ff", marginTop: "0.25rem" }}>Phase 0 / Phase 1 scaffolding</p>
        </div>
        <span className="status-pill">
          <span style={{ width: 8, height: 8, borderRadius: "50%", background: "#4ee1ad" }} />
          {status}
        </span>
      </div>
      <div style={{ marginTop: "1.5rem" }}>
        <p style={{ color: "#c3d3ff" }}>
          WebSocket heartbeat payloads simulate HL market data until credentials are approved.
        </p>
        <code style={{ background: "rgba(0,0,0,0.35)", padding: "0.5rem 0.75rem", borderRadius: 8 }}>
          {lastMessage ?? "Waiting for first heartbeat..."}
        </code>
      </div>
    </div>
  );
}
