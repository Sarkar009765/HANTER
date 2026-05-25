import type { ReactNode } from "react";

interface TerminalTextProps {
    children: ReactNode;
    color?: string;
}

export function TerminalText({ children, color = "#00ff88" }: TerminalTextProps) {
    return (
        <span className="font-mono text-xs" style={{ color }}>
            {children}
        </span>
    );
}
