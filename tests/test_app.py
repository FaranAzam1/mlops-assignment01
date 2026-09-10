import json
import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "healthy"
    assert data["application"] == "student-ml-api"
    assert "version" in data


def test_predict_success(client):
    response = client.post(
        "/predict",
        data=json.dumps({"value": 10}),
        content_type="application/json"
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["input"] == 10
    assert data["prediction"] == 20


def test_predict_missing_input(client):
    response = client.post(
        "/predict",
        data=json.dumps({}),
        content_type="application/json"
    )
    data = response.get_json()

    assert response.status_code == 400
    assert "error" in data


def test_predict_invalid_input(client):
    response = client.post(
        "/predict",
        data=json.dumps({"value": "not-a-number"}),
        content_type="application/json"
    )
    data = response.get_json()

    assert response.status_code == 400
    assert "error" in data
