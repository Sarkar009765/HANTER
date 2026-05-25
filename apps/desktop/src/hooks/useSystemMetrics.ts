import { useState, useEffect } from "react";
import type { SystemMetrics } from "../types/system";

export function useSystemMetrics() {
    const [metrics, setMetrics] = useState<SystemMetrics>({
        ram_used_mb: 0,
        ram_total_mb: 0,
        cpu_percent: 0,
        active_agents: [],
        loaded_skills: [],
        queue_length: 0,
    });

    useEffect(() => {
        const interval = setInterval(async () => {
            try {
                const response = await fetch("http://localhost:8000/api/v1/system/metrics");
                const data = await response.json();
                setMetrics(data);
            } catch {
                // Backend not available yet
            }
        }, 5000);

        return () => clearInterval(interval);
    }, []);

    return metrics;
}
