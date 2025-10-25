"use client";

import { useEffect, useState } from "react";
import type { ConfigResponse, ConfigUpdateRequest, FeeConfig, Network } from "../hooks/useSettings";

interface Props {
  config: ConfigResponse | null;
  onSave: (payload: ConfigUpdateRequest) => Promise<void>;
  status: "idle" | "saving" | "success";
}

export function SettingsPanel({ config, onSave, status }: Props) {
  const [network, setNetwork] = useState<Network>("mainnet");
  const [fees, setFees] = useState<FeeConfig>({ spot_fee_bps: null, perp_fee_bps: null });
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (config) {
      setNetwork(config.network);
      setFees(config.fees);
    }
  }, [config]);

  const handleNumberChange = (key: keyof FeeConfig) => (value: string) => {
    setFees((prev) => ({
      ...prev,
      [key]: value === "" ? null : Number(value)
    }));
  };

  const handleSubmit = async () => {
    if (!config) return;
    setError(null);
    try {
      await onSave({ network, fees });
    } catch (err) {
      setError("Failed to save settings");
    }
  };

  return (
    <section className="dashboard-card" style={{ marginTop: "1.5rem" }}>
      <h2 style={{ marginTop: 0 }}>Network & Fees</h2>
      <p style={{ color: "#91a9ff", fontSize: "0.9rem" }}>
        Configure which HL environment to read from and feed Spot/Perp fees manually (per Stop & Ask).
      </p>
      {error && <p style={{ color: "#ff8c8c" }}>{error}</p>}
      <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap" }}>
        <label style={{ flex: 1, minWidth: 240 }}>
          <span className="input-label">Network</span>
          <select
            value={network}
            onChange={(event) => setNetwork(event.target.value as Network)}
            className="input"
          >
            <option value="mainnet">Mainnet</option>
            <option value="testnet">Testnet</option>
          </select>
        </label>
        <label style={{ flex: 1, minWidth: 240 }}>
          <span className="input-label">API Base URL</span>
          <input className="input" value={config?.api_base_url ?? "--"} disabled />
        </label>
      </div>
      <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap", marginTop: "1rem" }}>
        <label style={{ flex: 1, minWidth: 240 }}>
          <span className="input-label">Spot Fee (bps)</span>
          <input
            type="number"
            className="input"
            value={fees.spot_fee_bps ?? ""}
            onChange={(event) => handleNumberChange("spot_fee_bps")(event.target.value)}
            placeholder="Enter when available"
          />
        </label>
        <label style={{ flex: 1, minWidth: 240 }}>
          <span className="input-label">Perp Fee (bps)</span>
          <input
            type="number"
            className="input"
            value={fees.perp_fee_bps ?? ""}
            onChange={(event) => handleNumberChange("perp_fee_bps")(event.target.value)}
            placeholder="Enter when available"
          />
        </label>
      </div>
      <div style={{ marginTop: "1rem", display: "flex", justifyContent: "flex-end", gap: "0.75rem" }}>
        <button className="button" onClick={handleSubmit} disabled={status === "saving" || !config}>
          {status === "saving" ? "Saving..." : status === "success" ? "Saved" : "Save Settings"}
        </button>
      </div>
    </section>
  );
}
