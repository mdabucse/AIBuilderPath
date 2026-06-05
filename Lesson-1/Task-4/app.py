"""Streamlit chat UI for the from-scratch RAG chatbot.

Run it with:   streamlit run app.py
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from rag import RAGChatbot, Settings
from rag.loaders import SUPPORTED_SUFFIXES
from rag.pipeline import build_index, load_or_build_index
from rag.vector_store import VectorStore

st.set_page_config(page_title="RAG Chatbot", page_icon="💬", layout="wide")


# --------------------------------------------------------------------------- #
# Settings: start from .env, then let the sidebar override for this session.
# --------------------------------------------------------------------------- #
def build_settings() -> Settings:
    s = Settings.from_env()

    st.sidebar.header("⚙️ Configuration")

    backends = ["ollama", "azure", "claude"]
    s.llm_backend = st.sidebar.selectbox(
        "LLM backend", backends, index=backends.index(s.llm_backend)
        if s.llm_backend in backends else 0,
        help="Which provider generates the answer.",
    )

    if s.llm_backend == "ollama":
        s.ollama_chat_model = st.sidebar.text_input("Ollama chat model", s.ollama_chat_model)
    elif s.llm_backend == "azure":
        s.azure_chat_deployment = st.sidebar.text_input("Azure chat deployment", s.azure_chat_deployment)
        if not s.azure_api_key or not s.azure_endpoint:
            st.sidebar.warning("Azure endpoint/key missing in .env.")
    elif s.llm_backend == "claude":
        s.anthropic_model = st.sidebar.text_input("Claude model", s.anthropic_model)
        if not s.anthropic_api_key:
            st.sidebar.warning("ANTHROPIC_API_KEY missing in .env.")

    embed_backends = ["ollama", "azure"]
    s.embed_backend = st.sidebar.selectbox(
        "Embedding backend", embed_backends,
        index=embed_backends.index(s.embed_backend) if s.embed_backend in embed_backends else 0,
        help="Which provider turns text into vectors. Change → rebuild the index.",
    )
    if s.embed_backend == "ollama":
        s.ollama_embed_model = st.sidebar.text_input("Ollama embed model", s.ollama_embed_model)
    else:
        s.azure_embed_deployment = st.sidebar.text_input("Azure embed deployment", s.azure_embed_deployment)

    with st.sidebar.expander("Retrieval settings"):
        s.top_k = st.slider("Chunks to retrieve (top-k)", 1, 10, s.top_k)
        s.chunk_size = st.slider("Chunk size (chars)", 200, 2000, s.chunk_size, step=100)
        s.chunk_overlap = st.slider("Chunk overlap (chars)", 0, 400, s.chunk_overlap, step=20)

    return s


# --------------------------------------------------------------------------- #
# Knowledge base management.
# --------------------------------------------------------------------------- #
def knowledge_base_panel(settings: Settings) -> None:
    st.sidebar.header("📚 Knowledge base")
    data_path = settings.data_path
    data_path.mkdir(parents=True, exist_ok=True)

    files = sorted(
        p.name for p in data_path.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_SUFFIXES
    )
    st.sidebar.caption(f"{len(files)} document(s) in `{settings.data_dir}/`")
    if files:
        st.sidebar.write("\n".join(f"• {f}" for f in files))

    uploads = st.sidebar.file_uploader(
        "Add documents", type=["txt", "md", "pdf"], accept_multiple_files=True
    )
    if uploads:
        for up in uploads:
            (data_path / up.name).write_bytes(up.getbuffer())
        st.sidebar.success(f"Added {len(uploads)} file(s). Click Rebuild index.")

    if st.session_state.get("store") is not None:
        st.sidebar.caption(f"Index: {st.session_state.store.size} chunks")

    if st.sidebar.button("🔄 Rebuild index", use_container_width=True):
        with st.spinner("Embedding documents and building the index…"):
            try:
                st.session_state.store = build_index(settings)
                st.sidebar.success("Index rebuilt.")
            except Exception as exc:  # surface a clean message, not a stack trace
                st.sidebar.error(str(exc))


def ensure_index(settings: Settings) -> bool:
    """Make sure a vector store is loaded; build on first run. Returns success."""
    if st.session_state.get("store") is not None:
        return True
    with st.spinner("Preparing the knowledge base…"):
        try:
            st.session_state.store = load_or_build_index(settings)
            return True
        except Exception as exc:
            st.error(str(exc))
            return False


# --------------------------------------------------------------------------- #
# Chat.
# --------------------------------------------------------------------------- #
def render_history() -> None:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                _render_sources(msg["sources"])


def _render_sources(sources: list[dict]) -> None:
    with st.expander(f"📖 Sources ({len(sources)})"):
        for i, src in enumerate(sources, 1):
            score = src.get("score", 0.0)
            st.markdown(f"**[{i}] {src.get('source', 'unknown')}** · similarity {score:.3f}")
            snippet = src["text"][:400] + ("…" if len(src["text"]) > 400 else "")
            st.caption(snippet)


def main() -> None:
    settings = build_settings()
    knowledge_base_panel(settings)

    st.title("💬 RAG Chatbot")
    st.caption(
        f"Retrieval-Augmented Generation from scratch · "
        f"LLM: **{settings.llm_backend}** · embeddings: **{settings.embed_backend}**"
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if st.sidebar.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if not ensure_index(settings):
        st.info("Add documents to the knowledge base and rebuild the index to start chatting.")
        return

    render_history()

    prompt = st.chat_input("Ask a question about your documents…")
    if not prompt:
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # History excludes the message we just added (it's the current question).
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[:-1]
    ]
    bot = RAGChatbot(st.session_state.store, settings)

    with st.chat_message("assistant"):
        try:
            tokens, sources = bot.answer(prompt, history)
            answer = st.write_stream(tokens)
            _render_sources(sources)
        except Exception as exc:
            answer, sources = f"⚠️ {exc}", []
            st.error(str(exc))

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )


if __name__ == "__main__":
    main()
