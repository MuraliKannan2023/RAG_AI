# RAG AI — Project Overview

## What is RAG?

**RAG (Retrieval-Augmented Generation)** is a technique that combines:
1. **Retrieval** — Finding relevant information from your documents
2. **Generation** — Using an AI model to generate human-readable answers

Instead of feeding an entire document to an AI, RAG **retrieves only the relevant parts** and generates an answer from them. This is faster, cheaper, and more accurate.

---

## Project Purpose

This project reads your **payslip PDF**, stores it in a **vector database**, and lets you **ask questions** about it in natural language.

**Example:**
```
User:   "What is my basic salary?"
System: "Based on the payslip, your basic salary is ₹18,158.00"
```

---

## Tech Stack

| Component       | Provider       | Model/Service                  | Cost   |
|-----------------|----------------|--------------------------------|--------|
| PDF Reader      | pypdf          | Local Python library           | Free   |
| Text Chunker    | Custom code    | Sliding window with overlap    | Free   |
| Embeddings      | Google Gemini  | `gemini-embedding-001` (768d)  | Free   |
| Vector Database | Pinecone       | Serverless (AWS us-east-1)     | Free   |
| LLM (Answers)   | Groq           | `llama-3.3-70b-versatile`      | Free   |

**Total Cost: $0** — Entirely free stack!

---

## Project Structure

```
RAG AI/
├── .env                  ← API keys (Google, Pinecone, Groq)
├── requirements.txt      ← Python dependencies
├── pdfreader.py          ← Step 1: Read PDF text
├── chunker.py            ← Step 2: Split text into overlapping chunks
├── embedder.py           ← Step 3: Convert text chunks into vector embeddings
├── vectorstore.py        ← Step 4: Store & search vectors in Pinecone
├── llm.py                ← Step 5: Generate answer using Groq LLM
├── dataprocessor.py      ← INDEXING pipeline (run once to store data)
├── QueryProcessor.py     ← QUERY pipeline (run per user question)
├── chunking_explained.md ← Documentation: How chunking works
├── PROJECT_OVERVIEW.md   ← This file
└── pdf_file/
    └── MuraliPDF.pdf     ← Source document (payslip)
```

---

## Two Pipelines

### Pipeline 1: Indexing (run ONCE)

**File:** `dataprocessor.py`

This pipeline processes your PDF and stores it in the vector database. You only need to run it once per document.

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ pdfreader.py │    │ chunker.py   │    │ embedder.py  │    │vectorstore.py│
│              │    │              │    │              │    │              │
│ Read PDF     │───▶│ Split into   │───▶│ Convert to   │───▶│ Store in     │
│ Extract text │    │ chunks       │    │ vectors      │    │ Pinecone     │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
     pypdf            900 chars/chunk     Gemini API          Pinecone DB
                      150 char overlap    768 dimensions       cosine metric
```

**Steps:**
1. `pdfreader.py` — Reads `MuraliPDF.pdf` and extracts text (1 string per page)
2. `chunker.py` — Splits the text into overlapping chunks (900 chars, 150 overlap)
3. `embedder.py` — Sends each chunk to Google Gemini → gets back 768 numbers per chunk
4. `vectorstore.py` — Uploads vectors + original text to Pinecone

**Run command:**
```bash
python dataprocessor.py
```

---

### Pipeline 2: Query (run per question)

**File:** `QueryProcessor.py`

This pipeline answers user questions by finding relevant chunks and generating a response.

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ embedder.py  │    │vectorstore.py│    │   llm.py     │
│              │    │              │    │              │
│ Embed query  │───▶│ Search       │───▶│ Generate     │
│ → 768 nums   │    │ Pinecone     │    │ answer       │
└──────────────┘    └──────────────┘    └──────────────┘
  Gemini API          Find top 4          Groq + Llama 3.3
                      closest matches     Human-readable answer
```

**Steps:**
1. `embedder.py` — Converts the user's question into 768 numbers
2. `vectorstore.py` — Searches Pinecone for the most similar chunks
3. `llm.py` — Sends the question + matched chunks to Groq → gets a natural answer

**Run command:**
```bash
python QueryProcessor.py
```

---

## File Details

### `pdfreader.py`
- **Library:** `pypdf`
- **Input:** Path to a PDF file
- **Output:** List of strings (one per page)
- **Validation:** Checks if the file exists before attempting to read

### `chunker.py`
- **Method:** Sliding window
- **chunk_size:** 900 characters (maximum per chunk)
- **chunk_overlap:** 150 characters (shared between consecutive chunks)
- **Why overlap?** Prevents sentences from being cut in half at chunk boundaries
- **Your payslip:** 1,271 characters → 2 chunks

### `embedder.py`
- **Provider:** Google Gemini (free)
- **Model:** `gemini-embedding-001`
- **Output dimensions:** 768 (configured via `output_dimensionality`)
- **Two functions:**
  - `embed_chunks()` — Embeds document chunks (for indexing)
  - `embed_User_query()` — Embeds user questions (for searching)

