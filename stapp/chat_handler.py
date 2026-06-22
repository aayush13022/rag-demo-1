"""Chat handling — mirrors api/routes/chat.py in-process for Streamlit."""

from __future__ import annotations

import logging

from openai import AuthenticationError

from rag.generator import answer
from rag.guardrails import build_refusal_response, classify, should_refuse
from rag.models import RAGResponse

logger = logging.getLogger(__name__)


class ChatError(Exception):
    """User-facing chat failure."""


def handle_message(message: str) -> RAGResponse:
    text = message.strip()
    if not text:
        raise ChatError("Please enter a question.")

    query_type = classify(text)
    logger.info("Classified query as %s", query_type.value)

    if should_refuse(query_type):
        return build_refusal_response()

    try:
        return answer(text)
    except AuthenticationError as exc:
        logger.exception("Invalid Groq API key for chat request")
        raise ChatError(
            "Invalid GROQ_API_KEY. Add a valid key to .env or set "
            "LLM_PROVIDER=mock for local development."
        ) from exc
    except Exception as exc:
        logger.exception("Generation failed for chat request")
        raise ChatError(
            "The assistant is temporarily unavailable. Please try again shortly."
        ) from exc
