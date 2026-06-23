"""Voice input via a Streamlit custom component (Web Speech API + silence auto-stop)."""

from __future__ import annotations

import os
from typing import Any

import streamlit.components.v1 as components

_COMPONENT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "components", "voice_mic")
_voice_mic = components.declare_component("voice_mic", path=_COMPONENT_DIR)


def voice_input(*, silence_ms: int = 6000, key: str = "voice_mic") -> dict[str, Any] | None:
    """Render the mic button; return {text, id} when a recording finishes."""
    result = _voice_mic(silence_ms=silence_ms, key=key, default=None)
    if not isinstance(result, dict):
        return None
    text = str(result.get("text", "")).strip()
    utterance_id = result.get("id")
    if not text or utterance_id is None:
        return None
    return {"text": text, "id": utterance_id}
