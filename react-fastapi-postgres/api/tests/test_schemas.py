"""API tests for Pydantic schema validation."""
import pytest
from pydantic import ValidationError
from schemas import ItemCreate, ItemUpdate, ItemResponse, ItemListResponse


class TestItemCreateSchema:
    """Test ItemCreate schema validation."""

    def test_valid_item_create(self):
        """Valid item creation should succeed."""
        item = ItemCreate(name="Test Item", description="A test item")
        assert item.name == "Test Item"
        assert item.description == "A test item"

    def test_item_create_default_description(self):
        """Item creation with no description should default to empty string."""
        item = ItemCreate(name="Test Item")
        assert item.description == ""

    def test_item_create_empty_name_rejected(self):
        """Empty name should be rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ItemCreate(name="")
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("name",) for e in errors)

    def test_item_create_missing_name_rejected(self):
        """Missing name should be rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ItemCreate(description="no name")
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("name",) for e in errors)

    def test_item_create_name_too_long_rejected(self):
        """Name exceeding 255 characters should be rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ItemCreate(name="x" * 256)
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("name",) for e in errors)

    def test_item_create_name_max_length_accepted(self):
        """Name at exactly 255 characters should be accepted."""
        item = ItemCreate(name="x" * 255)
        assert len(item.name) == 255

    def test_item_create_description_too_long_rejected(self):
        """Description exceeding 1000 characters should be rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ItemCreate(name="Valid", description="x" * 1001)
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("description",) for e in errors)

    def test_item_create_description_max_length_accepted(self):
        """Description at exactly 1000 characters should be accepted."""
        item = ItemCreate(name="Valid", description="x" * 1000)
        assert len(item.description) == 1000


class TestItemUpdateSchema:
    """Test ItemUpdate schema validation."""

    def test_partial_update_name_only(self):
        """Partial update with only name should succeed."""
        update = ItemUpdate(name="Updated Name")
        assert update.name == "Updated Name"
        assert update.description is None

    def test_partial_update_description_only(self):
        """Partial update with only description should succeed."""
        update = ItemUpdate(description="Updated description")
        assert update.name is None
        assert update.description == "Updated description"

    def test_partial_update_both_fields(self):
        """Partial update with both fields should succeed."""
        update = ItemUpdate(name="Updated", description="Updated desc")
        assert update.name == "Updated"
        assert update.description == "Updated desc"

    def test_partial_update_empty_rejected(self):
        """Empty name in update should be rejected if provided."""
        with pytest.raises(ValidationError):
            ItemUpdate(name="")


class TestItemResponseSchema:
    """Test ItemResponse schema."""

    def test_item_response_from_attributes(self):
        """ItemResponse should support from_attributes config."""
        # Simulate an ORM object
        class FakeItem:
            id = 1
            name = "Test"
            description = "Desc"
            created_at = None
            updated_at = None

        response = ItemResponse.model_validate(FakeItem())
        assert response.id == 1
        assert response.name == "Test"

    def test_item_response_has_all_fields(self):
        """ItemResponse should include all expected fields."""
        data = {
            "id": 1,
            "name": "Test",
            "description": "Desc",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
        }
        response = ItemResponse(**data)
        assert response.id == 1
        assert response.name == "Test"
        assert response.description == "Desc"


class TestItemListResponseSchema:
    """Test ItemListResponse schema."""

    def test_empty_list_response(self):
        """Empty list response should serialize correctly."""
        response = ItemListResponse(items=[], total=0)
        assert response.total == 0
        assert response.items == []

    def test_list_with_items(self):
        """List with items should serialize correctly."""
        items = [
            ItemResponse(
                id=1, name="Item 1", description="", created_at=None, updated_at=None
            ),
            ItemResponse(
                id=2, name="Item 2", description="", created_at=None, updated_at=None
            ),
        ]
        response = ItemListResponse(items=items, total=2)
        assert response.total == 2
        assert len(response.items) == 2
