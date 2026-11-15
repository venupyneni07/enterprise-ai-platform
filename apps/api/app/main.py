from fastapi import FastAPI

app = FastAPI(
    title="Enterprise AI Platform API",
    description="Backend API for our Enterprise AI Platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "service": "enterprise-ai-platform-api",
        "status": "running",
        "version": "0.1.0",
    }


from typing import Literal

from pydantic import BaseModel, Field


class InferenceRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=500)
    model: Literal["demo"] = "demo"


@app.post("/v1/inference/validate")
def validate_inference(request: InferenceRequest):
    return {
        "status": "accepted",
        "model": request.model,
        "prompt_length": len(request.prompt),
    }


@app.get("/health/live")
def liveness():
    return {
        "status": "alive",
        "service": "enterprise-ai-platform-api",
    }


from fastapi import HTTPException

# Lab simulation only; not a real dependency check.
dependency_available = True


@app.get("/health/ready")
def readiness():
    if not dependency_available:
        raise HTTPException(
            status_code=503,
            detail="Service is not ready",
        )

    return {
        "status": "ready",
        "service": "enterprise-ai-platform-api",
    }


from time import perf_counter
from uuid import uuid4

from fastapi import Request
from .logging_config import logger, request_id_ctx


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    request_id = uuid4().hex
    token = request_id_ctx.set(request_id)
    start_time = perf_counter()

    try:
        logger.info("request_started")

        response = await call_next(request)

        duration_ms = (perf_counter() - start_time) * 1000

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "request_completed method=%s status_code=%s duration_ms=%.2f",
            request.method,
            response.status_code,
            duration_ms,
        )

        return response

    except Exception:
        logger.error("request_failed")
        raise

    finally:
        request_id_ctx.reset(token)


from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


@app.exception_handler(RequestValidationError)
async def safe_validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    safe_details = [
        {
            "field": ".".join(str(part) for part in error["loc"]),
            "code": error["type"],
        }
        for error in exc.errors()
    ]

    logger.warning(
        "request_validation_failed error_count=%d",
        len(safe_details),
    )

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request payload",
                "details": safe_details,
            }
        },
    )
