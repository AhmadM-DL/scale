import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app import app

client = TestClient(app)

@patch("app.core_service")
@patch("app.APP_SECRET_KEY", "test_secret")
def test_post_endpoint_success(mock_core_service):
    response = client.post("/post", json={"secret_key": "test_secret"})
    assert response.status_code == 200
    mock_core_service.post_to_linkedin.assert_called_once()

@patch("app.APP_SECRET_KEY", "test_secret")
def test_post_endpoint_wrong_secret():
    response = client.post("/post", json={"secret_key": "wrong_secret"})
    assert response.status_code == 401

@patch("app.core_service")
@patch("app.APP_SECRET_KEY", "test_secret")
def test_post_endpoint_service_failure(mock_core_service):
    mock_core_service.post_to_linkedin.side_effect = Exception("Service Down")
    response = client.post("/post", json={"secret_key": "test_secret"})
    assert response.status_code == 500
