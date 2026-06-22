"""Tests for Streamlit chat handler."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from rag.guardrails import REFUSAL_MESSAGE
from rag.models import RAGResponse
from stapp.chat_handler import ChatError, handle_message


def test_handle_message_refuses_advisory():
    response = handle_message("Should I invest in HDFC Defence?")
    assert response.refused is True
    assert REFUSAL_MESSAGE in response.answer


def test_handle_message_rejects_empty():
    with pytest.raises(ChatError, match="enter a question"):
        handle_message("   ")


@patch("stapp.chat_handler.answer")
def test_handle_message_delegates_to_rag(mock_answer):
    mock_answer.return_value = RAGResponse(
        answer="1.2%",
        source_url="https://groww.in/example",
        last_updated_from_sources="2026-06-22",
        disclaimer="Facts-only. No investment advice.",
        refused=False,
    )
    response = handle_message("What is the expense ratio?")
    assert response.answer == "1.2%"
    mock_answer.assert_called_once_with("What is the expense ratio?")
