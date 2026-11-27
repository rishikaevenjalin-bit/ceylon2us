import os

import chromadb
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

from answer import answer
from config import COLLECTION_NAME, DB_DIR, EMBED_MODEL

load_dotenv()

st.set_page_config(page_title="Ceylon2US", page_icon="🇺🇸")
st.title("🇱🇰➡️🇺🇸 Ceylon2US")
st.caption(
    "Your guide to moving from Sri Lanka to the US, answered from official sources. "
    "Always verify visa and legal information on official government websites."
)

if not os.getenv("GROQ_API_KEY"):
    st.error("GROQ_API_KEY not found. Add it to your .env file.")
    st.stop()


@st.cache_resource
def load_resources():
    embedder = SentenceTransformer(EMBED_MODEL)
    collection = chromadb.PersistentClient(path=DB_DIR).get_collection(COLLECTION_NAME)
    llm = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return embedder, collection, llm


embedder, collection, llm = load_resources()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask about SSNs, green cards, visas...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching official sources..."):
            reply, sources = answer(question, embedder, collection, llm)

        if sources:
            source_lines = [
                f"- [{i}] {hit['source']} (p.{hit['page']}, checked {hit['checked']})"
                for i, hit in enumerate(sources, start=1)
            ]
            reply += "\n\n**Sources:**\n" + "\n".join(source_lines)

        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})