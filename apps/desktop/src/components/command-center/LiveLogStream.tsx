import { useEffect, useRef } from "react";
import { useLogStore } from "../../stores/useLogStore";
import { LOG_LEVEL_COLORS } from "../../utils/constants";

export function LiveLogStream() {
    const logs = useLogStore((s) => s.logs);
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (containerRef.current) {
            containerRef.current.scrollTop = containerRef.current.scrollHeight;
        }
    }, [logs]);

    return (
        <div
            ref={containerRef}
            className="h-full overflow-y-auto p-2 font-mono text-xs space-y-0.5"
        >
            {logs.length === 0 && (
                <div className="text-text-muted italic p-2">Waiting for activity...</div>
            )}
            {logs.map((log, i) => (
                <div key={i} className="flex gap-2">
                    <span className="text-text-muted shrink-0 w-16">
                        {new Date(log.timestamp).toLocaleTimeString("en-US", { hour12: false })}
                    </span>
                    <span
                        className="shrink-0 font-semibold"
                        style={{ color: LOG_LEVEL_COLORS[log.level] || "#a0a0b0" }}
                    >
                        [{log.agent}]
                    </span>
                    <span className="text-text-secondary truncate">{log.message}</span>
                </div>
            ))}
        </div>
    );
}
