from fastapi import FastAPI, status
from app.config import DATABASE_URL, WEBHOOK_SECRET
from app.models import init_db

app = FastAPI(title="Lyftr Backend Assignment")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health/live")
def health_live():
    return {"status": "alive"}


@app.get("/health/ready")
def health_ready():
    if not DATABASE_URL or not WEBHOOK_SECRET:
        return {"status": "not ready"}, status.HTTP_503_SERVICE_UNAVAILABLE
    return {"status": "ready"}
