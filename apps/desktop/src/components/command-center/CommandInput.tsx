import { useState, useRef, useEffect } from "react";
import { useWebSocket } from "../../hooks/useWebSocket";
import { useAppStore } from "../../stores/useAppStore";
import { LiveLogStream } from "./LiveLogStream";
import { Send, Mic, MicOff } from "lucide-react";

export function CommandCenter() {
    const [input, setInput] = useState("");
    const [isRecording, setIsRecording] = useState(false);
    const inputRef = useRef<HTMLInputElement>(null);
    const { sendCommand, isConnected } = useWebSocket("default");
    const setProcessing = useAppStore((s) => s.setProcessing);

    useEffect(() => {
        inputRef.current?.focus();
    }, []);

    const handleSubmit = () => {
        const text = input.trim();
        if (!text) return;
        sendCommand(text);
        setInput("");
        setProcessing(true);
        setTimeout(() => setProcessing(false), 2000);
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    };

    const toggleVoice = async () => {
        if (isRecording) {
            setIsRecording(false);
            return;
        }
        try {
            setIsRecording(true);
            const SpeechRecognition =
                (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
            if (SpeechRecognition) {
                const recognition = new SpeechRecognition();
                recognition.lang = "en-US";
                recognition.onresult = (event: any) => {
                    setInput(event.results[0][0].transcript);
                    setIsRecording(false);
                };
                recognition.onerror = () => setIsRecording(false);
                recognition.start();
            }
        } catch {
            setIsRecording(false);
        }
    };

    return (
        <div className="bg-bg-secondary/80 border-t border-border-subtle">
            <div className="flex items-center gap-2 px-4 py-2">
                <div className="flex-1 relative">
                    <input
                        ref={inputRef}
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Ask Bro anything..."
                        disabled={!isConnected}
                        className="w-full h-10 bg-black/30 border border-accent-cyan/30 rounded-full px-4 pr-20 text-sm text-text-primary placeholder-text-muted outline-none focus:border-accent-cyan focus:shadow-glow-cyan transition-all"
                    />
                    <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
                        <button
                            onClick={toggleVoice}
                            className={`p-1.5 rounded-full transition-colors ${
                                isRecording
                                    ? "text-accent-red bg-accent-red/10 animate-pulse"
                                    : "text-text-muted hover:text-text-primary"
                            }`}
                        >
                            {isRecording ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
                        </button>
                        <button
                            onClick={handleSubmit}
                            disabled={!input.trim() || !isConnected}
                            className="p-1.5 rounded-full text-text-muted hover:text-accent-cyan disabled:opacity-30 transition-colors"
                        >
                            <Send className="w-4 h-4" />
                        </button>
                    </div>
                </div>
            </div>
            <div className="h-32 overflow-y-auto border-t border-border-subtle">
                <LiveLogStream />
            </div>
        </div>
    );
}
