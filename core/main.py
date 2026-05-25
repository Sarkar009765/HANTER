import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.websocket import router as ws_router
from api.routes.agents import router as agents_router
from api.routes.tasks import router as tasks_router
from api.routes.memory import router as memory_router
from api.routes.system import router as system_router
from engine.orchestrator import Orchestrator
from memory.manager import MemoryManager
from utils.logger import setup_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    app.state.orchestrator = Orchestrator()
    app.state.memory = MemoryManager()
    await app.state.memory.initialize()
    yield
    await app.state.memory.close()

app = FastAPI(
    title="HANTER Core",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "tauri://localhost", "http://localhost:1420"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ws_router, prefix="/ws")
app.include_router(agents_router, prefix="/api/v1/agents")
app.include_router(tasks_router, prefix="/api/v1/tasks")
app.include_router(memory_router, prefix="/api/v1/memory")
app.include_router(system_router, prefix="/api/v1/system")

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
