import json
import random
import time
from dataclasses import dataclass

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

from data_loader import SCHEMES
from matcher import match_schemes
from config import config
from schemas import AssistantResponse

app = FastAPI(docs_url=None, redoc_url=None)


@dataclass
class OTPRecord:
    otp: str
    sent_at: float
    expires_at: float


OTP_COOLDOWN_SECONDS = 30
OTP_EXPIRY_SECONDS = 300
_otp_store = {}


class OTPRequest(BaseModel):
    phone: str = Field(..., min_length=10, max_length=15, pattern=r"^[0-9]+$")


class OTPVerifyRequest(BaseModel):
    phone: str = Field(..., min_length=10, max_length=15, pattern=r"^[0-9]+$")
    otp: str = Field(..., min_length=6, max_length=6, pattern=r"^[0-9]{6}$")


def _remaining_cooldown(record: OTPRecord, now: float) -> int:
    return max(0, OTP_COOLDOWN_SECONDS - int(now - record.sent_at))


def _generate_otp() -> str:
    return f"{random.randint(0, 999999):06d}"


@app.get("/ping")
def ping():
    payload = {"msg": "ok"}

    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    if len(raw) > config.response.MAX_RESPONSE_BYTES:
        return Response(
            content=b'{"msg":"payload too large"}',
            media_type="application/json",
            status_code=500
        )

    return Response(content=raw, media_type="application/json")


@app.post("/auth/request-otp")
def request_otp(payload: OTPRequest):
    now = time.time()
    existing = _otp_store.get(payload.phone)

    if existing:
        cooldown_left = _remaining_cooldown(existing, now)
        if cooldown_left > 0:
            raise HTTPException(
                status_code=429,
                detail={
                    "msg": "Please wait before requesting another OTP.",
                    "cooldown_seconds": cooldown_left,
                },
            )

    otp = _generate_otp()
    _otp_store[payload.phone] = OTPRecord(
        otp=otp,
        sent_at=now,
        expires_at=now + OTP_EXPIRY_SECONDS,
    )

    return {
        "msg": "OTP sent successfully.",
        "cooldown_seconds": OTP_COOLDOWN_SECONDS,
        "expires_in_seconds": OTP_EXPIRY_SECONDS,
        "otp": otp,
    }


@app.post("/auth/verify-otp")
def verify_otp(payload: OTPVerifyRequest):
    record = _otp_store.get(payload.phone)
    now = time.time()

    if not record:
        raise HTTPException(status_code=404, detail="OTP not found. Please request a new one.")

    if now > record.expires_at:
        del _otp_store[payload.phone]
        raise HTTPException(status_code=400, detail="OTP expired. Please request a new one.")

    if payload.otp != record.otp:
        raise HTTPException(status_code=401, detail="Invalid OTP.")

    del _otp_store[payload.phone]
    return {"msg": "Login successful.", "token": f"demo-token-{payload.phone}"}


@app.get("/ask")
def ask(q: str, lang: str = "hi"):
    matched = [
        s for s in match_schemes(q, SCHEMES, config.response.MAX_SCHEME_RESULTS)
        if s.get("lang") == lang
    ]
    schemes_out = []
    for s in matched:
        schemes_out.append({
            "id": s["id"],
            "name": s["name"],
            "benefit": s["benefit"]
        })

    response = AssistantResponse(
        msg="मिलान की गई योजनाएं",
        schemes=schemes_out,
        steps=[],
        lang=lang
    )

    raw = json.dumps(
        response.model_dump(),
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")

    if len(raw) > config.response.MAX_RESPONSE_BYTES:
        return Response(
            content=b'{"msg":"response too large"}',
            media_type="application/json",
            status_code=500
        )
    print(f"Response size: {len(raw)} bytes")
    return Response(content=raw, media_type="application/json")
