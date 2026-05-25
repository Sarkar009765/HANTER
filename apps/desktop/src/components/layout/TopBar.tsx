import { useAppStore } from "../../stores/useAppStore";
import { useSystemMetrics } from "../../hooks/useSystemMetrics";
import { WifiOff, Wifi, Menu } from "lucide-react";
import { useWebSocket } from "../../hooks/useWebSocket";

export function TopBar() {
    const toggleSidebar = useAppStore((s) => s.toggleSidebar);
    const isProcessing = useAppStore((s) => s.isProcessing);
    const metrics = useSystemMetrics();
    const sessionId = "default";
    const { isConnected } = useWebSocket(sessionId);

    return (
        <header className="h-12 border-b border-border-subtle flex items-center justify-between px-4 bg-bg-secondary/50">
            <div className="flex items-center gap-3">
                <button
                    onClick={toggleSidebar}
                    className="p-1 rounded hover:bg-bg-tertiary text-text-secondary"
                >
                    <Menu className="w-4 h-4" />
                </button>
                <span className="text-sm text-text-muted">
                    RAM: {metrics.ram_used_mb.toFixed(0)}MB / {metrics.ram_total_mb.toFixed(0)}MB
                </span>
            </div>
            <div className="flex items-center gap-4">
                {isProcessing && (
                    <span className="text-xs text-accent-yellow animate-pulse">Processing...</span>
                )}
                <div className="flex items-center gap-1.5 text-xs">
                    {isConnected ? (
                        <>
                            <Wifi className="w-3 h-3 text-accent-green" />
                            <span className="text-accent-green">Online</span>
                        </>
                    ) : (
                        <>
                            <WifiOff className="w-3 h-3 text-accent-red" />
                            <span className="text-accent-red">Offline</span>
                        </>
                    )}
                </div>
            </div>
        </header>
    );
}
