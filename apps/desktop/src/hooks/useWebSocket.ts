import { useEffect, useRef, useCallback, useState } from "react";
import { useLogStore } from "../stores/useLogStore";
import { useAgentStore } from "../stores/useAgentStore";
import { WS_URL } from "../utils/constants";

export function useWebSocket(sessionId: string) {
    const ws = useRef<WebSocket | null>(null);
    const [isConnected, setIsConnected] = useState(false);
    const addLog = useLogStore((s) => s.addLog);
    const updateAgent = useAgentStore((s) => s.updateAgent);

    useEffect(() => {
        const connect = () => {
            ws.current = new WebSocket(`${WS_URL}/${sessionId}`);

            ws.current.onopen = () => {
                setIsConnected(true);
                addLog({
                    timestamp: new Date().toISOString(),
                    agent: "System",
                    level: "info",
                    message: "Connected to HANTER Core",
                });
            };

            ws.current.onmessage = (event) => {
                const data = JSON.parse(event.data);
                handleMessage(data);
            };

            ws.current.onclose = () => {
                setIsConnected(false);
                setTimeout(connect, 3000);
            };

            ws.current.onerror = () => {
                addLog({
                    timestamp: new Date().toISOString(),
                    agent: "System",
                    level: "error",
                    message: "WebSocket connection error",
                });
            };
        };

        connect();
        return () => ws.current?.close();
    }, [sessionId]);

    const handleMessage = useCallback(
        (data: any) => {
            switch (data.type) {
                case "task_update":
                    updateAgent(data.agent, {
                        status: data.status === "running" ? "busy" : "idle",
                    });
                    addLog({
                        timestamp: data.timestamp || new Date().toISOString(),
                        agent: data.agent,
                        level: data.status === "failed" ? "error" : "info",
                        message: data.message,
                        taskId: data.task_id,
                    });
                    break;
                case "message":
                    addLog({
                        timestamp: new Date().toISOString(),
                        agent: data.agent_name || "Assistant",
                        level: "info",
                        message: data.content,
                    });
                    break;
                case "metrics":
                    break;
                case "error":
                    addLog({
                        timestamp: new Date().toISOString(),
                        agent: "System",
                        level: "error",
                        message: data.message,
                    });
                    break;
            }
        },
        [addLog, updateAgent]
    );

    const sendCommand = useCallback((text: string) => {
        if (ws.current?.readyState === WebSocket.OPEN) {
            ws.current.send(
                JSON.stringify({
                    type: "command",
                    id: crypto.randomUUID(),
                    text,
                    timestamp: new Date().toISOString(),
                })
            );
            addLog({
                timestamp: new Date().toISOString(),
                agent: "System",
                level: "info",
                message: `>>> ${text}`,
            });
        }
    }, [addLog]);

    return { isConnected, sendCommand };
}
