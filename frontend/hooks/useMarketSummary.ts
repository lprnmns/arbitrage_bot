"use client";

import { useEffect, useState } from "react";
import { getJSON } from "../lib/api";

export interface MarketSnapshot {
  symbol: string;
  best_bid: number | null;
  best_ask: number | null;
  best_bid_size: number | null;
  best_ask_size: number | null;
  spread_bps: number | null;
  trades_last_min: number;
}

interface MarketSummaryResponse {
  markets: MarketSnapshot[];
}

export function useMarketSummary(pollMs = 2000) {
  const [markets, setMarkets] = useState<MarketSnapshot[]>([]);

  useEffect(() => {
    let cancelled = false;

    async function fetchSummary() {
      try {
        const data = await getJSON<MarketSummaryResponse>("/markets/summary");
        if (!cancelled) {
          setMarkets(data.markets);
        }
      } catch (err) {
        console.error("Failed to fetch market summary", err);
      }
    }

    fetchSummary();
    const id = setInterval(fetchSummary, pollMs);
    return () => {
      cancelled = true;
      clearInterval(id);
    };
  }, [pollMs]);

  return markets;
}
