import chromadb
from sentence_transformers import SentenceTransformer

from config import COLLECTION_NAME, DB_DIR, EMBED_MODEL
from ingest import build_chunks


def main():
    chunks = build_chunks()
    texts = [chunk["text"] for chunk in chunks]
    print(f"Embedding {len(texts)} chunks...")

    model = SentenceTransformer(EMBED_MODEL)
    embeddings = model.encode(texts, show_progress_bar=True)

    client = chromadb.PersistentClient(path=DB_DIR)
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(
        COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )

    collection.add(
        ids=[chunk["id"] for chunk in chunks],
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[
            {"source": c["source"], "page": c["page"], "checked": c["checked"]}
            for c in chunks
        ],
    )
    print(f"✅ Stored {collection.count()} chunks in {DB_DIR}/")


if __name__ == "__main__":
    main()
