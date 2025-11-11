from pydantic import BaseModel, Field
from typing import List, Optional


class Message(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str


class ChatSession(BaseModel):
    user_id: str
    title: str
    messages: List[Message] = []


class ProductRetailerOption(BaseModel):
    retailer: str
    price: float
    url: str
    is_best: bool = False


class Product(BaseModel):
    name: str
    image: Optional[str] = None
    price: float
    rating: float = 0.0
    specs: List[str] = []
    retailers: List[ProductRetailerOption] = []
    why_recommend: Optional[str] = None


class TrendItem(BaseModel):
    title: str
    image: Optional[str] = None
    tag: Optional[str] = None


class ResearchSummary(BaseModel):
    summary: str
    highlights: List[str] = []
    caveats: List[str] = []
