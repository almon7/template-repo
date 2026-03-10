from fastapi.testclient import TestClient

from app.settings import settings


def test_health_check(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_security_headers(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["x-xss-protection"] == "1; mode=block"
    assert response.headers["referrer-policy"] == "strict-origin-when-cross-origin"


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
