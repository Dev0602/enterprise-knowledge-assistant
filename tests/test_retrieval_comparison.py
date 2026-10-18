from src.retrieval.retriever import Retriever
from src.retrieval.hybrid_retriever import HybridRetriever
from src.retrieval.reranker import Reranker
from src.retrieval.utils import unique_sources
from tests.evaluation_dataset import EVALUATION_DATASET

# --------------------------------------------------
# Initialize retrieval components
# --------------------------------------------------

vector_retriever = Retriever()
hybrid_retriever = HybridRetriever()
reranker = Reranker()


# --------------------------------------------------
# Evaluation function
# --------------------------------------------------

def evaluate_method(name, retrieve_function):
    correct = 0
    total = len(EVALUATION_DATASET)

    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    for item in EVALUATION_DATASET:

        question = item["question"]
        expected_source = item["expected_source"]

        results = retrieve_function(question)

        retrieved_sources = [
            result["metadata"]["source"]
            for result in results
        ]

        passed = expected_source in retrieved_sources

        if passed:
            correct += 1

        print(f"\nQuestion: {question}")
        print(f"Expected: {expected_source}")
        print(f"Retrieved: {retrieved_sources}")
        print(f"Result: {'PASS' if passed else 'FAIL'}")

    recall = correct / total * 100

    print("\n" + "-" * 70)
    print(f"Correct:  {correct}/{total}")
    print(f"Recall@3: {recall:.2f}%")
    print("-" * 70)

    return recall


# --------------------------------------------------
# 1. Vector Search
# --------------------------------------------------

vector_score = evaluate_method(
    "1. VECTOR SEARCH",
    lambda question: vector_retriever.retrieve(
        query=question,
        n_results=3,
    ),
)


# --------------------------------------------------
# 2. Hybrid Search
# --------------------------------------------------

hybrid_score = evaluate_method(
    "2. HYBRID SEARCH (VECTOR + BM25 + RRF)",
    lambda question: hybrid_retriever.retrieve(
        query=question,
        n_results=3,
    ),
)


# --------------------------------------------------
# 3. Hybrid + Reranker
# --------------------------------------------------
def retrieve_with_reranker(question):

    candidates = hybrid_retriever.retrieve(
        query=question,
        n_results=6,
    )

    reranked = reranker.rerank(
        query=question,
        results=candidates,
        top_k=6,
    )

    return unique_sources(reranked)[:3]


reranker_score = evaluate_method(
    "3. HYBRID + CROSS-ENCODER RERANKER",
    retrieve_with_reranker,
)


# --------------------------------------------------
# Final comparison
# --------------------------------------------------

print("\n" + "=" * 70)
print("FINAL RETRIEVAL COMPARISON")
print("=" * 70)

print(f"Vector Search:              {vector_score:.2f}%")
print(f"Hybrid Search:              {hybrid_score:.2f}%")
print(f"Hybrid + Reranker:          {reranker_score:.2f}%")

print("=" * 70)