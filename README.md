# LLM-Based Article Analyzer with Semantic Search

A single-file RAG (Retrieval-Augmented Generation) backend pipeline for
semantic search and automated insight extraction over news articles.

## How it works

1. **Ingestion** — loads `.txt` articles from `./articles`
2. **Chunking** — splits articles into overlapping 500-character chunks
   (`RecursiveCharacterTextSplitter`) so embeddings stay precise and fit
   within the LLM's context window
3. **Embedding** — each chunk is converted into a vector using a
   HuggingFace sentence-transformer model (`all-MiniLM-L6-v2`)
4. **Indexing** — all chunk embeddings are stored in a FAISS index for
   fast similarity search
5. **Retrieval** — a user's query is embedded the same way, and FAISS
   returns the top-k most semantically similar chunks
6. **Generation (RAG)** — the retrieved chunks + the query are passed to
   LLaMA3, served via Groq's low-latency inference API, to generate a
   grounded answer
7. **UI** — a Streamlit app exposes a search box and shows both the
   retrieved chunks and the generated insight

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

Drop your own `.txt` news articles into the `articles/` folder (a couple
of samples are included so it runs out of the box).

## Run

```bash
streamlit run app.py
```

## Notes on design choices

- **Chunk size (500 chars, 50 overlap):** small enough for accurate
  embeddings, large enough to preserve context; overlap prevents losing
  meaning at chunk boundaries.
- **all-MiniLM-L6-v2:** lightweight (384-dim) embedding model — fast on
  CPU, good enough accuracy for a project at this scale.
- **FAISS (flat index):** in-process, no separate server needed; exact
  similarity search is fine at this dataset size.
- **Groq + LLaMA3:** open-source model, low-latency inference, no
  per-token cost — good fit for a personal project.
