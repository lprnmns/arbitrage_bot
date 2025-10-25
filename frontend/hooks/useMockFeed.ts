"use client";

import { useEffect, useRef, useState } from "react";

interface FeedState {
  status: "connecting" | "open" | "error";
  message: string | null;
}

const WS_URL = process.env.NEXT_PUBLIC_WS_URL ?? "ws://localhost:8000/ws/stream";

export function useMockFeed(): FeedState {
  const [state, setState] = useState<FeedState>({ status: "connecting", message: null });
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onopen = () => setState({ status: "open", message: null });
    ws.onerror = () => setState({ status: "error", message: "connection error" });
    ws.onmessage = (event) => setState({ status: "open", message: event.data });

    return () => {
      ws.close();
    };
  }, []);

  return state;
}
