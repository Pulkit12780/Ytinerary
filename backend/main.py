"""Ytinerary FastAPI backend — /plan and /plan/stream (SSE)."""
from __future__ import annotations
import asyncio
import json
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv

from .models import PlanRequest, PlanResponse, ErrorResponse
from .pipeline import run as run_pipeline, PipelineError

load_dotenv()

app = FastAPI(title="Ytinerary API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_ERROR_STATUS: dict[str, int] = {
    "INVALID_DESTINATION": 422,
    "MISSING_TRANSCRIPT": 404,
    "ZERO_PLACES": 422,
    "GEOCODING_FAILURE": 502,
    "PIPELINE_ERROR": 500,
}


# ── POST /plan ─────────────────────────────────────────────────────────────


@app.post(
    "/plan",
    response_model=PlanResponse,
    responses={
        422: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        502: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def plan(request: PlanRequest) -> PlanResponse:
    """Run the full pipeline and return a structured itinerary."""
    try:
        return await run_pipeline(request)
    except PipelineError as exc:
        status = _ERROR_STATUS.get(exc.code, 500)
        raise HTTPException(
            status_code=status,
            detail=ErrorResponse(
                error=exc.message, code=exc.code
            ).model_dump(),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="An unexpected error occurred.",
                code="PIPELINE_ERROR",
                detail=str(exc)[:200],
            ).model_dump(),
        )


# ── POST /plan/stream (SSE) ────────────────────────────────────────────────


@app.post("/plan/stream")
async def plan_stream(request: PlanRequest) -> StreamingResponse:
    """
    Run the pipeline and stream Server-Sent Events.

    Event types:
      progress  — {type, step, label}          (steps 1-4)
      result    — {type, data: PlanResponse}    (final output)
      error     — {type, code, message}         (on failure)
    """
    queue: asyncio.Queue = asyncio.Queue()

    async def _event_generator():
        # Start pipeline in background; it pushes progress events to the queue
        pipeline_task = asyncio.create_task(_run_with_queue(request, queue))

        try:
            while True:
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=120.0)
                except asyncio.TimeoutError:
                    yield _sse("error", {"type": "error", "code": "TIMEOUT", "message": "Pipeline timed out."})
                    break

                if event is None:
                    break

                event_type = event.get("type", "progress")
                yield _sse(event_type, event)

                if event_type in ("result", "error"):
                    break
        finally:
            pipeline_task.cancel()

    return StreamingResponse(
        _event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


async def _run_with_queue(request: PlanRequest, queue: asyncio.Queue) -> None:
    """Run the pipeline and push the final result or error onto the queue."""
    try:
        result = await run_pipeline(request, progress_queue=queue)
        await queue.put({
            "type": "result",
            "data": result.model_dump(mode="json"),
        })
    except PipelineError as exc:
        await queue.put({
            "type": "error",
            "code": exc.code,
            "message": exc.message,
        })
    except Exception as exc:
        await queue.put({
            "type": "error",
            "code": "PIPELINE_ERROR",
            "message": str(exc)[:200],
        })
    finally:
        await queue.put(None)  # sentinel: generator exits


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


# ── Health ─────────────────────────────────────────────────────────────────


@app.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "openai_key_set": bool(os.getenv("OPENAI_API_KEY")),
        "foursquare_key_set": bool(os.getenv("FOURSQUARE_API_KEY")),
    }
