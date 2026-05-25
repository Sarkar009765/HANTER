from fastapi import APIRouter, HTTPException, Query
from typing import Optional

router = APIRouter()


@router.get("/search")
async def search_memory(q: str = Query(...), limit: Optional[int] = Query(5)):
    return {
        "query": q,
        "results": [],
        "total": 0
    }


@router.delete("/{memory_id}")
async def delete_memory(memory_id: str):
    return {"status": "deleted", "memory_id": memory_id}
