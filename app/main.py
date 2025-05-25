from fastapi import FastAPI, Request
from app.routers import speech
from app.middleware.logging_middleware import LoggingMiddleware

app = FastAPI()

# Custom logging middleware
app.add_middleware(LoggingMiddleware)

# Routers
app.include_router(speech.router, prefix="/api/speech", tags=["Speech"])

# Health check
@app.get("/api/health")
def health_check():
    return {"status": "ok"}
