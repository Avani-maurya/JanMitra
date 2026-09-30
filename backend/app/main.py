from fastapi import FastAPI
from backend.app.routes.recommendation_routes import router as recommendation_router
from backend.app.routes.chatbot_routes import router as chatbot_router
from backend.app.database.scheme_repository import get_all_active_schemes
from backend.app.services.chatbot_service import set_scheme_loader


app=FastAPI(
    title = "JanMitra AI Backend",
    description = "Backend for JanMitra AI citizen assistance platform",
    version = "1.0.0",
    )
async def chatbot_scheme_loader():
    return get_all_active_schemes()


set_scheme_loader(chatbot_scheme_loader)

app.include_router(recommendation_router)
app.include_router(chatbot_router)

@app.get("/")
def root():
    return {
    "message" : "JanMitra Backend is running."
    }

@app.get("/health")
def health():
    return {
    "status":"healthy"
    }