from pathlib import Path
import os

import chromadb
from dotenv import load_dotenv
from google import genai
from sentence_transformers import SentenceTransformer

# ----------------------------
# Configuration
# ----------------------------

load_dotenv()

DOCUMENT_PATH = "data/document.txt"

# Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Local Embedding Model
model = SentenceTransformer("all-MiniLM-L6-v2")


# ----------------------------
# Load Document
# ----------------------------

def load_document():
    return Path(DOCUMENT_PATH).read_text(encoding="utf-8")


# ----------------------------
# Chunk Document
# ----------------------------

def chunk_document(text, chunk_size=350):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):

        chunk = " ".join(words[i:i + chunk_size])

        chunks.append({
            "id": f"chunk_{len(chunks)+1}",
            "chunk_number": len(chunks)+1,
            "text": chunk
        })

    return chunks


# ----------------------------
# Build Vector Database
# ----------------------------

def build_vector_db(chunks):

    client_db = chromadb.PersistentClient(path="chroma_db")

    try:
        client_db.delete_collection("health_rag")
    except:
        pass

    collection = client_db.get_or_create_collection("health_rag")

    for chunk in chunks:

        embedding = model.encode(chunk["text"]).tolist()

        collection.add(
            ids=[chunk["id"]],
            embeddings=[embedding],
            documents=[chunk["text"]],
            metadatas=[
                {
                    "chunk_number": chunk["chunk_number"]
                }
            ]
        )

    return collection


# ----------------------------
# Semantic Search
# ----------------------------

def search_chunks(collection, query, top_k=3):

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results

def load_vector_db():
    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_collection("health_rag")
    return collection

# ----------------------------
# Gemini Answer
# ----------------------------

def generate_answer(question, retrieved_chunks):

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are an AI assistant.

Answer ONLY using the context below.

If the answer cannot be found in the context,
say:

"I couldn't find that information in the provided document."

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text




# ----------------------------
# Main
# ----------------------------

if __name__ == "__main__":

    text = load_document()

    chunks = chunk_document(text)

    collection = build_vector_db(chunks)

    print("\n✅ Knowledge Base Ready!")

    while True:

        question = input("\nAsk a question (or type exit): ")

        if question.lower() == "exit":
            break

        results = search_chunks(collection, question)

        retrieved_docs = results["documents"][0]

        answer = generate_answer(question, retrieved_docs)

        print("\n==============================")
        print("ANSWER")
        print("==============================\n")

        print(answer)

        print("\n==============================")
        print("RETRIEVED CHUNKS")
        print("==============================\n")

        for i, doc in enumerate(retrieved_docs, start=1):
            print(f"Chunk {i}")
            print("-" * 40)
            print(doc[:200])
            print()