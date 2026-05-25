import type { ReactNode } from "react";

interface GlassCardProps {
    children: ReactNode;
    title?: string;
    accentColor?: string;
    height?: string;
    padding?: string;
    glow?: boolean;
}

export function GlassCard({
    children,
    title,
    accentColor = "#00f0ff",
    height = "auto",
    padding = "16px",
    glow = true,
}: GlassCardProps) {
    return (
        <div
            className="rounded-xl border border-white/10"
            style={{
                background: "rgba(255, 255, 255, 0.03)",
                backdropFilter: "blur(10px)",
                WebkitBackdropFilter: "blur(10px)",
                height,
                padding,
                boxShadow: glow ? `0 0 20px ${accentColor}33` : undefined,
            }}
        >
            {title && (
                <h3 className="text-sm font-medium text-text-secondary mb-3" style={{ color: accentColor }}>
                    {title}
                </h3>
            )}
            {children}
        </div>
    );
}
