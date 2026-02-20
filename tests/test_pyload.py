from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_response_size_under_limit():
    res = client.get("/ask?q=test")
    payload = res.content

    assert len(payload) <= 10 * 1024


def test_ask_response_under_10kb():
    res = client.get("/ask?q=kisan")
    assert res.status_code == 200
    assert len(res.content) <= 10 * 1024


def test_ask_matches_tag_keyword():
    res = client.get("/ask?q=kisan&lang=hi")
    assert res.status_code == 200
    payload = res.content.decode("utf-8")
    assert "fin_001" in payload
