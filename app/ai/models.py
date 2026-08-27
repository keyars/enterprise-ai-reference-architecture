from typing import Any

from pydantic import BaseModel, Field


class ToolDefinition(BaseModel):
    name: str = Field(min_length=1, max_length=100, pattern=r"^[a-zA-Z0-9_-]+$")
    description: str = Field(min_length=1, max_length=2_000)
    parameters: dict[str, Any] = Field(default_factory=dict)

    def openai_schema(self) -> dict[str, Any]:
        return {
            "type": "function",
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "strict": True,
        }


class ToolCall(BaseModel):
    call_id: str
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class ToolCallingRequest(BaseModel):
    input: str | list[dict[str, Any]]
    tools: list[ToolDefinition] = Field(default_factory=list)
    model: str | None = None
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=None, ge=1, le=32_000)


class ToolCallingResponse(BaseModel):
    text: str
    provider: str
    model: str
    tool_calls: list[ToolCall] = Field(default_factory=list)
    output_items: list[dict[str, Any]] = Field(default_factory=list)
    usage: dict[str, int] = Field(default_factory=dict)


class AgentRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=20_000)
    model: str | None = None
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=None, ge=1, le=32_000)
    max_steps: int = Field(default=8, ge=1, le=20)
    allowed_tools: list[str] = Field(default_factory=list, max_length=50)


class AgentTraceEntry(BaseModel):
    step: int
    tool: str
    call_id: str
    output: str


class AgentResponse(BaseModel):
    answer: str
    provider: str
    model: str
    steps: int
    trace: list[AgentTraceEntry] = Field(default_factory=list)
