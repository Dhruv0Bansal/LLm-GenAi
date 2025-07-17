import os
import streamlit as st
import pickle
import time
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_groq import ChatGroq
from langchain.document_loaders import PyPDFLoader, UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate

# Load Groq-hosted LLaMA 3 model
llm = ChatGroq(
    api_key="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",
    model_name="llama3-8b-8192"
)

# Use HuggingFace for embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Streamlit UI
st.title("📰 Research Tool with LLaMA3")
st.sidebar.title("Enter up to 3 News Article URLs")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

urls = [u for u in urls if u]  # Remove blanks
process_url_click = st.sidebar.button("🔍 Analyze URLs")
reset = st.sidebar.button("🔁 Reset Session")
if reset:
    st.session_state.retriever = None
    st.rerun()

if process_url_click:
    with st.spinner("Loading and analyzing..."):
        loader = UnstructuredURLLoader(urls=urls)
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(data)
        db = FAISS.from_documents(docs, embeddings)
        retriever = db.as_retriever(search_kwargs={"k": 3})
        chain = RetrievalQAWithSourcesChain.from_chain_type(llm, retriever=retriever)

        response = chain({"question": "What is the main idea of the article?"})

        st.subheader("🧠 Answer")
        st.write(response["answer"])
        st.subheader("🔗 Sources")
        st.write(response["sources"])
