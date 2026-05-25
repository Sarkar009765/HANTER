from fastapi import APIRouter, HTTPException
from typing import Dict, Any

router = APIRouter()

_tasks: Dict[str, Dict[str, Any]] = {}


@router.get("")
async def list_tasks():
    return {"tasks": list(_tasks.values())}


@router.get("/{task_id}")
async def get_task(task_id: str):
    task = _tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")
    return task


@router.post("/{task_id}/cancel")
async def cancel_task(task_id: str):
    task = _tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")
    task["status"] = "cancelled"
    return {"status": "cancelled", "task_id": task_id}
