from collections.abc import Awaitable, Callable
from typing import Any

from app.ai.models import ToolDefinition

ToolHandler = Callable[[dict[str, Any]], Awaitable[str]]


class ToolNotFoundError(Exception):
    pass


class ToolAuthorizationError(Exception):
    pass


class ToolArgumentError(Exception):
    pass


class ToolRegistry:
    """Explicit registry for tools that an agent is permitted to execute."""

    def __init__(self) -> None:
        self._handlers: dict[str, tuple[ToolDefinition, ToolHandler]] = {}

    def register(self, definition: ToolDefinition, handler: ToolHandler) -> None:
        if definition.name in self._handlers:
            raise ValueError(f"Tool already registered: {definition.name}")
        self._handlers[definition.name] = (definition, handler)

    def definitions(self, allowed_tools: set[str]) -> list[ToolDefinition]:
        return [
            definition
            for name, (definition, _) in self._handlers.items()
            if name in allowed_tools
        ]

    async def execute(
        self,
        name: str,
        arguments: dict[str, Any],
        allowed_tools: set[str],
    ) -> str:
        if name not in allowed_tools:
            raise ToolAuthorizationError(f"Tool is not authorized: {name}")
        registered = self._handlers.get(name)
        if registered is None:
            raise ToolNotFoundError(f"Tool is not registered: {name}")
        definition, handler = registered
        _validate_arguments(definition.parameters, arguments)
        return await handler(arguments)


def _validate_arguments(schema: dict[str, Any], arguments: dict[str, Any]) -> None:
    if schema.get("type") not in (None, "object"):
        raise ToolArgumentError("Tool parameter schema must describe an object")

    properties = schema.get("properties", {})
    required = schema.get("required", [])
    missing = [name for name in required if name not in arguments]
    if missing:
        raise ToolArgumentError(f"Missing required tool arguments: {', '.join(missing)}")

    if schema.get("additionalProperties") is False:
        unknown = [name for name in arguments if name not in properties]
        if unknown:
            raise ToolArgumentError(f"Unknown tool arguments: {', '.join(unknown)}")

    for name, value in arguments.items():
        expected = properties.get(name, {}).get("type")
        if expected and not _matches_type(value, expected):
            raise ToolArgumentError(f"Invalid type for tool argument: {name}")


def _matches_type(value: Any, expected: str) -> bool:
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    return True
