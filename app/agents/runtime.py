from time import perf_counter
from typing import Any

from app.ai.models import AgentRequest, AgentResponse, AgentTraceEntry, ToolCall, ToolCallingRequest
from app.ai.providers.base import ToolCallingProvider
from app.ai.tools import ToolAuthorizationError, ToolNotFoundError, ToolRegistry


class AgentRuntime:
    """Bounded agent loop with explicit tool authorization."""

    def __init__(self, provider: ToolCallingProvider, tools: ToolRegistry) -> None:
        self.provider = provider
        self.tools = tools

    async def run(self, request: AgentRequest) -> AgentResponse:
        allowed = set(request.allowed_tools)
        definitions = self.tools.definitions(allowed)
        if not definitions and allowed:
            unknown = sorted(allowed)
            raise ToolNotFoundError(f"No registered tools found: {', '.join(unknown)}")

        conversation: list[dict[str, Any]] = [{"role": "user", "content": request.prompt}]
        trace: list[AgentTraceEntry] = []
        started = perf_counter()

        for step in range(1, request.max_steps + 1):
            response = await self.provider.generate_with_tools(
                ToolCallingRequest(
                    input=conversation,
                    tools=definitions,
                    model=request.model,
                    temperature=request.temperature,
                    max_tokens=request.max_tokens,
                )
            )

            conversation.extend(response.output_items)
            if not response.tool_calls:
                return AgentResponse(
                    answer=response.text,
                    provider=response.provider,
                    model=response.model,
                    steps=step,
                    trace=trace,
                )

            for call in response.tool_calls:
                output = await self._execute_call(call, allowed)
                trace.append(
                    AgentTraceEntry(
                        step=step,
                        tool=call.name,
                        call_id=call.call_id,
                        output=output,
                    )
                )
                conversation.append(
                    {
                        "type": "function_call_output",
                        "call_id": call.call_id,
                        "output": output,
                    }
                )

        elapsed_ms = round((perf_counter() - started) * 1000, 2)
        raise RuntimeError(
            f"Agent exceeded max_steps={request.max_steps} after {elapsed_ms} ms"
        )

    async def _execute_call(self, call: ToolCall, allowed: set[str]) -> str:
        try:
            output = await self.tools.execute(call.name, call.arguments, allowed)
        except (ToolAuthorizationError, ToolNotFoundError):
            raise
        except Exception as exc:
            output = f"Tool execution failed: {type(exc).__name__}"
        return _bounded_output(output)


def _bounded_output(output: str, limit: int = 10_000) -> str:
    if len(output) <= limit:
        return output
    return output[:limit] + "\n[tool output truncated]"
