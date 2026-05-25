export interface SystemMetrics {
    ram_used_mb: number;
    ram_total_mb: number;
    cpu_percent: number;
    active_agents: string[];
    loaded_skills: string[];
    queue_length: number;
}

export interface WSMessage {
    type: string;
    [key: string]: unknown;
}
