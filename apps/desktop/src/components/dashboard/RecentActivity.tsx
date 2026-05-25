import { useLogStore } from "../../stores/useLogStore";

export function RecentActivity() {
    const logs = useLogStore((s) => s.logs);
    const recent = logs.slice(-5).reverse();

    return (
        <div className="space-y-1">
            {recent.length === 0 && (
                <p className="text-xs text-text-muted italic">No recent activity</p>
            )}
            {recent.map((log, i) => (
                <div key={i} className="flex gap-2 text-xs">
                    <span className="text-text-muted shrink-0">
                        {new Date(log.timestamp).toLocaleTimeString("en-US", { hour12: false })}
                    </span>
                    <span className="text-accent-cyan shrink-0">[{log.agent}]</span>
                    <span className="text-text-muted truncate">{log.message}</span>
                </div>
            ))}
        </div>
    );
}
