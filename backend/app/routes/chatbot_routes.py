"""Chatbot & NLP endpoints.

Mounted by the existing app in app/main.py:

    from backend.app.routes.chatbot_routes import router as chatbot_router
    app.include_router(chatbot_router)

Scheme endpoints (/api/schemes, /api/schemes/recommend, /api/admin/seed-schemes)
are intentionally NOT here - they belong to the scheme recommendation module.
"""
from __future__ import annotations

import re
import time
from collections import defaultdict, deque

from fastapi import APIRouter, Depends, HTTPException, Request

from backend.app.services import chatbot_service as chatbot
from backend.app.services.chatbot_service import AnalyzeRequest, ChatRequest, ChatResponse

router = APIRouter(tags=["chatbot"])

_SESSION_ID_RE = re.compile(r"^[A-Za-z0-9_-]{8,64}$")

# --------------------------------------------------------------------------- #
# Simple per-IP rate limit (in-memory, per process). Only applied to the
# endpoints that can trigger a Gemini call / NLP work.
# --------------------------------------------------------------------------- #
_rate_hits: dict[str, deque] = defaultdict(deque)


async def rate_limit(request: Request) -> None:
    ip = request.client.host if request.client else "unknown"
    now = time.monotonic()
    window = _rate_hits[ip]
    while window and now - window[0] > 60:
        window.popleft()
    if len(window) >= chatbot.get_chatbot_settings().rate_limit_per_minute:
        raise HTTPException(status_code=429, detail="Too many requests. Please wait a minute.")
    window.append(now)


def _valid_session_id(session_id: str) -> str:
    if not _SESSION_ID_RE.match(session_id):
        raise HTTPException(status_code=400, detail="Invalid session id")
    return session_id


# --------------------------------------------------------------------------- #
# Endpoints
# --------------------------------------------------------------------------- #
@router.post("/api/chat/message", response_model=ChatResponse, dependencies=[Depends(rate_limit)])
async def chat_message(req: ChatRequest):
    """Main chat endpoint. The voice module can send its speech-to-text transcript here."""
    return await chatbot.handle_message(req)


@router.get("/api/chat/history/{session_id}")
async def chat_history(session_id: str):
    return await chatbot.get_history(_valid_session_id(session_id))


@router.delete("/api/chat/session/{session_id}")
async def delete_chat_session(session_id: str):
    await chatbot.delete_session(_valid_session_id(session_id))
    return {"deleted": True}


@router.post("/api/nlp/analyze", dependencies=[Depends(rate_limit)])
async def nlp_analyze(req: AnalyzeRequest):
    r = chatbot.analyze(req.text)
    return {"language": r.language, "intent": r.intent, "confidence": r.confidence,
            "profile": r.profile, "complaint_category": r.complaint_category}