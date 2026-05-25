import { useCallback } from "react";

export function useVoiceCommand() {
    const isSupported = "SpeechRecognition" in window || "webkitSpeechRecognition" in window;

    const startListening = useCallback((): Promise<string> => {
        return new Promise((resolve, reject) => {
            if (!isSupported) {
                reject(new Error("Speech recognition not supported"));
                return;
            }
            const SpeechRecognition =
                (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
            const recognition = new SpeechRecognition();
            recognition.lang = "en-US";
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;

            recognition.onresult = (event: any) => {
                resolve(event.results[0][0].transcript);
            };
            recognition.onerror = (event: any) => {
                reject(new Error(`Speech recognition error: ${event.error}`));
            };
            recognition.start();
        });
    }, [isSupported]);

    return { isSupported, startListening };
}
