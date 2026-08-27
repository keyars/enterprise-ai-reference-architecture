"""AI generation API endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.ai.gateway import AIGateway
from app.ai.models import GenerationRequest, GenerationResponse
from app.ai.providers.local import LocalProvider
from app.ai.providers.openai import OpenAIProvider
from app.core.config import settings

router = APIRouter(prefix="/ai", tags=["AI"])


def create_gateway() -> AIGateway:
    """Build the configured provider without exposing provider details to callers."""
    if settings.openai_api_key:
        return AIGateway(
            OpenAIProvider(
                api_key=settings.openai_api_key,
                default_model=settings.openai_model,
                timeout=settings.openai_timeout_seconds,
            )
        )
    return AIGateway(LocalProvider())


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=20_000)
    model: str | None = None
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=None, ge=1, le=32_000)


@router.post("/generate", response_model=GenerationResponse)
async def generate(request: GenerateRequest) -> GenerationResponse:
    """Generate through OpenAI when configured, otherwise use the local provider."""
    try:
        gateway = create_gateway()
        return await gateway.generate(GenerationRequest(**request.model_dump()))
    except Exception as exc:
        raise HTTPException(status_code=502, detail="AI provider request failed") from exc
