"""AI generation API endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.ai.gateway import AIGateway
from app.ai.models import GenerationRequest
from app.ai.providers import LocalEchoProvider

router = APIRouter(prefix="/ai", tags=["AI"])
gateway = AIGateway(LocalEchoProvider())


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=20_000)
    model: str | None = None
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)


class GenerateResponse(BaseModel):
    text: str
    model: str
    provider: str


@router.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest) -> GenerateResponse:
    """Generate a response through the provider-neutral AI gateway."""
    result = await gateway.generate(
        GenerationRequest(
            messages=[{"role": "user", "content": request.prompt}],
            model=request.model,
            temperature=request.temperature,
        )
    )
    return GenerateResponse(text=result.text, model=result.model, provider=result.provider)
