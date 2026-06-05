"""Turn text into embedding vectors via a switchable backend.

    EMBED_BACKEND = ollama   -> local model through the Ollama HTTP API
    EMBED_BACKEND = azure    -> Azure OpenAI embeddings deployment

Both return a ``np.ndarray`` of shape ``(len(texts), dim)``.
"""

from __future__ import annotations

import numpy as np

from .config import Settings


def embed_texts(texts: list[str], settings: Settings) -> np.ndarray:
    """Embed a list of strings using the configured backend."""
    if not texts:
        return np.zeros((0, 0), dtype=np.float32)

    backend = settings.embed_backend
    if backend == "ollama":
        return _ollama_embed(texts, settings)
    if backend == "azure":
        return _azure_embed(texts, settings)
    raise ValueError(
        f"Unknown EMBED_BACKEND '{backend}'. Use 'ollama' or 'azure'."
    )


def embed_query(text: str, settings: Settings) -> np.ndarray:
    """Embed a single query string -> 1-D vector."""
    return embed_texts([text], settings)[0]


# --------------------------------------------------------------------- Ollama
def _ollama_embed(texts: list[str], settings: Settings) -> np.ndarray:
    import requests

    base = settings.ollama_base_url.rstrip("/")
    model = settings.ollama_embed_model

    try:
        # Newer Ollama: batch endpoint that accepts a list of inputs.
        resp = requests.post(
            f"{base}/api/embed",
            json={"model": model, "input": texts},
            timeout=600,
        )
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            f"Could not reach Ollama at {base}. Is it running? (`ollama serve`)"
        ) from exc

    if resp.status_code == 200 and "embeddings" in resp.json():
        return np.array(resp.json()["embeddings"], dtype=np.float32)

    # Older Ollama: one request per text via /api/embeddings.
    vectors: list[list[float]] = []
    for text in texts:
        r = requests.post(
            f"{base}/api/embeddings",
            json={"model": model, "prompt": text},
            timeout=600,
        )
        if r.status_code != 200 or "embedding" not in r.json():
            raise RuntimeError(_ollama_error(r, model))
        vectors.append(r.json()["embedding"])
    return np.array(vectors, dtype=np.float32)


def _ollama_error(resp, model: str) -> str:
    detail = ""
    try:
        detail = resp.json().get("error", "")
    except Exception:
        detail = resp.text[:200]
    if "not found" in detail.lower():
        return (
            f"Ollama model '{model}' is not installed. "
            f"Pull it first:  ollama pull {model}"
        )
    return f"Ollama embeddings failed (HTTP {resp.status_code}): {detail}"


# ---------------------------------------------------------------------- Azure
def _azure_embed(texts: list[str], settings: Settings) -> np.ndarray:
    from openai import AzureOpenAI

    if not settings.azure_api_key or not settings.azure_endpoint:
        raise RuntimeError(
            "Azure embeddings need AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY in .env."
        )

    client = AzureOpenAI(
        api_key=settings.azure_api_key,
        api_version=settings.azure_api_version,
        azure_endpoint=settings.azure_endpoint,
    )
    resp = client.embeddings.create(
        model=settings.azure_embed_deployment, input=texts
    )
    # Preserve request order.
    ordered = sorted(resp.data, key=lambda d: d.index)
    return np.array([d.embedding for d in ordered], dtype=np.float32)
