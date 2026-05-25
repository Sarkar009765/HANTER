---
sidebar_position: 3
---

# Architecture

HANTER uses a hybrid local/cloud architecture optimized for 2GB RAM.

## System Design

```
┌─────────────────────────────────────┐
│         Tauri Desktop UI            │
│    (Rust + React, ~150MB RAM)       │
├─────────────────────────────────────┤
│         Python Agent Core            │
│    (FastAPI, ~300MB RAM)            │
├─────────────────────────────────────┤
│    SQLite + ChromaDB (Local DB)      │
│    (~100MB RAM)                     │
├─────────────────────────────────────┤
│    Skills (Lazy Loaded, ~200MB)      │
└─────────────────────────────────────┘
```

## Key Components

### Orchestrator Engine
The brain of HANTER. Receives user input, classifies intent, decomposes into tasks, selects agents, and merges results.

### Agent System
Five specialized agents:
- **DevAgent**: Code generation, debugging, deployment
- **SocialAgent**: Social media management
- **WebAgent**: Web scraping and research
- **FileAgent**: File organization
- **SysAgent**: System automation

### Skill System
Skills provide capabilities to agents. They are lazy-loaded and auto-unloaded when idle to save RAM.
