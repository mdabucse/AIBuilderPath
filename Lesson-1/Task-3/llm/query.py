import faiss
import json
from embeddings.model import get_embedding_model

def retrieve_relevant_chunks(query, top_k=3):
    ''' Retrieve relevant chunks from FAISS index based on query '''
    index = faiss.read_index("rag_index.faiss")
    with open("rag_chunks.json", "r") as f:
        chunks = json.load(f)
    
    model = get_embedding_model()
    query_vec = model.encode([query])
    distances, indices = index.search(query_vec, top_k)
    
    return [chunks[i] for i in indices[0]]
