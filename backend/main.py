from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import create_document, get_documents
from schemas import Message, ChatSession, Product, TrendItem, ResearchSummary

app = FastAPI(title="Shopping AI Assistant API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class NewChatRequest(BaseModel):
    user_id: str
    title: Optional[str] = None


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/test")
async def test_db():
    # Try to create and read a doc to validate connection
    _id = await create_document("ping", {"ping": "pong"})
    docs = await get_documents("ping", limit=1)
    return {"inserted": _id, "sample": docs[:1]}


@app.post("/chats", response_model=dict)
async def create_chat(req: NewChatRequest):
    title = req.title or "New Shopping Chat"
    session = ChatSession(user_id=req.user_id, title=title, messages=[])
    _id = await create_document("chats", session.model_dump())
    return {"id": _id, "title": title}


@app.get("/trending", response_model=List[TrendItem])
async def get_trending():
    # Placeholder curated items
    return [
        TrendItem(title="Apple AirPods Pro (2nd Gen)", tag="Audio", image="/airpods.jpg"),
        TrendItem(title="Stanley Quencher Tumbler", tag="Lifestyle", image="/tumbler.jpg"),
        TrendItem(title="Nintendo Switch OLED", tag="Gaming", image="/switch.jpg"),
    ]


class RecommendRequest(BaseModel):
    query: str
    budget: Optional[float] = None


class RecommendResponse(BaseModel):
    products: List[Product]
    research: ResearchSummary


@app.post("/recommend", response_model=RecommendResponse)
async def recommend(req: RecommendRequest):
    # For now, return structured mock data; in real scenario hook to LLM + aggregator
    products = [
        Product(
            name="Apple MacBook Air 13" M2",
            image="https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=60",
            price=1099.0,
            rating=4.8,
            specs=["M2 chip", "8GB RAM", "256GB SSD", "18-hr battery"],
            retailers=[
                {"retailer": "Apple", "price": 1099.0, "url": "https://apple.com/macbook-air", "is_best": False},
                {"retailer": "Amazon", "price": 999.0, "url": "https://amazon.com", "is_best": True},
            ],
            why_recommend="Best balance of portability, performance, and battery life for most shoppers.",
        ),
        Product(
            name="ASUS Zenbook 14 OLED",
            image="https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=60",
            price=899.0,
            rating=4.6,
            specs=["OLED display", "16GB RAM", "512GB SSD"],
            retailers=[
                {"retailer": "Best Buy", "price": 899.0, "url": "https://bestbuy.com", "is_best": True},
                {"retailer": "Amazon", "price": 929.0, "url": "https://amazon.com", "is_best": False},
            ],
            why_recommend="Stunning OLED screen with strong value under $1,000.",
        ),
    ]

    research = ResearchSummary(
        summary="Based on your request, here are the top picks that balance performance, battery life, and price.",
        highlights=[
            "MacBook Air M2 leads in efficiency and build quality",
            "Zenbook offers OLED at a lower price point",
            "Both have strong battery life and portable designs",
        ],
        caveats=[
            "If you need heavy GPU, consider a Pro-class device",
            "Prices can fluctuate — best price highlighted per retailer",
        ],
    )

    return RecommendResponse(products=products, research=research)
