from fastapi import FastAPI
from app.routers import speech

app = FastAPI()

# Include routers
app.include_router(speech.router, prefix="/api/speech", tags=["Speech"])

# Health check endpoint
@app.get("/api/health")
def health_check():
    return {"status": "ok"}