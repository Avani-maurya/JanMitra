from fastapi import FastAPI

app=FastAPI(
    title = "JanMitra AI Backend",
    description = "Backend for JanMitra AI citizen assistance platform",
    version = "1.0.0",
    )


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