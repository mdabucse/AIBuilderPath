import faiss
import numpy as np
import json
from embeddings.model import get_embedding_model

def embed_and_index(chunks):
    '''Embed chunks and create FAISS index'''
    model = get_embedding_model()

    # Embed all chunks
    embeddings = model.encode(chunks)

    # Create FAISS index
    dimension = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    # Save for future use
    faiss.write_index(index, "rag_index.faiss")
    with open("rag_chunks.json", "w") as f:
        json.dump(chunks, f)