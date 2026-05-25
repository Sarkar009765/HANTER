import { useTaskStore } from "../../stores/useTaskStore";
import { ProgressRing } from "../ui/ProgressRing";

export function TaskQueue() {
    const tasks = useTaskStore((s) => s.tasks);

    return (
        <div className="space-y-2">
            {tasks.length === 0 && (
                <p className="text-xs text-text-muted italic">No active tasks</p>
            )}
            {tasks.map((task) => (
                <div key={task.id} className="flex items-center gap-3 py-1">
                    <ProgressRing progress={task.progress} size={32} strokeWidth={3} color="#00f0ff" />
                    <div className="flex-1 min-w-0">
                        <p className="text-xs text-text-secondary truncate">{task.description}</p>
                        <p className="text-xs text-text-muted">{task.agent}</p>
                    </div>
                    <span
                        className={`text-xs px-1.5 py-0.5 rounded ${
                            task.status === "running"
                                ? "bg-accent-cyan/10 text-accent-cyan"
                                : task.status === "completed"
                                  ? "bg-accent-green/10 text-accent-green"
                                  : task.status === "failed"
                                    ? "bg-accent-red/10 text-accent-red"
                                    : "bg-text-muted/10 text-text-muted"
                        }`}
                    >
                        {task.status}
                    </span>
                </div>
            ))}
        </div>
    );
}
