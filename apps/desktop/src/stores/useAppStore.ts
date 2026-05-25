import { create } from "zustand";
import { persist } from "zustand/middleware";

interface AppState {
    theme: "dark" | "cyberpunk";
    sidebarOpen: boolean;
    activeTab: string;
    isProcessing: boolean;
    emergencyMode: boolean;

    setTheme: (theme: "dark" | "cyberpunk") => void;
    toggleSidebar: () => void;
    setActiveTab: (tab: string) => void;
    setProcessing: (processing: boolean) => void;
    setEmergencyMode: (emergency: boolean) => void;
}

export const useAppStore = create<AppState>()(
    persist(
        (set) => ({
            theme: "cyberpunk",
            sidebarOpen: true,
            activeTab: "dashboard",
            isProcessing: false,
            emergencyMode: false,

            setTheme: (theme) => set({ theme }),
            toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
            setActiveTab: (tab) => set({ activeTab: tab }),
            setProcessing: (processing) => set({ isProcessing: processing }),
            setEmergencyMode: (emergency) => set({ emergencyMode: emergency }),
        }),
        {
            name: "HANTER-app-storage",
            partialize: (state) => ({
                theme: state.theme,
                sidebarOpen: state.sidebarOpen,
            }),
        }
    )
);
