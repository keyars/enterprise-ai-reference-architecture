from typing import Any

from openai import AsyncOpenAI

from app.ai.models import (
    GenerationRequest,
    GenerationResponse,
    ToolCall,
    ToolCallingRequest,
    ToolCallingResponse,
    Usage,
)
from app.ai.providers.base import ToolCallingProvider


class OpenAIProvider(ToolCallingProvider):
    name = "openai"

    def __init__(self, api_key: str, default_model: str = "gpt-5.5", timeout: float = 30.0) -> None:
        self.default_model = default_model
        self.client = AsyncOpenAI(api_key=api_key, timeout=timeout)

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        model = request.model or self.default_model
        response = await self.client.responses.create(
            model=model,
            input=request.prompt,
            temperature=request.temperature,
            max_output_tokens=request.max_tokens,
        )
        usage = response.usage
        return GenerationResponse(
            text=response.output_text,
            provider=self.name,
            model=model,
            usage=Usage(
                input_tokens=getattr(usage, "input_tokens", 0) if usage else 0,
                output_tokens=getattr(usage, "output_tokens", 0) if usage else 0,
                total_tokens=getattr(usage, "total_tokens", 0) if usage else 0,
            ),
        )

    async def generate_with_tools(self, request: ToolCallingRequest) -> ToolCallingResponse:
        model = request.model or self.default_model
        response = await self.client.responses.create(
            model=model,
            input=request.input,
            tools=[tool.openai_schema() for tool in request.tools],
            temperature=request.temperature,
            max_output_tokens=request.max_tokens,
        )
        tool_calls = [
            ToolCall(
                call_id=item.call_id,
                name=item.name,
                arguments=_parse_arguments(item.arguments),
            )
            for item in response.output
            if getattr(item, "type", None) == "function_call"
        ]
        output_items = [_serialize_output_item(item) for item in response.output]
        usage = response.usage
        return ToolCallingResponse(
            text=response.output_text,
            provider=self.name,
            model=model,
            tool_calls=tool_calls,
            output_items=output_items,
            usage={
                "input_tokens": getattr(usage, "input_tokens", 0) if usage else 0,
                "output_tokens": getattr(usage, "output_tokens", 0) if usage else 0,
                "total_tokens": getattr(usage, "total_tokens", 0) if usage else 0,
            },
        )


def _parse_arguments(arguments: str) -> dict[str, Any]:
    import json

    parsed = json.loads(arguments)
    if not isinstance(parsed, dict):
        raise TypeError("Tool arguments must be a JSON object")
    return parsed


def _serialize_output_item(item: Any) -> dict[str, Any]:
    if hasattr(item, "model_dump"):
        return item.model_dump(mode="json", exclude_none=True)
    return dict(item)
