from fastapi.testclient import TestClient

from apps.api.app.main import app


client = TestClient(app)


def test_valid_inference_request():
    payload = {
        "prompt": "Explain Kubernetes HPA",
        "model": "demo",
    }

    response = client.post(
        "/v1/inference/validate",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "accepted"
    assert data["model"] == "demo"
    assert data["prompt_length"] == 22

    assert response.headers.get("X-Request-ID")


def test_empty_prompt_rejected():
    payload = {
        "prompt": "",
        "model": "demo",
    }

    response = client.post(
        "/v1/inference/validate",
        json=payload,
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"]["code"] == "VALIDATION_ERROR"

    assert {
        "field": "body.prompt",
        "code": "string_too_short",
    } in data["error"]["details"]

    assert response.headers.get("X-Request-ID")


def test_sensitive_prompt_not_exposed_in_validation_error():
    secret = "CONFIDENTIAL_FINANCE_DATA"

    payload = {
        "prompt": secret + "A" * 501,
        "model": "demo",
    }

    response = client.post(
        "/v1/inference/validate",
        json=payload,
    )

    assert response.status_code == 422

    body = response.text
    data = response.json()

    assert secret not in body, "SECURITY FAIL: Sensitive input leaked"

    assert data["error"]["code"] == "VALIDATION_ERROR"

    assert {
        "field": "body.prompt",
        "code": "string_too_long",
    } in data["error"]["details"]

    assert response.headers.get("X-Request-ID")


def test_readiness_failure_does_not_affect_liveness(monkeypatch):
    from apps.api.app import main as main_module

    monkeypatch.setattr(
        main_module,
        "dependency_available",
        False,
    )

    live_response = client.get("/health/live")
    ready_response = client.get("/health/ready")

    assert live_response.status_code == 200
    assert live_response.json()["status"] == "alive"

    assert ready_response.status_code == 503
    assert ready_response.json()["detail"] == "Service is not ready"

    assert live_response.headers.get("X-Request-ID")
    assert ready_response.headers.get("X-Request-ID")


def test_readiness_failure_does_not_affect_liveness(monkeypatch):
    from apps.api.app import main as main_module

    monkeypatch.setattr(
        main_module,
        "dependency_available",
        False,
    )

    live_response = client.get("/health/live")
    ready_response = client.get("/health/ready")

    assert live_response.status_code == 200
    assert live_response.json()["status"] == "alive"

    assert ready_response.status_code == 503
    assert ready_response.json()["detail"] == "Service is not ready"

    assert live_response.headers.get("X-Request-ID")
    assert ready_response.headers.get("X-Request-ID")


def test_readiness_recovers_after_dependency_restored(monkeypatch):
    from apps.api.app import main as main_module

    monkeypatch.setattr(
        main_module,
        "dependency_available",
        False,
    )

    failed_response = client.get("/health/ready")

    assert failed_response.status_code == 503
    assert failed_response.json()["detail"] == "Service is not ready"

    monkeypatch.setattr(
        main_module,
        "dependency_available",
        True,
    )

    recovered_response = client.get("/health/ready")

    assert recovered_response.status_code == 200
    assert recovered_response.json()["status"] == "ready"

    assert recovered_response.headers.get("X-Request-ID")

    assert (
        failed_response.headers["X-Request-ID"]
        != recovered_response.headers["X-Request-ID"]
    )


def test_missing_prompt_rejected():
    payload = {
        "model": "demo",
    }

    response = client.post(
        "/v1/inference/validate",
        json=payload,
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"]["code"] == "VALIDATION_ERROR"

    assert {
        "field": "body.prompt",
        "code": "missing",
    } in data["error"]["details"]

    assert response.headers.get("X-Request-ID")
