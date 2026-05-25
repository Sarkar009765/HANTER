import { create } from "zustand";
import type { LogEntry } from "../types/message";

interface LogState {
    logs: LogEntry[];
    maxLogs: number;
    addLog: (entry: LogEntry) => void;
    clearLogs: () => void;
}

export const useLogStore = create<LogState>((set) => ({
    logs: [],
    maxLogs: 500,
    addLog: (entry) =>
        set((state) => ({
            logs: [...state.logs.slice(-(state.maxLogs - 1)), entry],
        })),
    clearLogs: () => set({ logs: [] }),
}));
