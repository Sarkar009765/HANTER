from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
import json
import asyncio
import psutil
import time
from uuid import uuid4

from utils.logger import logger

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        logger.info("websocket_connected", session_id=session_id)

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            logger.info("websocket_disconnected", session_id=session_id)

    async def send_message(self, session_id: str, message: dict):
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_json(message)
            except Exception:
                self.disconnect(session_id)

    async def broadcast(self, message: dict):
        disconnected = []
        for sid, conn in self.active_connections.items():
            try:
                await conn.send_json(message)
            except Exception:
                disconnected.append(sid)
        for sid in disconnected:
            self.disconnect(sid)


manager = ConnectionManager()


@router.websocket("/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    orchestrator = websocket.app.state.orchestrator

    metrics_task = asyncio.create_task(send_metrics_periodic(session_id))

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            msg_type = message.get("type", "")

            if msg_type == "command":
                command_id = message.get("id", str(uuid4()))
                await manager.send_message(session_id, {
                    "type": "ack",
                    "command_id": command_id,
                    "status": "processing"
                })

                result = await orchestrator.process(
                    message.get("text", ""),
                    session_id
                )

                await manager.send_message(session_id, {
                    "type": "message",
                    "role": "assistant",
                    "content": result.response,
                    "task_id": command_id
                })

            elif msg_type == "agent_control":
                action = message.get("action")
                task_id = message.get("task_id")
                if action == "cancel":
                    await orchestrator.cancel_task(task_id)
                    await manager.send_message(session_id, {
                        "type": "task_update",
                        "task_id": task_id,
                        "status": "cancelled",
                        "message": "Task cancelled by user"
                    })

            elif msg_type == "skill":
                action = message.get("action")
                skill_name = message.get("skill_name")
                if action == "list":
                    skills = orchestrator.skill_registry.list_skills()
                    await manager.send_message(session_id, {
                        "type": "skill_list",
                        "skills": skills
                    })
                elif action == "load" and skill_name:
                    await orchestrator.skill_registry.get_skill(skill_name)
                    await manager.send_message(session_id, {
                        "type": "skill_loaded",
                        "skill_name": skill_name
                    })
                elif action == "unload" and skill_name:
                    await orchestrator.skill_registry.unload_skill(skill_name)
                    await manager.send_message(session_id, {
                        "type": "skill_unloaded",
                        "skill_name": skill_name
                    })

            elif msg_type == "memory_query":
                query = message.get("query", "")
                limit = message.get("limit", 5)
                results = await orchestrator.memory_manager.search(query, limit)
                await manager.send_message(session_id, {
                    "type": "memory_results",
                    "results": results
                })

            elif msg_type == "system_info":
                metrics = _get_system_metrics(orchestrator)
                await manager.send_message(session_id, {
                    "type": "metrics",
                    **metrics
                })

    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error("websocket_error", error=str(e))
        try:
            await manager.send_message(session_id, {
                "type": "error",
                "code": "INTERNAL_ERROR",
                "message": str(e),
                "recoverable": True
            })
        except Exception:
            pass
    finally:
        metrics_task.cancel()
        manager.disconnect(session_id)


async def send_metrics_periodic(session_id: str):
    try:
        while True:
            await asyncio.sleep(5)
            if session_id in manager.active_connections:
                proc = psutil.Process()
                mem = proc.memory_info()
                metrics = {
                    "type": "metrics",
                    "ram_used_mb": round(mem.rss / 1024 / 1024, 1),
                    "ram_total_mb": round(psutil.virtual_memory().total / 1024 / 1024, 1),
                    "cpu_percent": psutil.cpu_percent(interval=0.1),
                    "active_agents": [],
                    "loaded_skills": [],
                    "queue_length": 0
                }
                await manager.send_message(session_id, metrics)
    except asyncio.CancelledError:
        pass
    except Exception:
        pass


def _get_system_metrics(orchestrator) -> dict:
    proc = psutil.Process()
    mem = proc.memory_info()
    return {
        "ram_used_mb": round(mem.rss / 1024 / 1024, 1),
        "ram_total_mb": round(psutil.virtual_memory().total / 1024 / 1024, 1),
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "active_agents": [],
        "loaded_skills": [],
        "queue_length": 0
    }
