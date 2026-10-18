from src.rag_pipeline import RAGPipeline


# --------------------------------------------------
# Evaluation dataset
# --------------------------------------------------

TEST_CASES = [
    {
        "question": "Can I work remotely?",
        "answerable": True,
        "expected_source": "02_remote_work_policy.pdf",
    },
    {
        "question": "What should I do if my laptop is lost?",
        "answerable": True,
        "expected_source": "03_information_security_policy.pdf",
    },
    {
        "question": "How much paid time off do employees get?",
        "answerable": True,
        "expected_source": "04_leave_and_attendance_policy.pdf",
    },
    {
        "question": "How do I get technical support?",
        "answerable": True,
        "expected_source": "05_it_support_and_acceptable_use.pdf",
    },
    {
        "question": "What should a new employee do on the first day?",
        "answerable": True,
        "expected_source": "07_employee_onboarding_guide.pdf",
    },
    {
        "question": "What is the company's business travel policy?",
        "answerable": True,
        "expected_source": "06_business_travel_policy.pdf",
    },
    {
        "question": "What are the company's information security requirements?",
        "answerable": True,
        "expected_source": "03_information_security_policy.pdf",
    },
    {
        "question": "What is the company's maternity leave policy?",
        "answerable": False,
        "expected_source": None,
    },
    {
        "question": "What is the employee stock option policy?",
        "answerable": False,
        "expected_source": None,
    },
]


# --------------------------------------------------
# Initialize pipeline
# --------------------------------------------------

rag = RAGPipeline()


# --------------------------------------------------
# Metrics
# --------------------------------------------------

answerable_correct = 0
answerable_total = 0

abstention_correct = 0
abstention_total = 0

grounded_answers = 0
grounded_total = 0

source_hits = 0
source_total = 0


# --------------------------------------------------
# Run evaluation
# --------------------------------------------------

print("=" * 80)
print("FINAL RAG SYSTEM EVALUATION")
print("=" * 80)


for i, test_case in enumerate(TEST_CASES, start=1):

    question = test_case["question"]
    expected_answerable = test_case["answerable"]
    expected_source = test_case["expected_source"]

    result = rag.ask(question)

    answer = result["answer"]
    sources = result["sources"]
    grounding = result["grounding"]

    verdict = grounding["verdict"]

    print("\n" + "-" * 80)
    print(f"Test {i}")
    print(f"Question: {question}")

    print("\nAnswer:")
    print(answer)

    print("\nSources:")

    if sources:
        for source in sources:
            print(f"- {source}")
    else:
        print("- None")

    print(f"\nGrounding: {verdict}")


    # --------------------------------------------------
    # Answerability evaluation
    # --------------------------------------------------

    if expected_answerable:

        answerable_total += 1

        is_abstention = verdict == "ABSTENTION"

        if not is_abstention:
            answerable_correct += 1

    else:

        abstention_total += 1

        if verdict == "ABSTENTION":
            abstention_correct += 1


    # --------------------------------------------------
    # Grounding evaluation
    # --------------------------------------------------

    if expected_answerable:

        grounded_total += 1

        if verdict == "SUPPORTED":
            grounded_answers += 1


    # --------------------------------------------------
    # Source retrieval evaluation
    # --------------------------------------------------

    if expected_source is not None:

        source_total += 1

        if expected_source in sources:
            source_hits += 1


# --------------------------------------------------
# Calculate metrics
# --------------------------------------------------

answerable_accuracy = (
    answerable_correct / answerable_total
    if answerable_total
    else 0
)

abstention_accuracy = (
    abstention_correct / abstention_total
    if abstention_total
    else 0
)

groundedness_rate = (
    grounded_answers / grounded_total
    if grounded_total
    else 0
)

source_recall = (
    source_hits / source_total
    if source_total
    else 0
)


# --------------------------------------------------
# Final report
# --------------------------------------------------

print("\n")
print("=" * 80)
print("FINAL RESULTS")
print("=" * 80)

print(
    f"\nAnswerable Question Accuracy: "
    f"{answerable_accuracy:.2%}"
)

print(
    f"Abstention Accuracy: "
    f"{abstention_accuracy:.2%}"
)

print(
    f"Grounded Answer Rate: "
    f"{groundedness_rate:.2%}"
)

print(
    f"Expected Source Retrieval: "
    f"{source_recall:.2%}"
)

print("\n" + "=" * 80)
print("RETRIEVAL METRICS FROM PREVIOUS EVALUATION")
print("=" * 80)

print("Recall@3: 100.00%")
print("Vector Search MRR: 1.0000")
print("Hybrid Search MRR: 0.7381")
print("Hybrid + Reranker MRR: 0.9286")

print("\n" + "=" * 80)
print("EVALUATION COMPLETE")
print("=" * 80)