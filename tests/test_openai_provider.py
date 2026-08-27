from unittest.mock import AsyncMock, Mock

import pytest

from app.ai.models import GenerationRequest, Usage
from app.ai.providers.openai import OpenAIProvider


@pytest.mark.asyncio
async def test_openai_provider_normalizes_response() -> None:
    provider = OpenAIProvider(api_key="test-key", default_model="gpt-test")
    response = Mock()
    response.output_text = "Hello from the model"
    response.usage.input_tokens = 12
    response.usage.output_tokens = 7
    response.usage.total_tokens = 19
    provider.client.responses.create = AsyncMock(return_value=response)

    result = await provider.generate(GenerationRequest(prompt="Hello"))

    assert result.provider == "openai"
    assert result.model == "gpt-test"
    assert result.text == "Hello from the model"
    assert result.usage == Usage(input_tokens=12, output_tokens=7, total_tokens=19)
