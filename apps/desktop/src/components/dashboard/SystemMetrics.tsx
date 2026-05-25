import { useSystemMetrics } from "../../hooks/useSystemMetrics";

export function SystemMetrics() {
    const metrics = useSystemMetrics();

    return (
        <div className="grid grid-cols-3 gap-3">
            <div className="text-center">
                <div className="text-lg font-bold text-accent-cyan">
                    {metrics.ram_used_mb.toFixed(0)}
                    <span className="text-xs text-text-muted">MB</span>
                </div>
                <p className="text-xs text-text-muted">RAM Used</p>
            </div>
            <div className="text-center">
                <div className="text-lg font-bold text-accent-pink">
                    {metrics.cpu_percent.toFixed(0)}
                    <span className="text-xs text-text-muted">%</span>
                </div>
                <p className="text-xs text-text-muted">CPU</p>
            </div>
            <div className="text-center">
                <div className="text-lg font-bold text-accent-green">
                    {metrics.queue_length}
                </div>
                <p className="text-xs text-text-muted">Queue</p>
            </div>
        </div>
    );
}