### `vectorstore.py`
- **Provider:** Pinecone (free tier)
- **Index:** `rag-ai-gemini-embedding-001`
- **Config:** 768 dimensions, cosine similarity, Dense vectors
- **Region:** AWS us-east-1
- **Two functions:**
  - `store_in_pinecone()` — Upserts vectors with metadata (batch size: 100)
  - `search_in_pinecone()` — Queries top-k similar vectors

### `llm.py`
- **Provider:** Groq (free, 14,400 requests/day)
- **Model:** `llama-3.3-70b-versatile`
- **Temperature:** 0.4 (balanced between accuracy and creativity)
- **System prompt:** Answer only from provided context, don't assume

### `dataprocessor.py`
- **Purpose:** Orchestrates the indexing pipeline
- **Calls:** pdfreader → chunker → embedder → vectorstore
- **Run:** Once per document

### `QueryProcessor.py`
- **Purpose:** Orchestrates the query pipeline
- **Calls:** embedder → vectorstore → llm
- **Run:** Every time a user asks a question

---

## API Keys Required (in `.env`)

| Variable             | Service                  | How to get                                |
|----------------------|--------------------------|-------------------------------------------|
| `GOOGLE_API_KEY`     | Gemini embeddings        | https://aistudio.google.com/app/apikey    |
| `PINECONE_API_KEY`   | Vector database          | https://app.pinecone.io → API Keys        |
| `PINECONE_INDEX_NAME`| Pinecone index name      | From Pinecone console                     |
| `GROQ_API_KEY`       | LLM answer generation    | https://console.groq.com/keys             |

---

## Data Flow Example

```
User asks: "What is my basic salary?"

Step 1 — Embed the question (embedder.py + Gemini):
   "What is my basic salary?" → [0.019, -0.087, 0.039, ...]  (768 numbers)

Step 2 — Search Pinecone (vectorstore.py):
   Compare query vector with stored vectors:
   - chunk_0: similarity = 0.95 ← BEST MATCH
   - chunk_1: similarity = 0.42
   Returns chunk_0 text: "ebm-papst...BASIC 18,158.00...HRA 9,079.00..."

Step 3 — Generate answer (llm.py + Groq):
   Input:  Question + Matching chunk text
   Output: "Based on your payslip, your basic salary is ₹18,158.00"
```

---

## Key Concepts

### What is an Embedding?
A list of numbers (768 in our case) that represents the **meaning** of text. Similar texts have similar numbers, allowing mathematical comparison.

### What is Chunking?
Splitting large text into smaller pieces so the embedding model and LLM can process them. Overlap prevents information loss at boundaries.

### What is Cosine Similarity?
A mathematical measure of how similar two vectors are. Score ranges from 0 (completely different) to 1 (identical meaning).

### What is Upsert?
**Up**date + In**sert** — if a vector ID already exists, update it; if not, insert it as new.

---

## Dependencies

```
pypdf              — Read PDF files
google-genai        — Google Gemini API (embeddings)
pinecone            — Pinecone vector database
python-dotenv       — Load .env file variables
groq                — Groq API (LLM)
```

Install all:
```bash
pip install pypdf google-genai pinecone python-dotenv groq
```

---

## Quick Start

1. **Set up `.env`** with your API keys
2. **Index your PDF:**
   ```bash
   python dataprocessor.py
   ```
3. **Ask questions:**
   ```bash
   python QueryProcessor.py
   ```

---

## Architecture Diagram

```
                        ┌─────────────────────────┐
                        │       .env               │
                        │  GOOGLE_API_KEY          │
                        │  PINECONE_API_KEY        │
                        │  GROQ_API_KEY            │
                        └────────┬────────────────┘
                                 │ (loaded by all files)
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐    ┌───────────────────┐    ┌───────────────┐
│ Google Gemini │    │    Pinecone DB    │    │     Groq      │
│ (Embeddings)  │    │ (Vector Storage)  │    │ (LLM Answers) │
│               │    │                   │    │               │
│ gemini-       │    │ rag-ai-gemini-    │    │ llama-3.3-    │
│ embedding-001 │    │ embedding-001     │    │ 70b-versatile │
└───────┬───────┘    └────────┬──────────┘    └───────┬───────┘
        │                     │                       │
        │    ┌────────────────┼───────────────┐       │
        │    │                │               │       │
        ▼    ▼                ▼               ▼       ▼
┌──────────────────────────────────────────────────────────┐
│                     Python Code                          │
│                                                          │
│  pdfreader.py → chunker.py → embedder.py → vectorstore  │
│                                                          │
│  QueryProcessor.py: embedder → vectorstore → llm.py     │
└──────────────────────────────────────────────────────────┘
```
