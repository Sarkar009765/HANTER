import type { ReactNode } from "react";

interface NeonButtonProps {
    children: ReactNode;
    onClick?: () => void;
    color?: string;
    disabled?: boolean;
    size?: "sm" | "md" | "lg";
}

export function NeonButton({
    children,
    onClick,
    color = "#00f0ff",
    disabled = false,
    size = "md",
}: NeonButtonProps) {
    const sizeClasses = {
        sm: "px-3 py-1 text-xs",
        md: "px-4 py-2 text-sm",
        lg: "px-6 py-3 text-base",
    };

    return (
        <button
            onClick={onClick}
            disabled={disabled}
            className={`rounded-lg font-medium transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed ${sizeClasses[size]}`}
            style={{
                background: `${color}15`,
                border: `1px solid ${color}40`,
                color: color,
                boxShadow: `0 0 10px ${color}20`,
            }}
            onMouseEnter={(e) => {
                e.currentTarget.style.background = `${color}25`;
                e.currentTarget.style.boxShadow = `0 0 20px ${color}40`;
            }}
            onMouseLeave={(e) => {
                e.currentTarget.style.background = `${color}15`;
                e.currentTarget.style.boxShadow = `0 0 10px ${color}20`;
            }}
        >
            {children}
        </button>
    );
}
