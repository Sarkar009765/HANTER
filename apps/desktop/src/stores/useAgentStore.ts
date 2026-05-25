import { create } from "zustand";
import type { Agent, AgentStatus } from "../types/agent";

interface AgentState {
    agents: Agent[];
    connections: { from: string; to: string; strength: number }[];
    updateAgent: (name: string, update: Partial<Agent>) => void;
    setAgents: (agents: Agent[]) => void;
}

export const useAgentStore = create<AgentState>((set) => ({
    agents: [
        { name: "dev_agent", description: "Development Agent", version: "1.0.0", status: "idle", ram_budget_mb: 100, skills_loaded: [] },
        { name: "social_agent", description: "Social Media Agent", version: "1.0.0", status: "standby", ram_budget_mb: 80, skills_loaded: [] },
        { name: "web_agent", description: "Web Automation Agent", version: "1.0.0", status: "standby", ram_budget_mb: 60, skills_loaded: [] },
        { name: "file_agent", description: "File Management Agent", version: "1.0.0", status: "standby", ram_budget_mb: 40, skills_loaded: [] },
        { name: "sys_agent", description: "System Automation Agent", version: "1.0.0", status: "standby", ram_budget_mb: 50, skills_loaded: [] },
    ],
    connections: [
        { from: "dev_agent", to: "social_agent", strength: 0.6 },
        { from: "dev_agent", to: "web_agent", strength: 0.7 },
        { from: "social_agent", to: "web_agent", strength: 0.4 },
        { from: "file_agent", to: "sys_agent", strength: 0.5 },
    ],
    updateAgent: (name, update) =>
        set((state) => ({
            agents: state.agents.map((a) => (a.name === name ? { ...a, ...update } : a)),
        })),
    setAgents: (agents) => set({ agents }),
}));
