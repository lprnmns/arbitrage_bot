import { useEffect, useState } from "react";
import { getJSON } from "../lib/api";

export interface HealthMetrics {
  ts: number;
  build: string;
  hl_env: string;
  hl_ws_ok: boolean;
  redis_ok: boolean;
  db_ok: boolean;
  msgs_1m: { l2: number; trades: number };
  last_tick_ts: string | null;
  uptime_s: number;
}

export function useHealthMetrics(pollMs = 2000) {
  const [metrics, setMetrics] = useState<HealthMetrics | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function fetchMetrics() {
      try {
        const data = await getJSON<HealthMetrics>("/metrics/health");
        if (!cancelled) {
          setMetrics(data);
        }
      } catch (err) {
        console.error("Failed to fetch health metrics", err);
      }
    }

    fetchMetrics();
    const id = setInterval(fetchMetrics, pollMs);
    return () => {
      cancelled = true;
      clearInterval(id);
    };
  }, [pollMs]);

  return metrics;
}
