"""Build (or rebuild) the vector index from the documents in `data/`.

Optional helper — the Streamlit app builds the index on first run too, but this
is handy for the command line:

    python ingest.py
"""

from rag import Settings
from rag.pipeline import build_index


def main() -> None:
    settings = Settings.from_env()
    print(f"Embedding backend : {settings.embed_backend} "
          f"({settings.ollama_embed_model if settings.embed_backend == 'ollama' else settings.azure_embed_deployment})")
    print(f"Reading documents from: {settings.data_path}")

    store = build_index(settings)

    print(f"Built index with {store.size} chunks.")
    print(f"Saved to: {settings.index_path}")


if __name__ == "__main__":
    main()
