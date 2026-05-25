import { useAgentStore } from "../stores/useAgentStore";
import type { Agent } from "../types/agent";

export function useAgentStatus() {
    const agents = useAgentStore((s) => s.agents);

    const getAgentColor = (status: Agent["status"]): string => {
        switch (status) {
            case "busy":
                return "#ff006e";
            case "idle":
                return "#00f0ff";
            case "standby":
                return "#f0a000";
            case "error":
                return "#ff3333";
            case "loading":
                return "#a855f7";
            default:
                return "#5a5a6a";
        }
    };

    return { agents, getAgentColor };
}
