---
sidebar_position: 7
---

# API Reference

## WebSocket API

**Endpoint:** `ws://localhost:8000/ws/{session_id}`

### Client Messages

```json
{
    "type": "command",
    "id": "uuid",
    "text": "Deploy my app",
    "timestamp": "2026-01-01T00:00:00Z"
}
```

### Server Messages

```json
{
    "type": "message",
    "role": "assistant",
    "content": "Deploying your app...",
    "task_id": "uuid"
}
```

## REST API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/agents` | List agents |
| GET | `/api/v1/system/metrics` | System metrics |
| GET | `/api/v1/memory/search` | Search memory |
