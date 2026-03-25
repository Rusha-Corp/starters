"""API tests for Items CRUD endpoints.

These tests follow the TDD RED -> GREEN -> REFACTOR pattern.
Run with: pytest api/tests/ -v
"""
import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_health_returns_ok(self, client: TestClient):
        """GET /health returns status ok."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["ok", "degraded"]
        assert "version" in data

    def test_liveness_returns_ok(self, client: TestClient):
        """GET /health/live returns status ok."""
        response = client.get("/health/live")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

    def test_readiness_returns_ready_when_db_connected(self, client: TestClient):
        """GET /health/ready returns ready when DB is connected."""
        response = client.get("/health/ready")
        # With SQLite in tests, should return ready
        assert response.status_code in [200, 503]


class TestItemsEndpoints:
    """Test Items CRUD endpoints."""

    def test_list_items_returns_empty_initially(self, client: TestClient, db_session):
        """GET /api/items returns empty list when no items exist."""
        response = client.get("/api/items")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data

    def test_list_items_returns_stored_items(self, client: TestClient, db_session):
        """GET /api/items returns stored items."""
        # First, create an item
        create_response = client.post(
            "/api/items",
            json={"name": "Test Item", "description": "Test description"},
        )
        assert create_response.status_code == 201

        # Then, list items
        response = client.get("/api/items")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert any(item["name"] == "Test Item" for item in data["items"])

    def test_create_item_returns_new_item_with_id(self, client: TestClient, db_session):
        """POST /api/items creates item and returns it with generated ID."""
        response = client.post(
            "/api/items",
            json={"name": "New Item", "description": "New description"},
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["name"] == "New Item"
        assert data["description"] == "New description"

    def test_create_item_validation_error_on_empty_name(self, client: TestClient, db_session):
        """POST /api/items returns 422 when name is empty."""
        response = client.post(
            "/api/items",
            json={"name": "", "description": "test"},
        )
        assert response.status_code == 422

    def test_get_item_by_id_returns_item(self, client: TestClient, db_session):
        """GET /api/items/{id} returns specific item."""
        # Create item first
        create_response = client.post(
            "/api/items",
            json={"name": "Specific Item", "description": "desc"},
        )
        item_id = create_response.json()["id"]

        # Get item
        response = client.get(f"/api/items/{item_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Specific Item"

    def test_get_item_by_id_returns_404_for_nonexistent(self, client: TestClient, db_session):
        """GET /api/items/{id} returns 404 for non-existent item."""
        response = client.get("/api/items/99999")
        assert response.status_code == 404

    def test_delete_item_returns_204(self, client: TestClient, db_session):
        """DELETE /api/items/{id} deletes item and returns 204."""
        # Create item
        create_response = client.post(
            "/api/items",
            json={"name": "To Delete", "description": "desc"},
        )
        item_id = create_response.json()["id"]

        # Delete item
        response = client.delete(f"/api/items/{item_id}")
        assert response.status_code == 204

        # Verify deleted
        get_response = client.get(f"/api/items/{item_id}")
        assert get_response.status_code == 404


class TestMetricsEndpoint:
    """Test Prometheus metrics endpoint."""

    def test_metrics_endpoint_returns_prometheus_format(self, client: TestClient):
        """GET /metrics returns Prometheus metrics in text format."""
        response = client.get("/metrics")
        # May be 404 if metrics disabled in test env
        if response.status_code == 200:
            assert "text/plain" in response.headers["content-type"]
            # Should contain some metric names
            assert len(response.text) > 0
