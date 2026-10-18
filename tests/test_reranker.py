from src.retrieval.hybrid_retriever import HybridRetriever
from src.retrieval.reranker import Reranker


question = "How do I get technical support?"


print("=" * 70)
print("RERANKER TEST")
print("=" * 70)

retriever = HybridRetriever()

results = retriever.retrieve(
    query=question,
    n_results=6,
)

print("\nBEFORE RERANKING")
print("-" * 70)

for i, result in enumerate(results, start=1):
    print(
        f"{i}. "
        f"{result['metadata']['source']} | "
        f"RRF Score: {result['score']:.6f}"
    )


reranker = Reranker()

reranked_results = reranker.rerank(
    query=question,
    results=results,
    top_k=3,
)


print("\nAFTER RERANKING")
print("-" * 70)

for i, result in enumerate(reranked_results, start=1):
    print(
        f"{i}. "
        f"{result['metadata']['source']} | "
        f"Rerank Score: {result['rerank_score']:.6f}"
    )

    print(
        f"   {result['text'][:200]}"
    )

print("\n" + "=" * 70)