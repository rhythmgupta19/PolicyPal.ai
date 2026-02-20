import json

from fastapi import FastAPI, Response

from src.config import config
from src.data_loader import SCHEMES
from src.matcher import match_schemes
from src.schemas import AssistantResponse

app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/ping")
def ping():
    payload = {"msg": "ok"}

    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    if len(raw) > config.response.MAX_RESPONSE_BYTES:
        return Response(
            content=b'{"msg":"payload too large"}',
            media_type="application/json",
            status_code=500,
        )

    return Response(content=raw, media_type="application/json")


@app.get("/ask")
def ask(q: str, lang: str = "hi"):
    if lang not in config.language.SUPPORTED_LANGUAGES:
        lang = config.language.DEFAULT_LANGUAGE

    matched = match_schemes(q, SCHEMES, config.response.MAX_SCHEME_RESULTS)

    schemes_out = [
        {
            "id": s.get("id", ""),
            "name": s.get(f"name_{lang}") or s.get("name_hi") or s.get("name_en") or "",
            "benefit": s.get(f"benefits_{lang}") or s.get("benefits_hi") or s.get("benefits_en") or "",
        }
        for s in matched
    ]

    response = AssistantResponse(
        msg="मिलान की गई योजनाएं" if schemes_out else "कोई उपयुक्त योजना नहीं मिली",
        schemes=schemes_out,
        steps=[],
        lang=lang,
    )

    raw = json.dumps(
        response.model_dump(),
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    if len(raw) > config.response.MAX_RESPONSE_BYTES:
        return Response(
            content=b'{"msg":"response too large"}',
            media_type="application/json",
            status_code=500,
        )

    return Response(content=raw, media_type="application/json")
