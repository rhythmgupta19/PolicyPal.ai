from data_loader import SCHEMES
from matcher import match_schemes
from fastapi import FastAPI, Response
import json

from config import config
from schemas import AssistantResponse

app = FastAPI(docs_url=None, redoc_url=None)


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

    import json
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
