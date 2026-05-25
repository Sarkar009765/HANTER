interface SuggestionChipsProps {
    suggestions: string[];
    onSelect: (text: string) => void;
}

export function SuggestionChips({ suggestions, onSelect }: SuggestionChipsProps) {
    return (
        <div className="flex flex-wrap gap-2 px-4 pb-2">
            {suggestions.map((suggestion, i) => (
                <button
                    key={i}
                    onClick={() => onSelect(suggestion)}
                    className="px-3 py-1 text-xs rounded-full bg-bg-tertiary border border-border-subtle text-text-muted hover:border-accent-cyan/30 hover:text-accent-cyan transition-all"
                >
                    {suggestion}
                </button>
            ))}
        </div>
    );
}
