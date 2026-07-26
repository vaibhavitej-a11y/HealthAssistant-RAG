# 🏥 Health Transformation Knowledge Assistant

> An end-to-end Retrieval-Augmented Generation (RAG) application that answers questions about **India's Health Transformation** using semantic search over the official Press Information Bureau (PIB) document.

---

## 📌 Project Overview

This project implements a complete **Retrieval-Augmented Generation (RAG)** pipeline that enables users to ask natural language questions about India's Health Transformation initiatives.

Instead of relying solely on an LLM's internal knowledge, the system first retrieves the most relevant information from the provided PIB document using **semantic vector search**, then generates an answer grounded entirely in the retrieved context.

The result is a more reliable, explainable, and document-aware question answering system.

---

## ✨ Features

- 📄 Automated document ingestion from the official PIB webpage
- ✂️ Intelligent document chunking for efficient retrieval
- 🧠 Semantic embeddings using SentenceTransformers
- 🗂️ Vector storage with ChromaDB
- 🔎 Semantic similarity search
- 🤖 Grounded answer generation using Google Gemini 2.5 Flash
- 🌐 Interactive Streamlit web interface
- 📚 Supporting evidence displayed alongside every answer

---

## 🏗️ System Architecture

```text
                  PIB Webpage
                       │
                       ▼
             HTML Extraction (BeautifulSoup)
                       │
                       ▼
              Document Chunking (~350 words)
                       │
                       ▼
      SentenceTransformer Embeddings
                       │
                       ▼
             ChromaDB Vector Database
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
 User Question                Query Embedding
         │                           │
         └─────────────┬─────────────┘
                       ▼
             Semantic Similarity Search
                       │
               Top Relevant Chunks
                       │
                       ▼
             Gemini 2.5 Flash (RAG)
                       │
                       ▼
              Grounded Final Answer
```

---

# ⚙️ Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python |
| UI | Streamlit |
| Web Scraping | BeautifulSoup + Requests |
| Embedding Model | all-MiniLM-L6-v2 (SentenceTransformers) |
| Vector Database | ChromaDB |
| LLM | Google Gemini 2.5 Flash |
| Environment | python-dotenv |

---

# 📂 Project Structure

```text
health-rag-assistant/
│
├── app.py                 # Streamlit Interface
├── rag.py                 # RAG Pipeline
├── ingest.py              # PIB Document Extraction
├── implementation.md      # Design Decisions
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── document.txt
│
└── chroma_db/
```

---

# 🚀 How It Works

## Step 1 — Document Ingestion

The official **India's Health Transformation** PIB webpage is downloaded and converted into plain text using **BeautifulSoup**.

---

## Step 2 — Document Chunking

The extracted document is split into approximately **350-word chunks**.

Each chunk represents a meaningful section of the document while preserving enough context for semantic retrieval.

---

## Step 3 — Embedding Generation

Each chunk is converted into a dense semantic vector using:

> **SentenceTransformer**
>
> `all-MiniLM-L6-v2`

These embeddings capture semantic meaning rather than exact keyword matches.

---

## Step 4 — Vector Storage

The generated embeddings are stored inside **ChromaDB**.

This enables efficient nearest-neighbor similarity search for user queries.

---

## Step 5 — Semantic Retrieval

When a user asks a question:

1. The query is embedded.
2. ChromaDB searches for the most semantically similar chunks.
3. The top retrieved chunks become contextual knowledge.

---

## Step 6 — Retrieval-Augmented Generation

The retrieved context and the user's question are combined into a prompt and sent to **Gemini 2.5 Flash**.

The model is explicitly instructed to:

- Answer only from the retrieved context.
- Avoid hallucinating information.
- Return concise, grounded responses.

---

# 🖥️ User Interface

The project includes a lightweight **Streamlit** interface where users can:

- Ask questions in natural language
- View AI-generated answers
- Inspect supporting evidence retrieved from the knowledge base

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/health-rag-assistant.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

# ▶️ Running the Project

### 1. Extract the document

```bash
python ingest.py
```

### 2. Build the vector database

```bash
python rag.py
```

### 3. Launch the application

```bash
streamlit run app.py
```

---

# 📖 Example Questions

- What is PM-JAY?
- What are Ayushman Arogya Mandirs?
- What is ABDM?
- What initiatives were launched under NHM?
- How has India's healthcare infrastructure improved?

---

# 💡 Design Decisions

### Why SentenceTransformers?

- Fast
- Lightweight
- Excellent semantic retrieval performance
- No embedding API costs

---

### Why ChromaDB?

- Easy local vector database
- Persistent storage
- Fast similarity search
- Perfect for small-to-medium RAG applications

---

### Why Gemini 2.5 Flash?

- Fast response generation
- Strong reasoning capability
- Excellent instruction following
- Cost-effective for RAG workflows

---

# 🔮 Future Improvements

- Multi-document knowledge base
- PDF upload support
- Semantic chunking
- Metadata filtering
- Source citation highlighting
- Retrieval score visualization
- Conversational memory

---

# 📚 Source Document

**Press Information Bureau**

**India's Health Transformation**

https://www.pib.gov.in/PressReleasePage.aspx?PRID=2269699&reg=48&lang=2

---

# 👩‍💻 Author

**E. Vaibhavi Tej**

AI & ML Undergraduate

Python • Generative AI • RAG • AI Agents • Cloud

---

## ⭐ Highlights

- End-to-end RAG implementation
- Semantic search over vector embeddings
- Grounded LLM responses
- Clean and modular architecture
- Interactive web interface
- Production-style project organization