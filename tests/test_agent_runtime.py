from app.agents.runtime import AgentRuntime
from app.ai.models import (
    AgentRequest,
    GenerationRequest,
    GenerationResponse,
    ToolCall,
    ToolCallingResponse,
    ToolDefinition,
)
from app.ai.providers.base import ToolCallingProvider
from app.ai.tools import ToolArgumentError, ToolAuthorizationError, ToolRegistry


class FakeProvider(ToolCallingProvider):
    name = "fake"

    def __init__(self) -> None:
        self.calls = 0

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        raise NotImplementedError

    async def generate_with_tools(self, request):
        self.calls += 1
        if self.calls == 1:
            return ToolCallingResponse(
                text="",
                provider=self.name,
                model="fake-model",
                tool_calls=[
                    ToolCall(call_id="call-1", name="add", arguments={"left": 2, "right": 3})
                ],
                output_items=[
                    {
                        "type": "function_call",
                        "call_id": "call-1",
                        "name": "add",
                        "arguments": '{"left":2,"right":3}',
                    }
                ],
            )
        return ToolCallingResponse(
            text="The answer is 5.",
            provider=self.name,
            model="fake-model",
        )


async def add(arguments: dict) -> str:
    return str(arguments["left"] + arguments["right"])


def add_definition() -> ToolDefinition:
    return ToolDefinition(
        name="add",
        description="Add two numbers.",
        parameters={
            "type": "object",
            "properties": {
                "left": {"type": "number"},
                "right": {"type": "number"},
            },
            "required": ["left", "right"],
            "additionalProperties": False,
        },
    )


async def test_agent_executes_authorized_tool_then_finishes() -> None:
    registry = ToolRegistry()
    registry.register(add_definition(), add)

    response = await AgentRuntime(FakeProvider(), registry).run(
        AgentRequest(prompt="Calculate 2 + 3", allowed_tools=["add"])
    )

    assert response.answer == "The answer is 5."
    assert response.steps == 2
    assert response.trace[0].tool == "add"
    assert response.trace[0].output == "5"


async def test_agent_rejects_unauthorized_tool() -> None:
    registry = ToolRegistry()
    registry.register(add_definition(), add)

    try:
        await registry.execute("add", {"left": 1, "right": 2}, set())
    except ToolAuthorizationError:
        pass
    else:
        raise AssertionError("Unauthorized tool execution must fail")


async def test_tool_arguments_are_validated_before_execution() -> None:
    registry = ToolRegistry()
    registry.register(add_definition(), add)

    try:
        await registry.execute("add", {"left": "not-a-number", "right": 2}, {"add"})
    except ToolArgumentError:
        pass
    else:
        raise AssertionError("Invalid tool arguments must fail validation")
