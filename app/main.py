from fastapi import FastAPI, status
from app.config import DATABASE_URL, WEBHOOK_SECRET
from app.models import init_db
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import re

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

class WebhookMessage(BaseModel):
    message_id: str = Field(..., min_length=1)
    from_msisdn: str = Field(..., alias="from")
    to_msisdn: str = Field(..., alias="to")
    ts: datetime
    text: Optional[str] = Field(None, max_length=4096)

    @staticmethod
    def validate_msisdn(value: str):
        if not re.fullmatch(r"\+[0-9]+", value):
            raise ValueError("Invalid MSISDN format")
        return value
