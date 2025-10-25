"use client";

import { useEffect, useRef, useState } from "react";

export interface HeartbeatPayload {
  ts: number;
  mode: string;
  backend_ws_ok: boolean;
  redis_ok: boolean;
  db_ok: boolean;
  hl_env: string;
  latency_mock_ms: number;
  build: string;
}

interface FeedState {
  status: "connecting" | "open" | "error";
  heartbeat: HeartbeatPayload | null;
}

const WS_URL = process.env.NEXT_PUBLIC_WS_URL ?? "ws://localhost:8000/ws/stream";

export function useMockFeed(): FeedState {
  const [state, setState] = useState<FeedState>({ status: "connecting", heartbeat: null });
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onopen = () => setState((prev) => ({ ...prev, status: "open" }));
    ws.onerror = () => setState((prev) => ({ ...prev, status: "error" }));
    ws.onmessage = (event) => {
      try {
        const payload: HeartbeatPayload = JSON.parse(event.data);
        setState({ status: "open", heartbeat: payload });
      } catch (err) {
        console.error("Invalid heartbeat payload", err);
      }
    };

    return () => {
      ws.close();
    };
  }, []);

  return state;
}
