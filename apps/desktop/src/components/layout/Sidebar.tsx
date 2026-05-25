import { useAppStore } from "../../stores/useAppStore";
import { useAgentStore } from "../../stores/useAgentStore";
import { Brain, Cpu, MessageSquare, Database, Settings } from "lucide-react";

const navItems = [
    { id: "dashboard", label: "Dashboard", icon: Brain },
    { id: "agents", label: "Agents", icon: Cpu },
    { id: "memory", label: "Memory", icon: Database },
    { id: "config", label: "Config", icon: Settings },
];

export function Sidebar() {
    const activeTab = useAppStore((s) => s.activeTab);
    const setActiveTab = useAppStore((s) => s.setActiveTab);
    const sidebarOpen = useAppStore((s) => s.sidebarOpen);
    const agents = useAgentStore((s) => s.agents);

    if (!sidebarOpen) return null;

    return (
        <aside className="w-48 bg-bg-secondary border-r border-border-subtle flex flex-col h-full">
            <div className="p-4 border-b border-border-subtle">
                <div className="flex items-center gap-2">
                    <Brain className="w-6 h-6 text-accent-cyan" />
                    <span className="font-bold text-sm">HANTER</span>
                </div>
            </div>
            <nav className="flex-1 p-2 space-y-1">
                {navItems.map((item) => (
                    <button
                        key={item.id}
                        onClick={() => setActiveTab(item.id)}
                        className={`w-full flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors ${
                            activeTab === item.id
                                ? "bg-accent-cyan/10 text-accent-cyan border border-accent-cyan/30"
                                : "text-text-secondary hover:bg-bg-tertiary hover:text-text-primary"
                        }`}
                    >
                        <item.icon className="w-4 h-4" />
                        {item.label}
                    </button>
                ))}
            </nav>
            <div className="p-3 border-t border-border-subtle">
                <p className="text-xs text-text-muted mb-2">Active Agents</p>
                <div className="space-y-1">
                    {agents.slice(0, 3).map((agent) => (
                        <div key={agent.name} className="flex items-center gap-2 text-xs">
                            <span
                                className={`w-1.5 h-1.5 rounded-full ${
                                    agent.status === "busy"
                                        ? "bg-accent-pink animate-pulse"
                                        : agent.status === "idle"
                                          ? "bg-accent-cyan"
                                          : "bg-accent-yellow"
                                }`}
                            />
                            <span className="text-text-muted truncate">{agent.name.replace("_", " ")}</span>
                        </div>
                    ))}
                </div>
            </div>
        </aside>
    );
}
