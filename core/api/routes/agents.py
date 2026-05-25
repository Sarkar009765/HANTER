from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from agents.registry import AgentRegistry

router = APIRouter()


@router.get("")
async def list_agents():
    registry = AgentRegistry()
    return {
        "agents": [
            {
                "name": name,
                "description": agent_cls.description,
                "version": agent_cls.version,
                "status": "idle",
                "ram_budget_mb": agent_cls.ram_budget_mb
            }
            for name, agent_cls in registry._agents.items()
        ]
    }


@router.get("/{name}/status")
async def agent_status(name: str):
    registry = AgentRegistry()
    agent = registry._agents.get(name)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{name}' not found")
    return {
        "name": name,
        "status": "idle",
        "description": agent.description,
        "ram_budget_mb": agent.ram_budget_mb
    }


@router.post("/{name}/configure")
async def configure_agent(name: str, config: Dict[str, Any]):
    registry = AgentRegistry()
    agent = registry._agents.get(name)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{name}' not found")
    return {"status": "configured", "agent": name, "config": config}
