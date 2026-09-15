import os
import glob
import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

load_dotenv()

ARTICLES_DIR = "articles"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 4
GROQ_MODEL = "llama3-8b-8192"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


@st.cache_resource(show_spinner="Loading and chunking articles...")
def load_and_chunk_articles(articles_dir: str):
    file_paths = glob.glob(os.path.join(articles_dir, "*.txt"))
    if not file_paths:
        return []

    all_docs = []
    for path in file_paths:
        loader = TextLoader(path, encoding="utf-8")
        all_docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(all_docs)
    return chunks


@st.cache_resource(show_spinner="Building embeddings + FAISS index...")
def build_vector_store(_chunks):
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vector_store = FAISS.from_documents(_chunks, embeddings)
    return vector_store


def retrieve_relevant_chunks(vector_store, query: str, k: int = TOP_K):
    results = vector_store.similarity_search(query, k=k)
    return results


def generate_insight(query: str, retrieved_chunks, api_key: str):
    if not api_key:
        return "⚠️ GROQ_API_KEY not set. Add it to your .env file to enable insight generation."

    context = "\n\n---\n\n".join(chunk.page_content for chunk in retrieved_chunks)

    prompt = f"""You are a news analyst. Use ONLY the context below to answer
the question. If the context does not contain the answer, say so honestly.

Context:
{context}

Question: {query}

Answer concisely, citing specific facts from the context where relevant."""

    llm = ChatGroq(api_key=api_key, model=GROQ_MODEL, temperature=0.2)
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content


def main():
    st.set_page_config(page_title="Article Analyzer", page_icon="📰")
    st.title("📰 LLM-Based Article Analyzer")
    st.caption("Semantic search + RAG insight extraction over news articles")

    chunks = load_and_chunk_articles(ARTICLES_DIR)

    if not chunks:
        st.warning(
            f"No articles found in `./{ARTICLES_DIR}/`. "
            f"Add some `.txt` files there and refresh."
        )
        return

    st.sidebar.metric("Articles chunks indexed", len(chunks))
    vector_store = build_vector_store(chunks)

    query = st.text_input("Ask a question about the articles:")

    if query:
        with st.spinner("Retrieving relevant chunks..."):
            retrieved = retrieve_relevant_chunks(vector_store, query)

        with st.expander("🔍 Retrieved chunks (semantic search results)"):
            for i, chunk in enumerate(retrieved, start=1):
                source = chunk.metadata.get("source", "unknown")
                st.markdown(f"**Chunk {i}** — *{source}*")
                st.write(chunk.page_content)
                st.divider()

        with st.spinner("Generating insight with LLaMA3 (Groq)..."):
            answer = generate_insight(query, retrieved, GROQ_API_KEY)

        st.subheader("💡 Insight")
        st.write(answer)


if __name__ == "__main__":
    main()
