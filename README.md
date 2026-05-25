# HANTER 🤖

**Bro's Reliable Operator** — Personal Multi-Agent AI Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/Sarkar009765/HANTER/actions/workflows/ci.yml/badge.svg)](https://github.com/Sarkar009765/HANTER/actions/workflows/ci.yml)

HANTER is a multi-agent AI framework that operates as a digital twin for users. It combines a lightweight Tauri desktop UI with a Python-based agent orchestration engine, optimized to run on 2GB RAM PCs.

## Features

- 🧠 **Multi-Agent Swarm** — 5 specialized agents with human-like reasoning
- 💻 **2GB RAM Optimized** — Lazy loading, compressed embeddings, auto-unloading
- 🎨 **Cyberpunk Dashboard** — 3D neural visualizer, live log stream, voice commands
- 🔒 **Local-First** — Your data stays on your machine, optional cloud fallback
- 🛠️ **Skill System** — Modular plugins loaded on demand
- 🚀 **Real Operations** — Actual file ops, git, deployment (not mocked)

## Quick Start

```bash
git clone https://github.com/Sarkar009765/HANTER.git
cd hanter

# Windows
scripts\setup.bat
scripts\dev.bat

# Linux/Mac
chmod +x scripts/*.sh
./scripts/setup.sh
./scripts/dev.sh
```

## Architecture

```
┌─────────────────────┐     ┌─────────────────────┐
│  Tauri Desktop UI   │◄───►│  Python Agent Core   │
│  (Rust + React)     │  WS │  (FastAPI + Python)  │
│  ~150MB RAM         │     │  ~300MB RAM          │
└─────────────────────┘     └─────────────────────┘
                                    │
                          ┌─────────▼─────────┐
                          │  SQLite + ChromaDB  │
                          │  ~100MB RAM         │
                          └───────────────────┘
```

## Agents

| Agent | Description | RAM |
|-------|-------------|-----|
| DevAgent | Code generation, debug, deploy | 100MB |
| SocialAgent | Social media management | 80MB |
| WebAgent | Web scraping, research | 60MB |
| FileAgent | File organization | 40MB |
| SysAgent | System automation | 50MB |

## Tech Stack

**Frontend:** Tauri v2 + React 19 + TypeScript + Tailwind CSS + Three.js
**Backend:** Python 3.11+ + FastAPI + WebSocket + SQLAlchemy + ChromaDB
**AI:** LiteLLM (Groq/Together) + Sentence Transformers + Ollama
**Build:** Vite + tauri-bundler + GitHub Actions

## License

MIT — Free Forever
