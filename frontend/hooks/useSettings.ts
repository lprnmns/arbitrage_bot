"use client";

import { useCallback, useEffect, useState } from "react";
import { API_BASE_URL, getJSON } from "../lib/api";

export type Network = "mainnet" | "testnet";

export interface FeeConfig {
  spot_fee_bps: number | null;
  perp_fee_bps: number | null;
}

export interface ConfigResponse {
  network: Network;
  api_base_url: string;
  fees: FeeConfig;
}

export interface ConfigUpdateRequest {
  network: Network;
  fees: FeeConfig;
}

export function useSettings() {
  const [config, setConfig] = useState<ConfigResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<"idle" | "saving" | "success">("idle");

  useEffect(() => {
    getJSON<ConfigResponse>("/config")
      .then((data) => {
        setConfig(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const save = useCallback(async (payload: ConfigUpdateRequest) => {
    setStatus("saving");
    const res = await fetch(`${API_BASE_URL}/config`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      setStatus("idle");
      throw new Error("Failed to save settings");
    }
    const data: ConfigResponse = await res.json();
    setConfig(data);
    setStatus("success");
    setTimeout(() => setStatus("idle"), 1500);
  }, []);

  return { config, loading, error, status, save };
}
