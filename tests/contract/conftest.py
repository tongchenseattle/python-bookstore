import pytest


@pytest.fixture
def correlation_headers() -> dict[str, str]:
    return {"X-Correlation-ID": "test-correlation-id"}
