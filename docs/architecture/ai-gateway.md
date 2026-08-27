# AI Gateway

The AI Gateway is the provider-neutral boundary between application services and model providers.

## Contract

`ModelProvider` defines the asynchronous `generate()` operation. Providers return the common `GenerationResponse` contract, which keeps provider-specific SDK response shapes out of the application layer.

## Current provider

V0.2 includes a deterministic local provider so the architecture and tests can run without credentials or network access.

## Next provider

V0.3 will add a real OpenAI adapter behind the same interface. Provider credentials will remain environment-only and will never be committed to source control.

## Why this boundary matters

The gateway provides a stable place for model routing, timeout policy, retries, usage accounting, observability and provider failover as the platform evolves.
