from importlib.metadata import version

from app.main import app


def test_package_and_api_versions_match() -> None:
    assert version("enterprise-ai-reference-architecture") == app.version
