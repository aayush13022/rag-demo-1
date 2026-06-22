"""Mutual Fund FAQ Assistant — Streamlit UI + in-process RAG backend."""

from __future__ import annotations

import streamlit as st

from config.settings import configure_logging, get_settings
from rag.models import RAGResponse
from rag.warmup import warmup_rag_stack
from stapp.chat_handler import ChatError, handle_message
from stapp.constants import (
    DISCLAIMER,
    EXAMPLE_QUESTIONS,
    FOOTER_NOTE,
    SUPPORTED_SCHEMES,
    WELCOME_MESSAGE,
)

configure_logging()


def _init_session_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []


@st.cache_resource(show_spinner="Loading assistant models…")
def _warmup_stack() -> bool:
    warmup_rag_stack(get_settings())
    return True


def _render_assistant_message(response: RAGResponse) -> None:
    if response.refused:
        st.warning(response.answer)
        if response.educational_link:
            st.link_button("Learn more at AMFI", response.educational_link)
        return

    st.markdown(response.answer)

    if response.source_url:
        st.caption("Factual data")
        st.link_button("View source on Groww", response.source_url)
        if response.last_updated_from_sources:
            st.caption(f"Last updated from sources: {response.last_updated_from_sources}")

    st.caption(response.disclaimer)


def _reset_chat() -> None:
    st.session_state.messages = []


def _process_question(question: str) -> None:
    st.session_state.messages.append({"role": "user", "content": question})
    try:
        response = handle_message(question)
        st.session_state.messages.append(
            {"role": "assistant", "content": response.answer, "response": response}
        )
    except ChatError as exc:
        st.session_state.messages.append(
            {"role": "assistant", "content": str(exc), "error": True}
        )


def main() -> None:
    st.set_page_config(
        page_title="Mutual Fund FAQ Assistant",
        page_icon="💬",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    _init_session_state()
    _warmup_stack()

    st.warning(f"**Disclaimer:** {DISCLAIMER}")

    header_col, home_col = st.columns([0.8, 0.2])
    with header_col:
        st.title("Mutual Fund FAQ Assistant")
        st.caption("HDFC · 5 schemes")
    with home_col:
        if st.session_state.messages:
            st.button(
                "← Back to home",
                key="home-button",
                on_click=_reset_chat,
                use_container_width=True,
            )

    if not st.session_state.messages:
        st.markdown(WELCOME_MESSAGE)
        st.markdown("**Supported schemes**")
        for scheme in SUPPORTED_SCHEMES:
            st.markdown(f"- {scheme}")

        st.markdown("**Try an example**")
        cols = st.columns(len(EXAMPLE_QUESTIONS))
        for col, question in zip(cols, EXAMPLE_QUESTIONS, strict=True):
            if col.button(question, key=f"example-{question}", use_container_width=True):
                _process_question(question)
                st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(message["content"])
            elif message.get("error"):
                st.error(message["content"])
            else:
                response = message.get("response")
                if isinstance(response, RAGResponse):
                    _render_assistant_message(response)
                else:
                    st.markdown(message["content"])

    if prompt := st.chat_input("Ask a factual question about an HDFC scheme…"):
        _process_question(prompt)
        st.rerun()

    st.caption(FOOTER_NOTE)


if __name__ == "__main__":
    main()
