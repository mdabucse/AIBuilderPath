"""The generation step — switchable across Ollama, Azure OpenAI and Claude.

This is the "Switching Endpoints" idea in practice: the rest of the app only
calls ``stream_chat(messages, settings)`` and never cares which provider is
behind it. ``messages`` is the familiar OpenAI-style list, e.g.::

    [{"role": "system", "content": "..."},
     {"role": "user", "content": "..."},
     {"role": "assistant", "content": "..."},
     {"role": "user", "content": "..."}]

``stream_chat`` yields text deltas (nice for live typing in the UI);
``chat`` collects them into one string.
"""

from __future__ import annotations

from typing import Iterator

from .config import Settings


def stream_chat(messages: list[dict], settings: Settings) -> Iterator[str]:
    """Yield the assistant's reply in streamed text chunks."""
    backend = settings.llm_backend
    if backend == "ollama":
        yield from _ollama_chat(messages, settings)
    elif backend == "azure":
        yield from _azure_chat(messages, settings)
    elif backend == "claude":
        yield from _claude_chat(messages, settings)
    else:
        raise ValueError(
            f"Unknown LLM_BACKEND '{backend}'. Use 'ollama', 'azure' or 'claude'."
        )


def chat(messages: list[dict], settings: Settings) -> str:
    """Non-streaming convenience wrapper."""
    return "".join(stream_chat(messages, settings))


# --------------------------------------------------------------------- Ollama
def _ollama_chat(messages: list[dict], settings: Settings) -> Iterator[str]:
    import json

    import requests

    base = settings.ollama_base_url.rstrip("/")
    try:
        resp = requests.post(
            f"{base}/api/chat",
            json={"model": settings.ollama_chat_model, "messages": messages, "stream": True},
            stream=True,
            timeout=600,
        )
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            f"Could not reach Ollama at {base}. Is it running? (`ollama serve`)"
        ) from exc

    if resp.status_code != 200:
        raise RuntimeError(
            f"Ollama chat failed (HTTP {resp.status_code}): {resp.text[:200]}"
        )

    for line in resp.iter_lines():
        if not line:
            continue
        data = json.loads(line)
        if "error" in data:
            raise RuntimeError(f"Ollama error: {data['error']}")
        token = data.get("message", {}).get("content", "")
        if token:
            yield token
        if data.get("done"):
            break


# ---------------------------------------------------------------------- Azure
def _azure_chat(messages: list[dict], settings: Settings) -> Iterator[str]:
    from openai import AzureOpenAI

    if not settings.azure_api_key or not settings.azure_endpoint:
        raise RuntimeError(
            "Azure chat needs AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY in .env."
        )

    client = AzureOpenAI(
        api_key=settings.azure_api_key,
        api_version=settings.azure_api_version,
        azure_endpoint=settings.azure_endpoint,
    )
    stream = client.chat.completions.create(
        model=settings.azure_chat_deployment,
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        if not chunk.choices:
            continue
        token = chunk.choices[0].delta.content
        if token:
            yield token


# --------------------------------------------------------------------- Claude
def _claude_chat(messages: list[dict], settings: Settings) -> Iterator[str]:
    import anthropic

    if not settings.anthropic_api_key:
        raise RuntimeError("Claude needs ANTHROPIC_API_KEY in .env.")

    # Anthropic keeps the system prompt separate from the message list.
    system_prompt = "\n\n".join(
        m["content"] for m in messages if m["role"] == "system"
    )
    convo = [m for m in messages if m["role"] in ("user", "assistant")]

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    with client.messages.stream(
        model=settings.anthropic_model,
        max_tokens=1024,
        system=system_prompt,
        messages=convo,
    ) as stream:
        for token in stream.text_stream:
            if token:
                yield token
