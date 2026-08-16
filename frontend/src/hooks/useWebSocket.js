import {
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";

import {
  getAccessToken,
} from "../utils/storage";


const RECONNECT_DELAYS = [
  1000,
  2000,
  5000,
  10000,
];


function useWebSocket({
  enabled,
  onMessage,
}) {
  const websocketRef =
    useRef(null);

  const reconnectTimerRef =
    useRef(null);

  const pingTimerRef =
    useRef(null);

  const reconnectAttemptRef =
    useRef(0);

  const manuallyClosedRef =
    useRef(false);

  const onMessageRef =
    useRef(onMessage);

  const connectRef =
    useRef(null);

  const [connected, setConnected] =
    useState(false);


  useEffect(() => {
    onMessageRef.current =
      onMessage;
  }, [onMessage]);


  const clearReconnectTimer =
    useCallback(() => {
      if (
        reconnectTimerRef.current
      ) {
        window.clearTimeout(
          reconnectTimerRef.current
        );

        reconnectTimerRef.current =
          null;
      }
    }, []);


  const clearPingTimer =
    useCallback(() => {
      if (
        pingTimerRef.current
      ) {
        window.clearInterval(
          pingTimerRef.current
        );

        pingTimerRef.current =
          null;
      }
    }, []);


  const clearTimers =
    useCallback(() => {
      clearReconnectTimer();
      clearPingTimer();
    }, [
      clearReconnectTimer,
      clearPingTimer,
    ]);


  const closeSocket =
    useCallback(() => {
      manuallyClosedRef.current =
        true;

      clearTimers();

      const websocket =
        websocketRef.current;

      if (websocket) {
        websocket.onopen =
          null;

        websocket.onmessage =
          null;

        websocket.onclose =
          null;

        websocket.onerror =
          null;

        if (
          websocket.readyState ===
            WebSocket.OPEN ||
          websocket.readyState ===
            WebSocket.CONNECTING
        ) {
          websocket.close();
        }
      }

      websocketRef.current =
        null;

      reconnectAttemptRef.current =
        0;

      setConnected(false);
    }, [clearTimers]);


  const connect =
    useCallback(() => {
      if (!enabled) {
        return;
      }

      const token =
        getAccessToken();

      if (!token) {
        return;
      }

      const rawBaseUrl =
        import.meta.env
          .VITE_WS_BASE_URL;

      if (!rawBaseUrl) {
        setConnected(false);
        return;
      }

      const existing =
        websocketRef.current;

      if (
        existing &&
        (
          existing.readyState ===
            WebSocket.OPEN ||
          existing.readyState ===
            WebSocket.CONNECTING
        )
      ) {
        return;
      }

      manuallyClosedRef.current =
        false;

      const baseUrl =
        rawBaseUrl.replace(
          /\/$/,
          ""
        );

      const socketUrl =
        `${baseUrl}/ws/notifications` +
        `?token=${encodeURIComponent(token)}`;


      let websocket;

      try {
        websocket =
          new WebSocket(
            socketUrl
          );
      } catch {
        setConnected(false);
        return;
      }


      websocketRef.current =
        websocket;


      websocket.onopen =
        () => {
          clearReconnectTimer();
          clearPingTimer();

          reconnectAttemptRef.current =
            0;

          setConnected(true);

          pingTimerRef.current =
            window.setInterval(
              () => {
                if (
                  websocket.readyState ===
                  WebSocket.OPEN
                ) {
                  websocket.send(
                    "PING"
                  );
                }
              },
              30000
            );
        };


      websocket.onmessage =
        (event) => {
          try {
            const message =
              JSON.parse(
                event.data
              );

            onMessageRef.current?.(
              message
            );
          } catch {
            // Ignore malformed messages.
          }
        };


      websocket.onerror =
        () => {
          if (
            websocket.readyState ===
              WebSocket.OPEN ||
            websocket.readyState ===
              WebSocket.CONNECTING
          ) {
            websocket.close();
          }
        };


      websocket.onclose =
        () => {
          clearPingTimer();

          setConnected(false);

          websocketRef.current =
            null;

          if (
            manuallyClosedRef.current ||
            !enabled
          ) {
            return;
          }

          const attempt =
            reconnectAttemptRef.current;

          const delay =
            RECONNECT_DELAYS[
              Math.min(
                attempt,
                RECONNECT_DELAYS.length -
                  1
              )
            ];

          reconnectAttemptRef.current =
            attempt + 1;

          clearReconnectTimer();

          reconnectTimerRef.current =
            window.setTimeout(
              () => {
                connectRef.current?.();
              },
              delay
            );
        };
    }, [
      enabled,
      clearPingTimer,
      clearReconnectTimer,
    ]);


  useEffect(() => {
    connectRef.current =
      connect;
  }, [connect]);


  useEffect(() => {
    if (enabled) {
      connect();
    } else {
      closeSocket();
    }

    return () => {
      closeSocket();
    };
  }, [
    enabled,
    connect,
    closeSocket,
  ]);


  return {
    connected,
    reconnect:
      connect,
    disconnect:
      closeSocket,
  };
}


export default useWebSocket;