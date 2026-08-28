from importlib.metadata import version

from app.main import app


def test_release_contract_version_is_consistent() -> None:
    assert app.version == version("enterprise-ai-reference-architecture")
    assert app.version == "0.7.0"
