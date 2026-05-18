"""API tests for health check endpoints."""
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient


class TestLivenessEndpoint:
    """Test GET /health/live endpoint."""

    def test_liveness_returns_ok(self, client: TestClient):
        """Liveness probe should return 200 with status ok."""
        response = client.get("/health/live")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data

    def test_liveness_response_structure(self, client: TestClient):
        """Liveness response should have required fields."""
        response = client.get("/health/live")
        data = response.json()
        assert "status" in data
        assert "version" in data


class TestReadinessEndpoint:
    """Test GET /health/ready endpoint."""

    def test_readiness_returns_ready_when_db_connected(self, client: TestClient):
        """Readiness probe should return 200 when DB is reachable."""
        response = client.get("/health/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert data["db"] == "connected"

    def test_readiness_returns_503_when_db_unreachable(self, client: TestClient):
        """Readiness probe should return 503 when DB is unreachable."""
        with patch("main.check_db_connection", return_value=False):
            response = client.get("/health/ready")
            assert response.status_code == 503
            data = response.json()
            assert data["detail"]["status"] == "not_ready"
            assert data["detail"]["db"] == "unreachable"


class TestCombinedHealthEndpoint:
    """Test GET /health endpoint."""

    def test_health_returns_ok_when_db_connected(self, client: TestClient):
        """Combined health should return ok when DB is connected."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["ok", "degraded"]
        assert "version" in data
        assert "db" in data

    def test_health_returns_degraded_when_db_down(self, client: TestClient):
        """Combined health should return degraded when DB is down."""
        with patch("main.check_db_connection", return_value=False):
            response = client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "degraded"
            assert data["db"] == "unreachable"


class TestMetricsEndpoint:
    """Test GET /metrics endpoint."""

    def test_metrics_returns_prometheus_format(self, client: TestClient):
        """Metrics endpoint should return Prometheus text format."""
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]
        assert len(response.text) > 0
        # Should contain at least one metric name
        assert "http_" in response.text

    def test_metrics_disabled_returns_404(self, client: TestClient):
        """Metrics endpoint should return 404 when disabled."""
        from config import Settings

        original = Settings.model_fields["metrics_enabled"].default
        with patch("main.settings.metrics_enabled", False):
            response = client.get("/metrics")
            assert response.status_code == 404
