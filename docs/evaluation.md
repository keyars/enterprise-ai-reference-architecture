# AI Evaluation

The repository contains deterministic evaluation primitives for regression testing without requiring an LLM API key.

An evaluation case defines a question and expected answer evidence. The evaluator reports matched and missing evidence and can be composed into a suite.

## What this does not claim

Substring-based evaluation is intentionally simple. It is useful for deterministic contract/regression checks, but it is not a complete semantic quality evaluator. Production evaluation should add curated datasets, groundedness checks, retrieval metrics, judge-model evaluation with calibration, and human review.
