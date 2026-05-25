import { useLogStore } from "../stores/useLogStore";

export function useMemory() {
    const logs = useLogStore((s) => s.logs);

    const searchHistory = (query: string) => {
        return logs.filter(
            (log) =>
                log.message.toLowerCase().includes(query.toLowerCase()) ||
                log.agent.toLowerCase().includes(query.toLowerCase())
        );
    };

    return { searchHistory };
}
