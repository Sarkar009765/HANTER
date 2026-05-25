export interface Agent {
    name: string;
    description: string;
    version: string;
    status: "idle" | "standby" | "busy" | "error" | "loading";
    ram_budget_mb: number;
    current_task?: string;
    skills_loaded: string[];
}

export interface AgentStatus {
    name: string;
    status: Agent["status"];
    progress: number;
}

export interface AgentConnection {
    from: string;
    to: string;
    strength: number;
}
