from preprocessing.pdf_to_text_extractor import pdf_to_text
from preprocessing.chunker import chunk_text
from embeddings.embedding import embed_and_index
from llm.query import retrieve_relevant_chunks
from llm.model import llm
import warnings

def main(path,query):
    ''' the main function to run the RAG pipeline '''
    warnings.filterwarnings("ignore") 
    pdf_to_text("data/Trip.pdf")
    with open("data/data.txt", "r") as f:
        text = f.read()
    chunks = chunk_text(text)
    embed_and_index(chunks)
    relevant_chunks = retrieve_relevant_chunks(query)
    answer = llm(query, relevant_chunks)
    print("Answer:", answer)

    
if __name__ == "__main__":
    while True:
        query = input("\nEnter your question (or type 'exit' to quit): ")
        if query.lower() == "exit":
            break
        else:
            main("data/Trip.pdf", query)   
        
        