export interface Task {
    id: string;
    agent: string;
    description: string;
    status: "pending" | "running" | "completed" | "failed" | "cancelled";
    progress: number;
    dependencies: string[];
    priority: number;
    error_message?: string;
}

export interface TaskPlan {
    plan_id: string;
    tasks: Task[];
    estimated_time_seconds: number;
}
