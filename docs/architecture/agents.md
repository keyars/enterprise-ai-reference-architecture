# Agent Runtime Architecture

## Scope

V0.6 implements a bounded agent runtime around native function calling. It does not persist agent state and it does not grant arbitrary tool access.

## Execution boundary

```text
AgentRuntime
    |
    +--> ToolCallingProvider
    |       |
    |       +--> OpenAI Responses API
    |
    +--> ToolRegistry
            |
            +--> ToolDefinition
            +--> Authorization allowlist
            +--> Handler
```

## Tool authorization

A tool must satisfy both conditions before execution:

1. It is registered in `ToolRegistry`.
2. Its name appears in the request's `allowed_tools` list.

The model cannot expand the allowlist itself.

## Bounded execution

Each request has a `max_steps` limit. The runtime stops with an error when the model continues requesting tools beyond that limit.

Tool output is also bounded before it is returned to the model, preventing an individual tool from injecting unbounded response content into the next model turn.

## Native provider integration

The OpenAI provider uses the Responses API function-tool mechanism. The provider converts repository-level `ToolDefinition` objects into provider tool schemas, parses returned function calls, and sends `function_call_output` items back on the next model turn.

## Current limitations

- No persistent agent state
- No long-term memory
- No authentication or user identity boundary
- No per-tenant tool policy
- No tool sandboxing
- No tool-specific rate limits
- No production migration system

These are intentionally separate milestones rather than being implied by the current runtime.
