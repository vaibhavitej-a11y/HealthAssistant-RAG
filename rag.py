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

import re

MIN_WORDS = 200
MAX_WORDS = 500
TARGET_WORDS = 350


def is_heading(line):
    """
    Detects actual section headings in the document.
    """

    line = line.strip()

    if not line:
        return False

    # Too long to be a heading
    if len(line.split()) > 12:
        return False

    # Most body text ends with punctuation
    if line.endswith((".", ";", "?", "!")):
        return False

    # Ignore statistics / bullets that start with numbers
    if line[0].isdigit():
        return False

    # Require title-like capitalization
    words = line.split()

    capitalized = sum(
        word[0].isupper()
        for word in words
        if word and word[0].isalpha()
    )

    return capitalized >= max(2, len(words) // 2)


def chunk_document(text):
    """
    Creates semantic chunks based on section headings.
    Large sections are split into multiple chunks while
    keeping paragraphs together.
    """

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    sections = []

    current_title = "Introduction"
    current_paragraphs = []

    # ----------------------------
    # Build sections
    # ----------------------------

    for line in lines:

        if is_heading(line):

            if current_paragraphs:

                sections.append(
                    {
                        "title": current_title,
                        "paragraphs": current_paragraphs
                    }
                )

            current_title = line
            current_paragraphs = []

        else:
            current_paragraphs.append(line)

    if current_paragraphs:
        sections.append(
            {
                "title": current_title,
                "paragraphs": current_paragraphs
            }
        )

    # ----------------------------
    # Split sections into chunks
    # ----------------------------

    chunks = []

    for section in sections:

        title = section["title"]

        paragraphs = section["paragraphs"]

        current_chunk = []

        current_word_count = 0

        part = 1

        for paragraph in paragraphs:

            paragraph_words = len(paragraph.split())

            # Start a new chunk if adding this paragraph exceeds max size
            if (
                current_chunk
                and current_word_count + paragraph_words > MAX_WORDS
            ):

                chunk_title = (
                    title
                    if part == 1
                    else f"{title} (Part {part})"
                )

                chunks.append(
                    {
                        "id": f"chunk_{len(chunks)+1}",
                        "title": chunk_title,
                        "text": f"Section: {chunk_title}\n\n"
                        + "\n\n".join(current_chunk),
                    }
                )

                part += 1

                current_chunk = []

                current_word_count = 0

            current_chunk.append(paragraph)

            current_word_count += paragraph_words

        if current_chunk:

            chunk_title = (
                title
                if part == 1
                else f"{title} (Part {part})"
            )

            chunks.append(
                {
                    "id": f"chunk_{len(chunks)+1}",
                    "title": chunk_title,
                    "text": f"Section: {chunk_title}\n\n"
                    + "\n\n".join(current_chunk),
                }
            )

    print(f"\nCreated {len(chunks)} semantic chunks.\n")

    return chunks


# ----------------------------
# Build Vector Database
# ----------------------------

def get_display_title(title):
    if "Ayushman Arogya Mandir" in title:
        return "Ayushman Arogya Mandirs"

    if "Tele-MANAS" in title:
        return "Tele-MANAS"

    if "Ayushman Bharat Digital Mission" in title or "ABDM" in title:
        return "ABDM"

    if "Ayushman App" in title:
        return "Ayushman App"

    if "eSanjeevani" in title:
        return "eSanjeevani"

    if "Jan Aushadhi" in title:
        return "Jan Aushadhi"

    if ":" in title:
        return title.split(":", 1)[1].strip()

    return title

def build_vector_db(chunks):

    client_db = chromadb.PersistentClient(path="chroma_db")

    try:
        client_db.delete_collection("health_rag")
    except:
        pass

    collection = client_db.get_or_create_collection(
        name="health_rag",
        metadata={"hnsw:space": "cosine"}
    )

    for chunk in chunks:

        embedding = model.encode(chunk["text"]).tolist()

        collection.add(
            ids=[chunk["id"]],
            embeddings=[embedding],
            documents=[chunk["text"]],
            metadatas=[
                {
                    "title": chunk["title"],
                    "display_title": get_display_title(chunk["title"])
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
        retrieved_metadata = results["metadatas"][0]

        answer = generate_answer(question, retrieved_docs)

        print("\n==============================")
        print("ANSWER")
        print("==============================\n")

        print(answer)

        print("\n==============================")
        print("RETRIEVED CHUNKS")
        print("==============================\n")

        for meta, doc in zip(retrieved_metadata, retrieved_docs):
            print(f"Section: {meta['title']}")
            print("-" * 50)
            print(doc[:250])
            print()