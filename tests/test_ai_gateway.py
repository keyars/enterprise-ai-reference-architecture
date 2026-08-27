import pytest

from app.ai.gateway import AIGateway
from app.ai.models import GenerationRequest
from app.ai.providers import LocalEchoProvider


@pytest.mark.anyio
async def test_gateway_normalizes_provider_response() -> None:
    gateway = AIGateway(LocalEchoProvider())

    result = await gateway.generate(
        GenerationRequest(messages=[{"role": "user", "content": "Hello enterprise AI"}])
    )

    assert result.provider == "local-echo"
    assert result.model == "local-echo-v1"
    assert result.text == "Echo: Hello enterprise AI"


@pytest.mark.anyio
async def test_gateway_rejects_empty_messages() -> None:
    gateway = AIGateway(LocalEchoProvider())

    with pytest.raises(ValueError, match="At least one message"):
        await gateway.generate(GenerationRequest(messages=[]))
