"""
tests/unit/test_api_reference.py – Unit tests for the reference API endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.enums import RelativeFrame, RelativeModelMode

client = TestClient(app)


class TestReferenceEndpoints:
    def test_get_frames_status(self) -> None:
        response = client.get("/api/v1/reference/frames")
        assert response.status_code == 200

    def test_get_frames_content(self) -> None:
        response = client.get("/api/v1/reference/frames")
        data = response.json()
        assert "inertial_frames" in data
        assert "ECI_J2000" in data["inertial_frames"]
        assert "relative_frames" in data
        for frame in RelativeFrame:
            assert frame.value in data["relative_frames"]

    def test_get_models_status(self) -> None:
        response = client.get("/api/v1/reference/models")
        assert response.status_code == 200

    def test_get_models_content(self) -> None:
        response = client.get("/api/v1/reference/models")
        data = response.json()
        assert "relative_models" in data
        assert "default_relative_model" in data
        assert data["default_relative_model"] == RelativeModelMode.KGD_QNS_J2.value

    def test_health_check(self) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
