interface VoiceWaveProps {
    isActive: boolean;
}

export function VoiceWave({ isActive }: VoiceWaveProps) {
    if (!isActive) return null;

    return (
        <div className="flex items-center gap-0.5 h-6">
            {[1, 2, 3, 4, 5].map((i) => (
                <div
                    key={i}
                    className="w-0.5 bg-accent-cyan rounded-full animate-pulse"
                    style={{
                        height: `${Math.random() * 16 + 8}px`,
                        animationDelay: `${i * 0.1}s`,
                        opacity: 0.8,
                    }}
                />
            ))}
        </div>
    );
}
