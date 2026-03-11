import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.settings import Settings, settings


def test_health_check(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_security_headers(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["content-security-policy"] == "default-src 'none'"
    assert response.headers["referrer-policy"] == "strict-origin-when-cross-origin"
    # X-XSS-Protection is intentionally absent: it is deprecated (removed in
    # Chrome ≥78, never supported in Firefox) and can introduce vulnerabilities
    # in old IE/Edge. Content-Security-Policy is the modern replacement.
    assert "x-xss-protection" not in response.headers


def test_request_id_generated_when_absent(client: TestClient) -> None:
    """A request without X-Request-ID must receive a freshly generated UUID."""
    response = client.get("/api/v1/health")
    assert "x-request-id" in response.headers
    # Basic UUID v4 shape check
    request_id = response.headers["x-request-id"]
    assert len(request_id) == 36  # xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx


def test_request_id_propagated_when_present(client: TestClient) -> None:
    """A supplied X-Request-ID must be echoed back unchanged."""
    custom_id = "my-trace-id-123"
    response = client.get("/api/v1/health", headers={"X-Request-ID": custom_id})
    assert response.headers["x-request-id"] == custom_id


def test_docs_available_in_development(client: TestClient) -> None:
    """Swagger UI should be reachable in non-production environments."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema(client: TestClient) -> None:
    """OpenAPI schema title must match the configured app_name."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json()["info"]["title"] == settings.app_name


def test_unknown_route_returns_404(client: TestClient) -> None:
    response = client.get("/does-not-exist")
    assert response.status_code == 404


@pytest.mark.parametrize("log_level", ["TRACE", "DEBUG"])
def test_verbose_log_level_forbidden_in_production(log_level: str) -> None:
    """Production must reject TRACE and DEBUG log levels."""
    with pytest.raises(ValidationError, match="is not permitted when ENVIRONMENT=production"):
        Settings(environment="production", log_level=log_level)


def test_wildcard_allowed_hosts_forbidden_in_production() -> None:
    """Production must reject the catch-all wildcard for allowed_hosts."""
    with pytest.raises(ValidationError, match="is not permitted when ENVIRONMENT=production"):
        Settings(environment="production", allowed_hosts=["*"])


@pytest.mark.parametrize(("log_level", "expected_debug"), [("TRACE", True), ("DEBUG", True), ("INFO", False)])
def test_debug_derived_from_log_level(log_level: str, expected_debug: bool) -> None:
    """debug is True only when log_level is TRACE or DEBUG."""
    s = Settings(log_level=log_level)
    assert s.debug is expected_debug
