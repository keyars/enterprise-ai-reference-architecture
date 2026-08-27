"""Agent runtime API endpoints."""

from fastapi import APIRouter, HTTPException

from app.agents.default_tools import build_default_tool_registry
from app.agents.runtime import AgentRuntime
from app.ai.models import AgentRequest, AgentResponse
from app.ai.providers.openai import OpenAIProvider
from app.ai.tools import ToolArgumentError, ToolAuthorizationError, ToolNotFoundError
from app.core.config import settings

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.post("/run", response_model=AgentResponse)
async def run_agent(request: AgentRequest) -> AgentResponse:
    """Run a bounded agent using native OpenAI tool calling when configured."""
    if not settings.openai_api_key:
        raise HTTPException(
            status_code=501,
            detail="Agent runtime requires OPENAI_API_KEY for native tool calling",
        )

    runtime = AgentRuntime(
        provider=OpenAIProvider(
            api_key=settings.openai_api_key,
            default_model=settings.openai_model,
            timeout=settings.openai_timeout_seconds,
        ),
        tools=build_default_tool_registry(),
    )
    try:
        return await runtime.run(request)
    except ToolAuthorizationError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except (ToolArgumentError, ToolNotFoundError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
