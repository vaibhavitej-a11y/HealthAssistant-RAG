# Implementation Notes

## Project Overview

This project implements a Retrieval-Augmented Generation (RAG) system for answering questions about India's Health Transformation initiatives using a Press Information Bureau (PIB) document.

Instead of relying only on the language model's knowledge, the application retrieves relevant information from the provided document before generating an answer.

---

## Workflow

1. Download the PIB webpage.
2. Extract the webpage text using BeautifulSoup.
3. Split the document into fixed-size chunks (350 words).
4. Generate embeddings using SentenceTransformers (`all-MiniLM-L6-v2`).
5. Store embeddings in ChromaDB.
6. Perform semantic search for the user's question.
7. Retrieve the top relevant chunks.
8. Generate a grounded answer using Gemini 2.5 Flash.

---

## Technologies Used

- Python
- Streamlit
- ChromaDB
- SentenceTransformers
- Google Gemini 2.5 Flash
- BeautifulSoup
- Requests

---

## Chunking Strategy

The document is divided into fixed-size chunks of approximately 350 words. This approach provides sufficient context while maintaining efficient semantic retrieval.

---

## Embedding Model

The project uses the `all-MiniLM-L6-v2` SentenceTransformer model to generate dense vector embeddings for each document chunk and user query.

---

## Vector Database

ChromaDB is used as the vector database to store embeddings and perform similarity search.

---

## Retrieval Process

For every user question:

- Generate the query embedding.
- Search ChromaDB.
- Retrieve the top three most relevant chunks.

These retrieved chunks are provided as context to the language model.

---

## Answer Generation

Google Gemini 2.5 Flash receives:

- User question
- Retrieved context

The model is instructed to answer only from the retrieved document. If sufficient information is unavailable, it responds accordingly instead of generating unsupported information.

---

## User Interface

A simple Streamlit interface allows users to:

- Enter questions
- View AI-generated answers
- Inspect the retrieved supporting evidence

---

## Limitations

- Supports a single source document.
- Uses fixed-size chunking.
- No conversational memory between questions.

---

## Future Improvements

- Support multiple documents.
- Add PDF upload functionality.
- Implement metadata filtering.
- Improve chunking with semantic segmentation.
- Display similarity scores for retrieved chunks.