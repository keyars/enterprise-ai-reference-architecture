"""Deterministic evaluation primitives for RAG/AI regressions."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EvaluationCase:
    name: str
    question: str
    expected_substrings: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    name: str
    passed: bool
    matched: tuple[str, ...]
    missing: tuple[str, ...]

    @property
    def score(self) -> float:
        total = len(self.matched) + len(self.missing)
        return len(self.matched) / total if total else 1.0


def evaluate_answer(case: EvaluationCase, answer: str) -> EvaluationResult:
    normalized = answer.casefold()
    matched = tuple(item for item in case.expected_substrings if item.casefold() in normalized)
    missing = tuple(item for item in case.expected_substrings if item.casefold() not in normalized)
    return EvaluationResult(case.name, not missing, matched, missing)


def evaluate_suite(cases: list[EvaluationCase], answers: dict[str, str]) -> list[EvaluationResult]:
    return [evaluate_answer(case, answers.get(case.name, "")) for case in cases]


def suite_pass_rate(results: list[EvaluationResult]) -> float:
    if not results:
        return 1.0
    return sum(result.passed for result in results) / len(results)


DEFAULT_CASES = [
    EvaluationCase(
        "provider-neutrality",
        "What architectural principle keeps the application independent of an LLM vendor?",
        ("provider", "interface"),
    ),
    EvaluationCase(
        "bounded-agency",
        "How is agent autonomy constrained?",
        ("bounded", "tool"),
    ),
]
