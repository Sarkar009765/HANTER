import type { Agent } from "../../types/agent";
import { useAgentStore } from "../../stores/useAgentStore";
import { Cpu, Wifi, WifiOff } from "lucide-react";

export function AgentCard({ agent }: { agent: Agent }) {
    const statusColors: Record<string, string> = {
        idle: "bg-accent-cyan",
        busy: "bg-accent-pink",
        standby: "bg-accent-yellow",
        error: "bg-accent-red",
        loading: "bg-accent-green",
    };

    return (
        <div className="rounded-lg bg-bg-secondary border border-border-subtle p-3 hover:border-accent-cyan/30 transition-all">
            <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                    <Cpu className="w-4 h-4 text-accent-cyan" />
                    <span className="text-sm font-medium capitalize">{agent.name.replace("_", " ")}</span>
                </div>
                <div className="flex items-center gap-1.5">
                    <span className={`w-2 h-2 rounded-full ${statusColors[agent.status]} ${agent.status === "busy" ? "animate-pulse" : ""}`} />
                    <span className="text-xs text-text-muted">{agent.status}</span>
                </div>
            </div>
            <p className="text-xs text-text-muted mb-2 truncate">{agent.description}</p>
            <div className="flex items-center justify-between text-xs text-text-muted">
                <span>{agent.ram_budget_mb}MB RAM</span>
                <span>
                    {agent.status === "busy" ? (
                        <span className="flex items-center gap-1 text-accent-cyan">
                            <Wifi className="w-3 h-3" /> Active
                        </span>
                    ) : (
                        <span className="flex items-center gap-1">
                            <WifiOff className="w-3 h-3" /> Standby
                        </span>
                    )}
                </span>
            </div>
        </div>
    );
}
