export interface Message {
    id?: string;
    role: "user" | "assistant" | "system" | "agent";
    content: string;
    agent_name?: string;
    timestamp: string;
}

export interface LogEntry {
    timestamp: string;
    agent: string;
    level: "info" | "success" | "warning" | "error";
    message: string;
    taskId?: string;
}
