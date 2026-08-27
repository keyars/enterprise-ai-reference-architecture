# AI Gateway

## Decision

The application communicates with models through a provider-neutral `AIGateway` rather than importing a vendor SDK throughout the business logic.

```text
Application
    |
    v
 AIGateway
    |
    v
ModelProvider interface
    |
 +--+----------------+
 |                   |
LocalEcho        OpenAI adapter
provider         (next milestone)
```

## Why

Direct model-provider calls scattered through an enterprise codebase create coupling to vendor-specific request formats, error models and configuration. A gateway creates a stable application boundary and lets provider adapters evolve independently.

## Current implementation

V0.2 includes a deterministic local provider. It intentionally requires no API key and is suitable for unit tests and architecture validation.

The next provider implementation will add a real OpenAI adapter while preserving the same application-facing contract.

## Contract

`GenerationRequest` contains messages and model-generation controls. `GenerationResponse` normalizes provider, model, token and latency metadata where available.

The gateway is asynchronous and validates that at least one message is supplied before delegating to the configured provider.

## Non-goals

The gateway is not an agent orchestrator, RAG engine or prompt-management system. Those capabilities will sit above or beside this boundary in later milestones.
