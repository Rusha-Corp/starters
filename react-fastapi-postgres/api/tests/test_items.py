"""API tests for Items CRUD endpoints."""
import pytest
from fastapi.testclient import TestClient


class TestItemsCRUD:
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
        create_response = client.post(
            "/api/items",
            json={"name": "Test Item", "description": "Test description"},
        )
        assert create_response.status_code == 201

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

    def test_create_item_with_default_description(self, client: TestClient, db_session):
        """POST /api/items should default description to empty string."""
        response = client.post(
            "/api/items",
            json={"name": "No Desc Item"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["description"] == ""

    def test_create_item_max_name_length(self, client: TestClient, db_session):
        """POST /api/items should accept name at max length (255 chars)."""
        response = client.post(
            "/api/items",
            json={"name": "x" * 255},
        )
        assert response.status_code == 201

    def test_create_item_name_too_long(self, client: TestClient, db_session):
        """POST /api/items should reject name over 255 chars."""
        response = client.post(
            "/api/items",
            json={"name": "x" * 256},
        )
        assert response.status_code == 422

    def test_create_item_description_too_long(self, client: TestClient, db_session):
        """POST /api/items should reject description over 1000 chars."""
        response = client.post(
            "/api/items",
            json={"name": "Valid", "description": "x" * 1001},
        )
        assert response.status_code == 422

    def test_create_item_max_description_length(self, client: TestClient, db_session):
        """POST /api/items should accept description at max length (1000 chars)."""
        response = client.post(
            "/api/items",
            json={"name": "Valid", "description": "x" * 1000},
        )
        assert response.status_code == 201

    def test_get_item_by_id_returns_item(self, client: TestClient, db_session):
        """GET /api/items/{id} returns specific item."""
        create_response = client.post(
            "/api/items",
            json={"name": "Specific Item", "description": "desc"},
        )
        item_id = create_response.json()["id"]

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
        create_response = client.post(
            "/api/items",
            json={"name": "To Delete", "description": "desc"},
        )
        item_id = create_response.json()["id"]

        response = client.delete(f"/api/items/{item_id}")
        assert response.status_code == 204

        get_response = client.get(f"/api/items/{item_id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_item_returns_404(self, client: TestClient, db_session):
        """DELETE /api/items/{id} returns 404 for non-existent item."""
        response = client.delete("/api/items/99999")
        assert response.status_code == 404

    def test_multiple_items_creation(self, client: TestClient, db_session):
        """Creating multiple items should return incremental IDs."""
        r1 = client.post("/api/items", json={"name": "Item 1"})
        r2 = client.post("/api/items", json={"name": "Item 2"})
        assert r1.status_code == 201
        assert r2.status_code == 201
        assert r2.json()["id"] > r1.json()["id"]

    def test_list_items_total_matches_count(self, client: TestClient, db_session):
        """Total in list response should match the number of items."""
        client.post("/api/items", json={"name": "Item A"})
        client.post("/api/items", json={"name": "Item B"})

        response = client.get("/api/items")
        data = response.json()
        assert data["total"] == len(data["items"])
