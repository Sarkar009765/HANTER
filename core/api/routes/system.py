from fastapi import APIRouter
import psutil
import platform

router = APIRouter()


@router.get("/metrics")
async def get_system_metrics():
    proc = psutil.Process()
    mem = proc.memory_info()
    return {
        "ram_used_mb": round(mem.rss / 1024 / 1024, 1),
        "ram_total_mb": round(psutil.virtual_memory().total / 1024 / 1024, 1),
        "ram_percent": psutil.virtual_memory().percent,
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "cpu_count": psutil.cpu_count(),
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "process_uptime_seconds": int(proc.create_time())
    }


@router.get("/logs")
async def get_system_logs():
    return {"logs": []}


@router.post("/shutdown")
async def shutdown():
    return {"status": "shutting_down"}
