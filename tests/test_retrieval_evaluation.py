from src.retrieval.retriever import Retriever


# Questions and the document we expect the retriever to find.
EVALUATION_DATA = [
    {
        "question": "Can I work remotely?",
        "expected_source": "02_remote_work_policy.pdf",
    },
    {
        "question": "What should I do if my laptop is lost?",
        "expected_source": "03_information_security_policy.pdf",
    },
    {
        "question": "How much paid time off do employees get?",
        "expected_source": "04_leave_and_attendance_policy.pdf",
    },
    {
        "question": "How do I get technical support?",
        "expected_source": "05_it_support_and_acceptable_use.pdf",
    },
    {
        "question": "What should a new employee do on the first day?",
        "expected_source": "07_employee_onboarding_guide.pdf",
    },
    {
        "question": "What is the company's business travel policy?",
        "expected_source": "06_business_travel_policy.pdf",
    },
    {
        "question": "What are the company's information security requirements?",
        "expected_source": "03_information_security_policy.pdf",
    },
]


def evaluate_retriever():
    retriever = Retriever()

    correct = 0
    total = len(EVALUATION_DATA)

    print("\n" + "=" * 70)
    print("RETRIEVAL EVALUATION")
    print("=" * 70)

    for item in EVALUATION_DATA:

        question = item["question"]
        expected_source = item["expected_source"]

        results = retriever.retrieve(
            query=question,
            n_results=3,
        )

        retrieved_sources = [
            result["metadata"]["source"]
            for result in results
        ]

        # Check whether the expected document
        # appears anywhere in the top 3 results.
        passed = expected_source in retrieved_sources

        if passed:
            correct += 1
            status = "PASS"
        else:
            status = "FAIL"

        print("\n" + "-" * 70)
        print(f"Question: {question}")
        print(f"Expected: {expected_source}")
        print(f"Retrieved: {retrieved_sources}")
        print(f"Result: {status}")

    accuracy = (correct / total) * 100

    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)

    print(f"Total questions: {total}")
    print(f"Correct:         {correct}")
    print(f"Incorrect:       {total - correct}")
    print(f"Accuracy:        {accuracy:.2f}%")
    print("=" * 70)


if __name__ == "__main__":
    evaluate_retriever()