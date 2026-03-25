"""
Pydantic schemas for request/response validation.
Separates API contracts from database models.
"""
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ItemBase(BaseModel):
    """Base schema for Item - used for input validation."""

    name: str = Field(..., min_length=1, max_length=255, description="Item name")
    description: str = Field(
        default="", max_length=1000, description="Item description"
    )


class ItemCreate(ItemBase):
    """Schema for creating a new Item."""

    pass


class ItemUpdate(BaseModel):
    """Schema for updating an existing Item."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)


class ItemResponse(ItemBase):
    """Schema for Item response - includes generated fields."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Item unique identifier")
    created_at: datetime | None = Field(
        default=None, description="Creation timestamp"
    )
    updated_at: datetime | None = Field(
        default=None, description="Last update timestamp"
    )


class ItemListResponse(BaseModel):
    """Schema for list of items response."""

    items: list[ItemResponse]
    total: int
