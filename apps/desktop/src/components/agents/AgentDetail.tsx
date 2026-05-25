import type { Agent } from "../../types/agent";

interface AgentDetailProps {
    agent: Agent;
}

export function AgentDetail({ agent }: AgentDetailProps) {
    return (
        <div className="rounded-lg bg-bg-secondary border border-border-subtle p-4">
            <h3 className="text-lg font-semibold capitalize mb-2">{agent.name.replace("_", " ")}</h3>
            <p className="text-sm text-text-secondary mb-4">{agent.description}</p>
            <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                    <span className="text-text-muted">Status: </span>
                    <span className="text-accent-cyan capitalize">{agent.status}</span>
                </div>
                <div>
                    <span className="text-text-muted">RAM Budget: </span>
                    <span>{agent.ram_budget_mb}MB</span>
                </div>
                <div>
                    <span className="text-text-muted">Version: </span>
                    <span>{agent.version}</span>
                </div>
            </div>
        </div>
    );
}
