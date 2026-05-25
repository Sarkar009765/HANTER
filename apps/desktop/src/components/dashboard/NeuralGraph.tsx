import { useAgentStore } from "../../stores/useAgentStore";
import type { AgentConnection } from "../../types/agent";

interface NeuralGraphProps {
    activityLevel?: number;
}

export function NeuralGraph({ activityLevel = 0.5 }: NeuralGraphProps) {
    const agents = useAgentStore((s) => s.agents);
    const connections = useAgentStore((s) => s.connections);

    const getAgentColor = (name: string) => {
        const agent = agents.find((a) => a.name === name);
        if (!agent) return "#4a4a5a";
        switch (agent.status) {
            case "busy":
                return "#ff006e";
            case "idle":
                return "#00f0ff";
            case "standby":
                return "#f0a000";
            default:
                return "#4a4a5a";
        }
    };

    const getAgentPulse = (name: string) => {
        const agent = agents.find((a) => a.name === name);
        return agent?.status === "busy" ? "animate-pulse" : "";
    };

    return (
        <div className="w-full h-full relative flex items-center justify-center">
            <svg viewBox="0 0 400 200" className="w-full h-full opacity-80">
                {connections.map((conn, i) => {
                    const nodes: Record<string, { x: number; y: number }> = {
                        dev_agent: { x: 60, y: 100 },
                        social_agent: { x: 160, y: 40 },
                        web_agent: { x: 160, y: 160 },
                        file_agent: { x: 280, y: 80 },
                        sys_agent: { x: 280, y: 160 },
                    };
                    const from = nodes[conn.from];
                    const to = nodes[conn.to];
                    if (!from || !to) return null;
                    return (
                        <line
                            key={i}
                            x1={from.x}
                            y1={from.y}
                            x2={to.x}
                            y2={to.y}
                            stroke={getAgentColor(conn.from)}
                            strokeWidth={1.5 * conn.strength}
                            opacity={0.4 * conn.strength}
                            className="transition-all duration-500"
                        />
                    );
                })}
                {agents.map((agent) => {
                    const positions: Record<string, { x: number; y: number }> = {
                        dev_agent: { x: 60, y: 100 },
                        social_agent: { x: 160, y: 40 },
                        web_agent: { x: 160, y: 160 },
                        file_agent: { x: 280, y: 80 },
                        sys_agent: { x: 280, y: 160 },
                    };
                    const pos = positions[agent.name];
                    if (!pos) return null;
                    return (
                        <g key={agent.name}>
                            <circle
                                cx={pos.x}
                                cy={pos.y}
                                r={12}
                                fill={getAgentColor(agent.name)}
                                opacity={0.3}
                                className={getAgentPulse(agent.name)}
                            />
                            <circle
                                cx={pos.x}
                                cy={pos.y}
                                r={8}
                                fill={getAgentColor(agent.name)}
                                className={getAgentPulse(agent.name)}
                            />
                            <text
                                x={pos.x}
                                y={pos.y + 25}
                                textAnchor="middle"
                                fill="white"
                                fontSize="10"
                                fontFamily="JetBrains Mono, monospace"
                                opacity={0.7}
                            >
                                {agent.name.replace("_", "")}
                            </text>
                        </g>
                    );
                })}
            </svg>
        </div>
    );
}
