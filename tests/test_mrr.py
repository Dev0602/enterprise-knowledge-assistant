import argparse

from src.retrieval.retriever import Retriever
from src.retrieval.hybrid_retriever import HybridRetriever
from src.retrieval.reranker import Reranker
from src.retrieval.utils import unique_sources
from tests.evaluation_dataset import EVALUATION_DATASET
from tests.evaluation_dataset_hard import HARD_EVALUATION_DATASET


vector_retriever = Retriever()
hybrid_retriever = HybridRetriever()
reranker = Reranker()


def get_expected_sources(item):
    """
    Support either:

    "expected_source": "file.pdf"

    or:

    "expected_sources": [
        "file1.pdf",
        "file2.pdf",
    ]
    """

    if "expected_sources" in item:
        return item["expected_sources"]

    return [item["expected_source"]]


def find_rank(results, expected_sources):
    """
    Return the rank of the first retrieved source that matches
    any valid expected source.

    Returns 0 if none of the valid sources were retrieved.
    """

    for rank, result in enumerate(results, start=1):
        source = result["metadata"]["source"]

        if source in expected_sources:
            return rank

    return 0


def evaluate_retrieval(name, retrieve_function, dataset):

    reciprocal_rank_total = 0.0
    hit_at_1_total = 0
    hit_at_3_total = 0

    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    for item in dataset:

        question = item["question"]
        expected_sources = get_expected_sources(item)

        results = retrieve_function(question)

        retrieved_sources = [
            result["metadata"]["source"]
            for result in results
        ]

        rank = find_rank(
            results,
            expected_sources,
        )

        reciprocal_rank = (
            1 / rank
            if rank > 0
            else 0.0
        )

        hit_at_1 = rank == 1
        hit_at_3 = 1 <= rank <= 3

        reciprocal_rank_total += reciprocal_rank
        hit_at_1_total += int(hit_at_1)
        hit_at_3_total += int(hit_at_3)

        print(f"\nQuestion: {question}")
        print(f"Expected: {expected_sources}")
        print(f"Retrieved: {retrieved_sources}")
        print(f"Correct Rank: {rank}")
        print(f"Reciprocal Rank: {reciprocal_rank:.4f}")

    total_questions = len(dataset)

    hit_at_1_rate = hit_at_1_total / total_questions
    hit_at_3_rate = hit_at_3_total / total_questions
    mrr = reciprocal_rank_total / total_questions

    print("\n" + "-" * 70)
    print(f"Questions: {total_questions}")
    print(f"Hit@1:     {hit_at_1_rate:.2%}")
    print(f"Hit@3:     {hit_at_3_rate:.2%}")
    print(f"MRR:       {mrr:.4f}")
    print("-" * 70)

    return {
        "hit_at_1": hit_at_1_rate,
        "hit_at_3": hit_at_3_rate,
        "mrr": mrr,
    }


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


def run_evaluation(dataset, dataset_name):

    print("\n" + "=" * 70)
    print(f"DATASET: {dataset_name}")
    print(f"QUESTIONS: {len(dataset)}")
    print("=" * 70)

    vector_metrics = evaluate_retrieval(
        "1. VECTOR SEARCH",
        lambda question: vector_retriever.retrieve(
            query=question,
            n_results=3,
        ),
        dataset,
    )

    hybrid_metrics = evaluate_retrieval(
        "2. HYBRID SEARCH",
        lambda question: unique_sources(
            hybrid_retriever.retrieve(
                query=question,
                n_results=6,
            )
        )[:3],
        dataset,
    )

    reranker_metrics = evaluate_retrieval(
        "3. HYBRID + CROSS-ENCODER RERANKER",
        retrieve_with_reranker,
        dataset,
    )

    print("\n" + "=" * 70)
    print(f"FINAL RETRIEVAL COMPARISON — {dataset_name}")
    print("=" * 70)

    print(
        f"{'Method':<28}"
        f"{'Hit@1':>12}"
        f"{'Hit@3':>12}"
        f"{'MRR':>12}"
    )

    print("-" * 70)

    print(
        f"{'Vector Search':<28}"
        f"{vector_metrics['hit_at_1']:>11.2%}"
        f"{vector_metrics['hit_at_3']:>11.2%}"
        f"{vector_metrics['mrr']:>12.4f}"
    )

    print(
        f"{'Hybrid Search':<28}"
        f"{hybrid_metrics['hit_at_1']:>11.2%}"
        f"{hybrid_metrics['hit_at_3']:>11.2%}"
        f"{hybrid_metrics['mrr']:>12.4f}"
    )

    print(
        f"{'Hybrid + Reranker':<28}"
        f"{reranker_metrics['hit_at_1']:>11.2%}"
        f"{reranker_metrics['hit_at_3']:>11.2%}"
        f"{reranker_metrics['mrr']:>12.4f}"
    )

    print("=" * 70)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dataset",
        choices=["baseline", "hard"],
        default="baseline",
        help="Choose which retrieval evaluation dataset to run.",
    )

    args = parser.parse_args()

    if args.dataset == "hard":
        run_evaluation(
            HARD_EVALUATION_DATASET,
            "HARD",
        )
    else:
        run_evaluation(
            EVALUATION_DATASET,
            "BASELINE",
        )
