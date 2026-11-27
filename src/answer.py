import os

import chromadb
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

from config import (
    COLLECTION_NAME, DB_DIR, EMBED_MODEL, LLM_MODEL, MIN_SIMILARITY, TOP_K
)

load_dotenv()

SYSTEM_PROMPT = """You are Ceylon2US, an assistant helping people move from Sri Lanka to the United States.
Answer ONLY using the numbered sources provided. Do not use outside knowledge.
If the sources do not contain the answer, say you don't have that information yet.
Cite sources in square brackets like [1] or [2] after each fact.
Keep answers clear and short. For visa or legal topics, remind the user to verify on the official website."""


def retrieve(question, embedder, collection):
    """Find the closest chunks to the question."""
    query_embedding = embedder.encode([question]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=TOP_K)

    hits = []
    for doc, meta, dist in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        hits.append({"text": doc, **meta, "similarity": 1 - dist})
    return hits


def build_prompt(question, hits):
    """Put the numbered sources and the question together."""
    sources = []
    for i, hit in enumerate(hits, start=1):
        sources.append(
            f"[{i}] ({hit['source']}, p.{hit['page']}, checked {hit['checked']})\n{hit['text']}"
        )
    return "SOURCES:\n\n" + "\n\n".join(sources) + f"\n\nQUESTION: {question}"


def answer(question, embedder, collection, llm):
    """Retrieve, check confidence, then ask the LLM."""
    hits = retrieve(question, embedder, collection)
    good_hits = [hit for hit in hits if hit["similarity"] >= MIN_SIMILARITY]

    if not good_hits:
        return "Sorry, I don't have information on that yet. Try asking about SSNs, green cards or visas.", []

    response = llm.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_prompt(question, good_hits)},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content, good_hits


def main():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found. Add it to your .env file.")
        return

    embedder = SentenceTransformer(EMBED_MODEL)
    collection = chromadb.PersistentClient(path=DB_DIR).get_collection(COLLECTION_NAME)
    llm = Groq(api_key=api_key)

    while True:
        question = input("\n❓ Ask Ceylon2US (or 'quit'): ")
        if question.lower() == "quit":
            break

        reply, sources = answer(question, embedder, collection, llm)
        print(f"\n🤖 {reply}")

        if sources:
            print("\n📚 Sources:")
            for i, hit in enumerate(sources, start=1):
                print(f"  [{i}] {hit['source']} (p.{hit['page']}, checked {hit['checked']}, similarity {hit['similarity']:.2f})")


if __name__ == "__main__":
    main()
