from __future__ import annotations

MODEL_CONFIG = {
    "primary": {
        "provider": "groq",
        "model": "llama-3.1-8b-instant",
        "max_tokens": 4096,
        "temperature": 0.7,
    },
    "fallback": {
        "provider": "together",
        "model": "qwen-2.5-7b-instruct",
        "max_tokens": 4096,
        "temperature": 0.7,
    },
    "local": {
        "provider": "ollama",
        "model": "tinyllama",
        "max_tokens": 2048,
        "temperature": 0.8,
    },
    "embeddings": {
        "model": "all-MiniLM-L6-v2",
        "dimension": 384,
    }
}
