from src.retrieval.retriever import Retriever
from src.retrieval.hybrid_retriever import HybridRetriever
from src.retrieval.reranker import Reranker
from src.retrieval.utils import unique_sources
from tests.evaluation_dataset import EVALUATION_DATASET


vector_retriever = Retriever()
hybrid_retriever = HybridRetriever()
reranker = Reranker()


def reciprocal_rank(results, expected_source):
    """
    Calculate Reciprocal Rank for one question.

    Correct document at:
    #1 -> 1.0
    #2 -> 0.5
    #3 -> 0.333
    """

    for rank, result in enumerate(results, start=1):

        source = result["metadata"]["source"]

        if source == expected_source:
            return 1 / rank

    return 0.0


def evaluate_mrr(name, retrieve_function):

    total_score = 0.0

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

        rr = reciprocal_rank(
            results,
            expected_source,
        )

        total_score += rr

        rank = 0

        for i, source in enumerate(
            retrieved_sources,
            start=1,
        ):
            if source == expected_source:
                rank = i
                break

        print(f"\nQuestion: {question}")
        print(f"Expected: {expected_source}")
        print(f"Retrieved: {retrieved_sources}")
        print(f"Correct Rank: {rank}")
        print(f"Reciprocal Rank: {rr:.4f}")

    mrr = total_score / len(EVALUATION_DATASET)

    print("\n" + "-" * 70)
    print(f"MRR: {mrr:.4f}")
    print("-" * 70)

    return mrr


# --------------------------------------------------
# VECTOR SEARCH
# --------------------------------------------------

vector_mrr = evaluate_mrr(
    "1. VECTOR SEARCH",
    lambda question: vector_retriever.retrieve(
        query=question,
        n_results=3,
    ),
)


# --------------------------------------------------
# HYBRID SEARCH
# --------------------------------------------------

hybrid_mrr = evaluate_mrr(
    "2. HYBRID SEARCH",
    lambda question: unique_sources(
        hybrid_retriever.retrieve(
            query=question,
            n_results=6,
        )
    )[:3],
)


# --------------------------------------------------
# HYBRID + RERANKER
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

    unique_results = unique_sources(reranked)

    return unique_results[:3]


reranker_mrr = evaluate_mrr(
    "3. HYBRID + CROSS-ENCODER RERANKER",
    retrieve_with_reranker,
)


# --------------------------------------------------
# FINAL RESULTS
# --------------------------------------------------

print("\n" + "=" * 70)
print("FINAL MRR COMPARISON")
print("=" * 70)

print(f"Vector Search:              {vector_mrr:.4f}")
print(f"Hybrid Search:              {hybrid_mrr:.4f}")
print(f"Hybrid + Reranker:          {reranker_mrr:.4f}")

print("=" * 70)