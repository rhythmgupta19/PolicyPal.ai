import json

from fastapi import FastAPI, Response, WebSocket, WebSocketDisconnect

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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time chat"""
    await websocket.accept()
    try:
        while True:
            # Receive query from client
            data = await websocket.receive_json()
            q = data.get("q", "").strip()
            lang = data.get("lang", "hi")
            
            if not q:
                await websocket.send_json({"error": "Empty query"})
                continue
            
            if lang not in config.language.SUPPORTED_LANGUAGES:
                lang = config.language.DEFAULT_LANGUAGE
            
            # Match schemes
            matched = match_schemes(q, SCHEMES, config.response.MAX_SCHEME_RESULTS)
            
            schemes_out = []
            for s in matched:
                if s.get("lang") == lang or not s.get("lang"):
                    schemes_out.append({
                        "id": s.get("id", ""),
                        "name": s.get(f"name_{lang}") or s.get("name_hi") or s.get("name_en") or s.get("name", ""),
                        "benefit": s.get(f"benefit_{lang}") or s.get("benefit_hi") or s.get("benefit_en") or s.get("benefit", ""),
                    })
            
            # Send response
            response = {
                "msg": "मिलान की गई योजनाएं" if schemes_out else "कोई उपयुक्त योजना नहीं मिली",
                "schemes": schemes_out,
                "steps": [],
                "lang": lang
            }
            
            await websocket.send_json(response)
            
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.send_json({"error": str(e)})
