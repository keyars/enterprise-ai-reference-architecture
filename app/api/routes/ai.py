from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.gateway import AIGateway
from app.ai.models import GenerationRequest, GenerationResponse
from app.ai.providers.local import LocalProvider

router = APIRouter(prefix="/ai", tags=["AI"])
_gateway = AIGateway(provider=LocalProvider())


class GenerateBody(BaseModel):
    prompt: str
    model: str | None = None
    temperature: float = 0.2
    max_tokens: int | None = None


@router.post("/generate", response_model=GenerationResponse)
async def generate(body: GenerateBody) -> GenerationResponse:
    request = GenerationRequest(
        prompt=body.prompt,
        model=body.model,
        temperature=body.temperature,
        max_tokens=body.max_tokens,
    )
    return await _gateway.generate(request)
