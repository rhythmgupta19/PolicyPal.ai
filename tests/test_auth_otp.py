from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_request_otp_success():
    response = client.post("/auth/request-otp", json={"phone": "9999999999"})
    assert response.status_code == 200
    body = response.json()
    assert body["cooldown_seconds"] == 30
    assert len(body["otp"]) == 6


def test_request_otp_cooldown_enforced():
    first = client.post("/auth/request-otp", json={"phone": "8888888888"})
    assert first.status_code == 200

    second = client.post("/auth/request-otp", json={"phone": "8888888888"})
    assert second.status_code == 429
    assert second.json()["detail"]["cooldown_seconds"] > 0


def test_verify_otp_success_and_single_use():
    phone = "7777777777"
    otp_response = client.post("/auth/request-otp", json={"phone": phone})
    otp = otp_response.json()["otp"]

    verify = client.post("/auth/verify-otp", json={"phone": phone, "otp": otp})
    assert verify.status_code == 200

    verify_again = client.post("/auth/verify-otp", json={"phone": phone, "otp": otp})
    assert verify_again.status_code == 404


def test_verify_otp_invalid_code():
    phone = "6666666666"
    client.post("/auth/request-otp", json={"phone": phone})

    verify = client.post("/auth/verify-otp", json={"phone": phone, "otp": "000000"})
    assert verify.status_code == 401
