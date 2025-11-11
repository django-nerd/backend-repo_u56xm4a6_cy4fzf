import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Product, ShoppingMessage, Trend, Achievement

app = FastAPI(title="Shopping AI Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    summary: str
    suggestions: List[Product] = []
    insights: List[str] = []

@app.get("/")
def read_root():
    return {"message": "Shopping AI Assistant Backend"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os as _os
    response["database_url"] = "✅ Set" if _os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if _os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest):
    user_message = payload.message.strip()

    # Simple rule-based mock insights and product suggestions
    sample_products = [
        Product(
            title="AirLite Pro Wireless Earbuds",
            description="ANC, 30h battery, IPX5",
            price=129.0,
            category="Audio",
            image="https://images.unsplash.com/photo-1518443728798-5d7a8143b8ab?q=80&w=1200&auto=format&fit=crop",
            rating=4.6,
            specs=["Active Noise Cancelling", "Bluetooth 5.3", "Wireless Charging"],
            retailers=[
                {"name": "Apple", "price": 129.0, "best": True},
                {"name": "Amazon", "price": 125.0},
                {"name": "BestBuy", "price": 127.0}
            ]
        ),
        Product(
            title="Nimbus X Laptop 14",
            description="Ultra-light 14"" laptop with M2-class performance",
            price=1299.0,
            category="Computers",
            image="https://images.unsplash.com/photo-1517336714731-489689fd1ca8?q=80&w=1200&auto=format&fit=crop",
            rating=4.8,
            specs=["16GB RAM", "512GB SSD", "Retina-class Display"],
            retailers=[
                {"name": "Brand Store", "price": 1299.0, "best": True},
                {"name": "Amazon", "price": 1249.0}
            ]
        ),
        Product(
            title="AuraFit Smartwatch 7",
            description="Health tracking with AMOLED display",
            price=249.0,
            category="Wearables",
            image="https://images.unsplash.com/photo-1511732351157-1865efcb7b7b?q=80&w=1200&auto=format&fit=crop",
            rating=4.5,
            specs=["ECG", "SpO2", "GPS", "7-day battery"],
            retailers=[
                {"name": "Brand Store", "price": 249.0},
                {"name": "Amazon", "price": 239.0, "best": True}
            ]
        )
    ]

    summary = (
        "I compared top options balancing performance, value, and reliability. "
        "Based on your query, these are the most relevant picks with quick pros/cons."
    )

    insights = [
        "Prioritize battery life and comfort for all‑day use.",
        "Look for multi‑point Bluetooth for seamless device switching.",
        "Retailer prices fluctuate daily — set a price alert if not urgent.",
    ]

    # Save conversation message (optional persistence)
    try:
        create_document("shoppingmessage", {
            "user_id": payload.user_id,
            "role": "user",
            "content": user_message,
            "summary": summary
        })
    except Exception:
        pass

    return ChatResponse(summary=summary, suggestions=sample_products, insights=insights)

@app.get("/api/trending", response_model=List[Trend])
def get_trending(limit: int = 6):
    items = [
        Trend(title="Noise‑Cancelling Headphones", category="Audio", price=299.0,
              image="https://images.unsplash.com/photo-1518443739046-d2b7b67ab4ac?q=80&w=1200&auto=format&fit=crop", rating=4.7),
        Trend(title="USB‑C GaN Charger 65W", category="Accessories", price=39.0,
              image="https://images.unsplash.com/photo-1616348436168-de43ad0db179?q=80&w=1200&auto=format&fit=crop", rating=4.6),
        Trend(title="Mechanical Keyboard", category="Peripherals", price=119.0,
              image="https://images.unsplash.com/photo-1517336714731-489689fd1ca8?q=80&w=1200&auto=format&fit=crop", rating=4.5),
        Trend(title="Smart Home Hub", category="Smart Home", price=89.0,
              image="https://images.unsplash.com/photo-1587578932405-7d9d4da9a2b5?q=80&w=1200&auto=format&fit=crop", rating=4.4),
        Trend(title="Portable SSD 1TB", category="Storage", price=99.0,
              image="https://images.unsplash.com/photo-1606229365485-93a3bda3bda9?q=80&w=1200&auto=format&fit=crop", rating=4.8),
        Trend(title="Wireless Mouse", category="Peripherals", price=49.0,
              image="https://images.unsplash.com/photo-1587825140400-1086b59eb5d8?q=80&w=1200&auto=format&fit=crop", rating=4.6),
    ]
    return items[:limit]

@app.get("/api/essentials", response_model=List[Trend])
def get_essentials(limit: int = 6):
    items = [
        Trend(title="USB‑C Cable (2‑pack)", category="Cables", price=12.0,
              image="https://images.unsplash.com/photo-1584907797074-426aa1a16800?q=80&w=1200&auto=format&fit=crop", rating=4.7),
        Trend(title="Screen Cleaner Kit", category="Care", price=15.0,
              image="https://images.unsplash.com/photo-1625012715369-6f0a4f377444?q=80&w=1200&auto=format&fit=crop", rating=4.6),
        Trend(title="Wireless Charger", category="Charging", price=29.0,
              image="https://images.unsplash.com/photo-1555617981-e6c88f17bf8c?q=80&w=1200&auto=format&fit=crop", rating=4.5),
        Trend(title="Cable Organizer", category="Desk", price=9.0,
              image="https://images.unsplash.com/photo-1605649487219-4e0be84a3d8f?q=80&w=1200&auto=format&fit=crop", rating=4.4),
        Trend(title="Laptop Stand", category="Ergonomics", price=39.0,
              image="https://images.unsplash.com/photo-1541807084-5c52b6b3adef?q=80&w=1200&auto=format&fit=crop", rating=4.7),
        Trend(title="Compact Power Bank", category="Power", price=35.0,
              image="https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=1200&auto=format&fit=crop", rating=4.6),
    ]
    return items[:limit]

@app.get("/api/picks/{user_id}", response_model=List[Trend])
def get_personal_picks(user_id: str, limit: int = 6):
    # Simple heuristic demo
    items = [
        Trend(title="Work‑from‑Home Headset", category="Audio", price=99.0,
              image="https://images.unsplash.com/photo-1518443739046-d2b7b67ab4ac?q=80&w=1200&auto=format&fit=crop", rating=4.6),
        Trend(title="Minimal Desk Lamp", category="Desk", price=59.0,
              image="https://images.unsplash.com/photo-1519710164239-da123dc03ef4?q=80&w=1200&auto=format&fit=crop", rating=4.7),
        Trend(title="Ergo Office Chair", category="Ergonomics", price=299.0,
              image="https://images.unsplash.com/photo-1582582429416-c51b9c6fc36f?q=80&w=1200&auto=format&fit=crop", rating=4.5),
    ]
    return items[:limit]

@app.post("/api/achievements/{user_id}")
def unlock_achievement(user_id: str, achievement: Achievement):
    try:
        create_document("achievement", achievement)
        return {"status": "ok"}
    except Exception as e:
        # Fallback without DB
        return {"status": "ok", "note": "stored in memory disabled", "error": str(e)[:60]}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
