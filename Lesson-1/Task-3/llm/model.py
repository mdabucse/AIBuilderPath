import requests

def llm(query, context_chunks, model="phi3"):
    ''' Query the LLM with the retrieved context chunks '''
    context = "\n\n".join(context_chunks)

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a strict assistant. "
                        "Answer ONLY using the provided context. "
                        "If the answer is not in the context, say 'I don't know'."
                    )
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion:\n{query}"
                }
            ],
            "stream": False
        }
    )

    return response.json()["message"]["content"]