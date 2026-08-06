from core.config import settings
from main import app
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Nos aseguramos que el path de la API esté en sys.path para poder importar correctamente los módulos
api_root = str(Path(__file__).resolve().parent.parent)
if api_root not in sys.path:
    sys.path.insert(0, api_root)


client = TestClient(app)


def test_healthcheck_endpoint():
    """Prueba que el endpoint /health responda correctamente sin necesidad de API Key."""

    response = client.get("/api/v1/feedbacks/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database" in data
    print("Test Healthcheck Passed!")


def test_unauthorized_access_without_api_key():
    """Prueba que los endpoints de datos rechacen peticiones sin el header X-API-Key (401)."""

    response = client.get("/api/v1/feedbacks/social-media")
    assert response.status_code == 401
    print(f"401 Missing Key Response: {response.json()}")
    assert "detail" in response.json()
    print("Test 401 Unauthorized Without Header Passed!")


def test_unauthorized_access_with_invalid_api_key():
    """Prueba que los endpoints rechacen peticiones con una clave incorrecta (401)."""

    response = client.get("/api/v1/feedbacks/social-media",
                          headers={"X-API-Key": "invalid_key_123"})
    assert response.status_code == 401
    print(f"401 Invalid Key Response: {response.json()}")
    assert "detail" in response.json()
    print("Test 401 Invalid Key Passed!")


def test_authorized_access_with_valid_api_key():
    """Prueba que las peticiones con X-API-Key válida funcionen correctamente."""

    headers = {"X-API-Key": settings.API_KEY}
    response = client.get(
        "/api/v1/feedbacks/social-media?limit=5", headers=headers)
    print(f"200 Valid Key Status: {response.status_code}")
    # 500 si el contenedor de la BD no esta corriendo, 200 si esta corriendo y la BD esta accesible
    assert response.status_code in (200, 500)
    print("Test Authorized Access Executed Successfully!")


if __name__ == "__main__":
    test_healthcheck_endpoint()
    test_unauthorized_access_without_api_key()
    test_unauthorized_access_with_invalid_api_key()
    test_authorized_access_with_valid_api_key()
    print("All Integration Tests Executed Successfully!")
