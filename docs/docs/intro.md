---
sidebar_position: 1
---

# HANTER Introduction

**HANTER (Bro's Reliable Operator)** is a multi-agent AI framework that operates as a digital twin for users. It combines a lightweight desktop UI with a Python-based agent orchestration engine.

## Features

- **Multi-Agent Swarm**: Five specialized agents working together
- **2GB RAM Optimized**: Runs on low-end PCs through lazy loading
- **Local-First Privacy**: Your data stays on your machine
- **Cyberpunk Dashboard**: Futuristic UI with real-time neural visualization
- **Free Forever**: MIT Licensed, no subscriptions
- **Skill Marketplace**: Community-driven plugin ecosystem

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Sarkar009765/HANTER.git
cd HANTER

# Run setup
./scripts/setup.sh  # Linux/Mac
scripts\setup.bat   # Windows

# Start development
./scripts/dev.sh    # Linux/Mac
scripts\dev.bat     # Windows
```

## Architecture Overview

HANTER uses a hybrid architecture:
- **Tauri Desktop App** (React + Rust): ~150MB RAM
- **Python Agent Core** (FastAPI): ~300MB RAM
- **SQLite + ChromaDB**: ~100MB RAM
- **Skills (Lazy Loaded)**: Max 2 active at ~200MB total
