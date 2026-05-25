import { Sidebar } from "./Sidebar";
import { TopBar } from "./TopBar";
import { useAppStore } from "../../stores/useAppStore";
import { CommandCenter } from "../command-center/CommandInput";
import { NeuralGraph } from "../dashboard/NeuralGraph";
import { AgentStatusGrid } from "../dashboard/AgentStatusGrid";
import { TaskQueue } from "../dashboard/TaskQueue";
import { SystemMetrics as SysMetrics } from "../dashboard/SystemMetrics";
import { RecentActivity } from "../dashboard/RecentActivity";

export function MainLayout() {
    const activeTab = useAppStore((s) => s.activeTab);

    return (
        <div className="flex h-screen w-screen bg-bg-primary text-text-primary overflow-hidden">
            <Sidebar />
            <div className="flex-1 flex flex-col overflow-hidden">
                <TopBar />
                <main className="flex-1 overflow-auto p-4 space-y-4">
                    {activeTab === "dashboard" && (
                        <>
                            <div className="h-64 rounded-lg bg-bg-secondary border border-border-subtle overflow-hidden">
                                <NeuralGraph />
                            </div>
                            <div className="grid grid-cols-3 gap-4">
                                <div className="rounded-lg bg-bg-secondary border border-border-subtle p-4">
                                    <h3 className="text-sm font-medium text-text-secondary mb-3">Active Tasks</h3>
                                    <div className="space-y-2 text-sm">
                                        <div className="flex items-center gap-2">
                                            <div className="w-full bg-bg-tertiary rounded-full h-2">
                                                <div className="bg-accent-cyan h-2 rounded-full" style={{ width: "67%" }} />
                                            </div>
                                            <span className="text-text-muted w-10 text-right">67%</span>
                                        </div>
                                        <p className="text-text-muted text-xs">Deploy API</p>
                                    </div>
                                </div>
                                <div className="rounded-lg bg-bg-secondary border border-border-subtle p-4">
                                    <h3 className="text-sm font-medium text-text-secondary mb-3">Agents Status</h3>
                                    {["DevAgent", "SocialAgent", "WebAgent"].map((name) => (
                                        <div key={name} className="flex items-center gap-2 text-sm py-1">
                                            <span className="w-2 h-2 rounded-full bg-accent-green" />
                                            <span className="text-text-secondary">{name}</span>
                                        </div>
                                    ))}
                                </div>
                                <div className="rounded-lg bg-bg-secondary border border-border-subtle p-4">
                                    <h3 className="text-sm font-medium text-text-secondary mb-3">Web Monitor</h3>
                                    <div className="text-sm text-text-muted space-y-1">
                                        <div className="flex justify-between">
                                            <span>github.com</span>
                                            <span className="text-accent-green">200ms</span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span>vercel.com</span>
                                            <span className="text-accent-cyan">150ms</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </>
                    )}
                    {activeTab === "agents" && <div className="text-text-muted">Agent management view</div>}
                    {activeTab === "memory" && <div className="text-text-muted">Memory search view</div>}
                    {activeTab === "config" && <div className="text-text-muted">Configuration view</div>}
                </main>
                <div className="border-t border-border-subtle">
                    <CommandCenter />
                </div>
            </div>
        </div>
    );
}
