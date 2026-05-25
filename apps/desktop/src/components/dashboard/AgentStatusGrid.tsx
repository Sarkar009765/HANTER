import { useAgentStore } from "../../stores/useAgentStore";
import { AgentCard } from "./AgentCard";

export function AgentStatusGrid() {
    const agents = useAgentStore((s) => s.agents);

    return (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
            {agents.map((agent) => (
                <AgentCard key={agent.name} agent={agent} />
            ))}
        </div>
    );
}
