from fastapi import FastAPI
from backend.app.routes.recommendation_routes import router as recommendation_router


app=FastAPI(
    title = "JanMitra AI Backend",
    description = "Backend for JanMitra AI citizen assistance platform",
    version = "1.0.0",
    )

app.include_router(recommendation_router)

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