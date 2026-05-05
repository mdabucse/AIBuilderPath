from sentence_transformers import SentenceTransformer

# Initialize model once and reuse it
_model = None

def get_embedding_model():
    """Get or initialize the embedding model (singleton pattern)"""
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model
