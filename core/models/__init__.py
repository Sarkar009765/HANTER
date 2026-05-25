from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum
from uuid import uuid4
from datetime import datetime


class TaskType(str, Enum):
    CODE = "code"
    SOCIAL = "social"
    WEB = "web"
    FILE = "file"
    SYSTEM = "system"
    GENERAL = "general"


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentStatus(str, Enum):
    IDLE = "idle"
    STANDBY = "standby"
    BUSY = "busy"
    ERROR = "error"
    LOADING = "loading"


class IntentType(str, Enum):
    CODE_GENERATION = "CODE_GENERATION"
    PROJECT_SCAFFOLD = "PROJECT_SCAFFOLD"
    DEPLOYMENT = "DEPLOYMENT"
    SOCIAL_MEDIA = "SOCIAL_MEDIA"
    WEB_RESEARCH = "WEB_RESEARCH"
    FILE_ORGANIZATION = "FILE_ORGANIZATION"
    SYSTEM_AUTOMATION = "SYSTEM_AUTOMATION"
    GENERAL_CHAT = "GENERAL_CHAT"
    CLARIFICATION_NEEDED = "CLARIFICATION_NEEDED"


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    AGENT = "agent"


class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: TaskType = TaskType.GENERAL
    description: str
    agent: Optional[str] = None
    dependencies: List[str] = Field(default_factory=list)
    priority: int = 5
    status: TaskStatus = TaskStatus.PENDING
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Optional[Dict[str, Any]] = None
    max_retries: int = 3
    timeout_seconds: int = 300
    ram_required_mb: int = 50
    error_message: Optional[str] = None


class TaskTree(BaseModel):
    tasks: List[Task]
    explanation: str


class IntentClassification(BaseModel):
    intent: IntentType
    confidence: float
    emotion: str = "neutral"
    entities: List[str] = Field(default_factory=list)
    clarifying_question: Optional[str] = None


class AgentMessage(BaseModel):
    from_agent: str
    to_agent: str
    message_type: str = "request"
    content: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    priority: int = 5


class AgentResult(BaseModel):
    success: bool = True
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None


class ExecutionResult(BaseModel):
    response: str
    tasks_completed: int = 0
    tasks_failed: int = 0
    total_time_ms: int = 0
    plan: Optional[TaskTree] = None


class SessionContext(BaseModel):
    session_id: str
    current_intent: Optional[str] = None
    active_agents: List[str] = Field(default_factory=list)
    loaded_skills: List[str] = Field(default_factory=list)
    conversation_buffer: List[Dict[str, str]] = Field(default_factory=list)
    context_variables: Dict[str, Any] = Field(default_factory=dict)


class MemoryDocument(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    embedding: Optional[List[float]] = None


class SystemMetrics(BaseModel):
    ram_used_mb: float = 0.0
    ram_total_mb: float = 0.0
    cpu_percent: float = 0.0
    active_agents: List[str] = Field(default_factory=list)
    loaded_skills: List[str] = Field(default_factory=list)
    queue_length: int = 0
