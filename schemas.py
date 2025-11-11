"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    image: Optional[str] = Field(None, description="Image URL")
    rating: Optional[float] = Field(4.5, ge=0, le=5)
    specs: Optional[List[str]] = Field(default_factory=list)
    retailers: Optional[List[dict]] = Field(default_factory=list, description="Retailer options with prices")
    in_stock: bool = Field(True, description="Whether product is in stock")

class ShoppingMessage(BaseModel):
    """Conversation messages between user and assistant"""
    user_id: str
    role: str = Field(..., description="user or assistant")
    content: str
    summary: Optional[str] = None

class Trend(BaseModel):
    """Trending items curated by the system"""
    title: str
    category: str
    price: float
    image: Optional[str] = None
    rating: Optional[float] = 4.5

class Achievement(BaseModel):
    """Achievement unlocked for smart shopping"""
    user_id: str
    title: str
    description: str
    icon: Optional[str] = "Star"
