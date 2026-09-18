

from fastapi.testclient import TestClient
from app.main import app

def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

def test_predict():
    with TestClient(app) as client:
        response = client.post("/predict", json={"text":"This movie is excellent."})
        assert response.status_code == 200
        body = response.json()
        assert "prediction" in body
        assert "confidence" in body

def test_missing_text():
    with TestClient(app) as client:
        response = client.post("/predict", json={})
        assert response.status_code == 422

def test_wrong_type():
    with TestClient(app) as client:
        response = client.post("/predict", json={"text":123})
        assert response.status_code == 422

def test_empty_text():
    with TestClient(app) as client:
        response = client.post("/predict", json={"text":""})
        assert response.status_code == 422

def test_whitespace_text():
    with TestClient(app) as client:
        response = client.post("/predict", json={"text":"     "})
        assert response.status_code == 400

