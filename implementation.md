# Implementation Notes

## Project Overview

This project implements a Retrieval-Augmented Generation (RAG) system that answers questions about **India's Health Transformation** using the official Press Information Bureau (PIB) article.

Rather than relying only on the language model's built-in knowledge, the application retrieves the most relevant information from the source document and uses it as context to generate grounded, document-based responses.

---

# System Workflow

1. Download the PIB webpage using `requests`.
2. Extract the main article content using BeautifulSoup.
3. Divide the document into semantic sections based on headings and paragraphs.
4. Generate embeddings for each section using SentenceTransformers.
5. Store the embeddings and metadata in ChromaDB.
6. Convert the user's question into an embedding.
7. Retrieve the most relevant sections using cosine similarity search.
8. Provide the retrieved context to Gemini 2.5 Flash.
9. Display the generated answer along with the supporting evidence.

---

# Embedding Model Choice

The project uses **SentenceTransformers (`all-MiniLM-L6-v2`)**.

### Why this model?

- Produces high-quality semantic embeddings.
- Lightweight and fast to run locally.
- Well-suited for small and medium-sized RAG applications.
- Open-source and does not require an embedding API.

The same model is used to embed both the document sections and user queries, allowing them to be compared in the same vector space.

---

# Embedding Storage and Index

Embeddings are stored using **ChromaDB**, a lightweight vector database.

Each stored record contains:

- Section text
- Section title
- Display title (used in the Streamlit interface)
- Embedding vector

The collection is configured to use **cosine similarity**, which measures semantic closeness between the query and document embeddings.

ChromaDB provides persistent storage, allowing the embeddings to be generated once and reused across application runs.

---

# LLM and Prompt Design

Google **Gemini 2.5 Flash** is used as the language model.

For each query, the application constructs a prompt containing:

- The retrieved document sections
- The user's question
- Instructions to answer only using the provided context

The prompt also instructs the model to avoid making unsupported claims. If the answer cannot be found in the retrieved context, the model is expected to state that the information is unavailable.

This prompt design helps reduce hallucinations and keeps responses grounded in the source document.

---

# What I Learned During This Assignment

While completing this project, I explored several concepts that were new to me:

- Building a complete Retrieval-Augmented Generation (RAG) pipeline.
- Generating semantic embeddings using SentenceTransformers.
- Storing and querying embeddings with ChromaDB.
- Designing prompts that encourage grounded responses.
- Improving retrieval quality through semantic section-based chunking instead of fixed-size chunks.
- Using metadata to improve both retrieval and user interface presentation.

---

# Limitations

Current limitations include:

- Supports only a single source document.
- Retrieval quality depends on the embedding model.
- Does not rerank retrieved results.
- No conversational memory between questions.
- Does not highlight the exact text used to generate the answer.

---

# Improvements With Two More Days

Given additional development time, I would:

- Support multiple documents.
- Implement hybrid keyword + semantic retrieval.
- Add a reranking stage to improve retrieval accuracy.
- Highlight the exact passages used to generate each answer.
- Support PDF uploads.
- Add conversational memory for follow-up questions.

---

# Conclusion

This project demonstrates an end-to-end RAG workflow, including document ingestion, semantic chunking, embedding generation, vector search, and grounded answer generation through an interactive Streamlit application.