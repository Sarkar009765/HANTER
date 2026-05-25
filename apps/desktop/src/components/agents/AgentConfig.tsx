interface AgentConfigProps {
    agentName: string;
    onSave?: (config: Record<string, unknown>) => void;
}

export function AgentConfig({ agentName, onSave }: AgentConfigProps) {
    return (
        <div className="rounded-lg bg-bg-secondary border border-border-subtle p-4">
            <h3 className="text-sm font-semibold capitalize mb-4">{agentName.replace("_", " ")} Configuration</h3>
            <p className="text-sm text-text-muted">Agent configuration UI coming soon.</p>
        </div>
    );
}
