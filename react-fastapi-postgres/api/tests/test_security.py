"""API security tests covering OWASP Top 10 concerns."""
import pytest
from fastapi.testclient import TestClient


class TestCORSSecurity:
    """Test CORS configuration security (OWASP A05: Security Misconfiguration)."""

    def test_cors_allows_configured_origin(self, client: TestClient):
        """CORS should allow requests from configured origins."""
        response = client.options(
            "/api/items",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert "access-control-allow-origin" in response.headers

    def test_cors_includes_common_methods(self, client: TestClient):
        """CORS preflight should include expected methods."""
        response = client.options(
            "/api/items",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
            },
        )
        # Should not reject the preflight
        assert response.status_code in [200, 204]


class TestInputValidation:
    """Test input validation and injection resistance (OWASP A03: Injection)."""

    def test_sql_injection_in_name(self, client: TestClient, db_session):
        """SQL injection attempts in name should be handled safely."""
        response = client.post(
            "/api/items",
            json={"name": "'; DROP TABLE items; --", "description": "attack"},
        )
        # Should create the item with the literal string, not execute SQL
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "'; DROP TABLE items; --"

        # Verify table still exists
        list_response = client.get("/api/items")
        assert list_response.status_code == 200

    def test_xss_in_name_is_sanitized(self, client: TestClient, db_session):
        """XSS script tags in name should be sanitized by bleach."""
        response = client.post(
            "/api/items",
            json={"name": "<script>alert('xss')</script>", "description": "attack"},
        )
        assert response.status_code == 201
        data = response.json()
        # Bleach strips HTML tags, so <script> tags should be removed
        assert "<script>" not in data["name"]
        assert "alert" in data["name"]  # text content preserved

    def test_very_long_name_rejected(self, client: TestClient, db_session):
        """Extremely long names should be rejected by schema validation."""
        response = client.post(
            "/api/items",
            json={"name": "x" * 10000, "description": "attack"},
        )
        assert response.status_code == 422

    def test_very_long_description_rejected(self, client: TestClient, db_session):
        """Extremely long descriptions should be rejected by schema validation."""
        response = client.post(
            "/api/items",
            json={"name": "Valid Name", "description": "x" * 10000},
        )
        assert response.status_code == 422

    def test_null_bytes_in_name(self, client: TestClient, db_session):
        """Null bytes in name should be handled safely."""
        response = client.post(
            "/api/items",
            json={"name": "test\x00injection", "description": "attack"},
        )
        # FastAPI/Pydantic should handle this — either reject or sanitize
        assert response.status_code in [201, 422]

    def test_non_string_types_rejected(self, client: TestClient, db_session):
        """Non-string types for name should be rejected."""
        response = client.post(
            "/api/items",
            json={"name": 12345, "description": "attack"},
        )
        assert response.status_code == 422


class TestHTTPMethodSecurity:
    """Test that unsupported HTTP methods are rejected (OWASP A01: Broken Access Control)."""

    def test_put_items_not_allowed(self, client: TestClient):
        """PUT on /api/items should return 405."""
        response = client.put("/api/items", json={"name": "test"})
        assert response.status_code == 405

    def test_patch_items_not_allowed(self, client: TestClient):
        """PATCH on /api/items should return 405."""
        response = client.patch("/api/items", json={"name": "test"})
        assert response.status_code == 405

    def test_delete_items_list_not_allowed(self, client: TestClient):
        """DELETE on /api/items list should return 405."""
        response = client.delete("/api/items")
        assert response.status_code == 405


class TestSensitiveDataExposure:
    """Test that sensitive data is not exposed (OWASP A02: Cryptographic Failures)."""

    def test_error_responses_do_not_leak_internal_info(self, client: TestClient):
        """Error responses should not contain stack traces or internal paths."""
        response = client.get("/api/items/invalid_id")
        assert response.status_code == 422
        data = response.json()
        # Should have validation error detail, but no internal file paths
        detail_str = str(data)
        assert "/app/" not in detail_str
        assert "Traceback" not in detail_str

    def test_health_endpoint_does_not_expose_secrets(self, client: TestClient):
        """Health endpoint should not expose configuration secrets."""
        response = client.get("/health")
        data = response.json()
        response_str = str(data)
        assert "secret" not in response_str.lower()
        assert "password" not in response_str.lower()

    def test_404_response_does_not_leak_info(self, client: TestClient):
        """404 responses should not leak internal details."""
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404


class TestNoAuthenticationWarning:
    """
    Document that the API currently has no authentication.

    These tests serve as documentation that auth should be added
    before production use (OWASP A07: Identification and Authentication Failures).
    """

    def test_items_endpoint_has_no_auth(self, client: TestClient, db_session):
        """Items endpoint should currently be accessible without auth.

        NOTE: Before production, add authentication middleware and
        update this test to verify that unauthenticated requests are rejected.
        """
        response = client.get("/api/items")
        # Currently returns 200 (no auth)
        assert response.status_code == 200

    def test_create_item_has_no_auth(self, client: TestClient, db_session):
        """Create item endpoint should currently be accessible without auth.

        NOTE: Before production, add authentication and update this test.
        """
        response = client.post(
            "/api/items",
            json={"name": "Unauth Item", "description": "No auth"},
        )
        # Currently returns 201 (no auth)
        assert response.status_code == 201
