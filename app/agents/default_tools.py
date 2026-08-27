from typing import Any

from app.ai.models import ToolDefinition
from app.ai.tools import ToolRegistry


async def add_numbers(arguments: dict[str, Any]) -> str:
    left = arguments.get("left")
    right = arguments.get("right")
    if not isinstance(left, (int, float)) or isinstance(left, bool):
        raise TypeError("left must be a number")
    if not isinstance(right, (int, float)) or isinstance(right, bool):
        raise TypeError("right must be a number")
    return str(left + right)


def build_default_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(
        ToolDefinition(
            name="add_numbers",
            description="Add two numbers and return the numeric result.",
            parameters={
                "type": "object",
                "properties": {
                    "left": {"type": "number"},
                    "right": {"type": "number"},
                },
                "required": ["left", "right"],
                "additionalProperties": False,
            },
        ),
        add_numbers,
    )
    return registry
