import chromadb
from sentence_transformers import SentenceTransformer

from config import COLLECTION_NAME, DB_DIR, EMBED_MODEL


def main():
    model = SentenceTransformer(EMBED_MODEL)
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_collection(COLLECTION_NAME)

    while True:
        question = input("\n❓ Ask a question (or 'quit'): ")
        if question.lower() == "quit":
            break

        query_embedding = model.encode([question]).tolist()
        results = collection.query(query_embeddings=query_embedding, n_results=3)

        for doc, meta, dist in zip(
            results["documents"][0], results["metadatas"][0], results["distances"][0]
        ):
            similarity = 1 - dist
            print(f"\n📄 {meta['source']} (p.{meta['page']}, checked {meta['checked']})")
            print(f"   Similarity: {similarity:.2f}")
            print(f"   {doc[:300]}...")


if __name__ == "__main__":
    main()
