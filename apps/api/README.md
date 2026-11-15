# Enterprise AI Platform — FastAPI Service

## Overview

Day 14 FastAPI backend development lab.

Current functionality:
- API request validation
- Liveness and readiness endpoints
- Structured JSON application logging
- Unique HTTP request IDs
- Sanitized validation error responses
- Automated Pytest regression tests

This is a local development service, not a production AI inference service.

## Technology Stack

- Python 3.14
- FastAPI
- Uvicorn
- Pydantic
- Pytest
- HTTPX

## Local Setup

Run from the repository root.

1. Create and activate a Python virtual environment.
2. Install dependencies:

    python -m pip install -r apps/api/requirements.lock

3. Start the API:

    python -m uvicorn apps.api.app.main:app --host 127.0.0.1 --port 8000

## API Endpoints

GET /
- Service information

GET /health/live
- Checks application responsiveness
- Expected healthy response: HTTP 200

GET /health/ready
- Checks simulated dependency readiness
- Healthy: HTTP 200
- Simulated dependency failure: HTTP 503

POST /v1/inference/validate
- Validates an inference request
- This endpoint does not run an AI model

GET /docs
- Swagger UI documentation

GET /openapi.json
- OpenAPI specification

## Smoke Tests

Liveness:

    curl -i http://127.0.0.1:8000/health/live

Readiness:

    curl -i http://127.0.0.1:8000/health/ready

Valid inference request:

    curl -i -X POST http://127.0.0.1:8000/v1/inference/validate \
      -H "Content-Type: application/json" \
      -d '{"prompt":"Explain Kubernetes HPA","model":"demo"}'

## Automated Testing

Run from the repository root:

    python -m pytest apps/api/tests/test_api.py -v

Day 14 baseline: 6 tests passed.

Tests cover:
- Valid inference request
- Empty prompt rejection
- Oversized prompt and sensitive response handling
- Readiness failure isolation
- Dependency recovery
- Missing required field

## Request ID and Logging

Each HTTP request receives an X-Request-ID response header.

Application logs include:
- Timestamp
- Log level
- Logger name
- Event message
- Request ID

Do not log user prompts, passwords, API keys, or secrets.

## Troubleshooting Runbook

### API connection refused

- Verify the Uvicorn process is running.
- Verify host 127.0.0.1 and port 8000.
- Check application startup errors.

### Liveness returns unexpected status

- Check Uvicorn logs.
- Check application errors.
- Verify the /health/live route.

### Readiness returns HTTP 503

- Verify the simulated dependency_available flag.
- False represents a simulated dependency outage.
- Restore True for normal local operation.

### Validation returns HTTP 422

- Check required prompt field.
- Check prompt length: 1 to 500 characters.
- Check allowed model value: demo.

### Automated tests fail

- Activate the correct Python environment.
- Verify installed dependencies.
- Run Pytest with verbose output.
- Inspect assertion failures.

## Known Limitations

- Dependency readiness is simulated using an in-memory variable.
- No real database, Redis, or AI model is connected.
- No production authentication or tenant authorization.
- Uvicorn access logs are not yet structured JSON.
- Dependency snapshot was generated on macOS.
- Starlette TestClient deprecation warning requires review.
- No production deployment approval is implied.
