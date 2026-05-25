import { create } from "zustand";
import type { Task } from "../types/task";

interface TaskState {
    tasks: Task[];
    addTask: (task: Task) => void;
    updateTask: (id: string, update: Partial<Task>) => void;
    removeTask: (id: string) => void;
    clearCompleted: () => void;
}

export const useTaskStore = create<TaskState>((set) => ({
    tasks: [],
    addTask: (task) => set((state) => ({ tasks: [...state.tasks, task] })),
    updateTask: (id, update) =>
        set((state) => ({
            tasks: state.tasks.map((t) => (t.id === id ? { ...t, ...update } : t)),
        })),
    removeTask: (id) =>
        set((state) => ({ tasks: state.tasks.filter((t) => t.id !== id) })),
    clearCompleted: () =>
        set((state) => ({ tasks: state.tasks.filter((t) => t.status !== "completed") })),
}));
