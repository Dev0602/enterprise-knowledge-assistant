from src.embeddings.embedder import Embedder
from src.vectorstore.chroma_store import ChromaStore


embedder = Embedder()
store = ChromaStore()

query = "When are assignments due?"

query_embedding = embedder.embed(query)

results = store.search(query_embedding, n_results=1)

print("FULL RESULTS:")
print(results)