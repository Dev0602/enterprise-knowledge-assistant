from src.retrieval.retriever import Retriever
from tests.evaluation_dataset import EVALUATION_DATASET


retriever = Retriever()

total_questions = len(EVALUATION_DATASET)
correct = 0


print("=" * 70)
print("RETRIEVAL EVALUATION")
print("=" * 70)


for item in EVALUATION_DATASET:
    question = item["question"]
    expected_source = item["expected_source"]

    print("\n" + "-" * 70)
    print(f"Question: {question}")
    print(f"Expected: {expected_source}")

    results = retriever.retrieve(
        query=question,
        n_results=3,
    )

    retrieved_sources = [
        result["metadata"]["source"]
        for result in results
    ]

    print(f"Retrieved: {retrieved_sources}")

    if expected_source in retrieved_sources:
        correct += 1
        print("Result: PASS")
    else:
        print("Result: FAIL")


accuracy = correct / total_questions * 100


print("\n" + "=" * 70)
print("EVALUATION SUMMARY")
print("=" * 70)
print(f"Total questions: {total_questions}")
print(f"Correct:         {correct}")
print(f"Incorrect:       {total_questions - correct}")
print(f"Accuracy:        {accuracy:.2f}%")
print("=" * 70)