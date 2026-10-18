from src.rag_pipeline import RAGPipeline


rag = RAGPipeline()


TEST_CASES = [
    {
        "question": "Can I work remotely?",
        "expected_answer": "Employees may work remotely when their role, manager approval, and business needs allow it.",
        "expected_source": "02_remote_work_policy.pdf",
        "answerable": True,
    },
    {
        "question": "What should I do if my laptop is lost?",
        "expected_answer": "Report the lost company device to IT Support as soon as possible.",
        "expected_source": "03_information_security_policy.pdf",
        "answerable": True,
    },
    {
        "question": "How do I get technical support?",
        "expected_answer": "Submit technical issues through the approved IT support portal. Critical incidents should use the emergency support process.",
        "expected_source": "05_it_support_and_acceptable_use.pdf",
        "answerable": True,
    },
    {
        "question": "What should a new employee do on the first day?",
        "expected_answer": "Complete HR orientation, receive required equipment, activate the company account, and review essential policies.",
        "expected_source": "07_employee_onboarding_guide.pdf",
        "answerable": True,
    },
    {
        "question": "What is the company's maternity leave policy?",
        "expected_answer": "I couldn't find that information in the company knowledge base.",
        "expected_source": None,
        "answerable": False,
    },
    {
        "question": "What is the employee stock option policy?",
        "expected_answer": "I couldn't find that information in the company knowledge base.",
        "expected_source": None,
        "answerable": False,
    },
]


print("=" * 70)
print("ANSWER QUALITY EVALUATION")
print("=" * 70)


for test_case in TEST_CASES:

    question = test_case["question"]

    result = rag.ask(question)

    answer = result["answer"]
    sources = result["sources"]

    source_names = [
        document["metadata"]["source"]
        for document in sources
    ]

    print("\n" + "-" * 70)

    print(f"Question: {question}")

    print(f"\nExpected:")
    print(test_case["expected_answer"])

    print(f"\nGenerated:")
    print(answer)

    print(f"\nExpected Source:")
    print(test_case["expected_source"])

    print(f"\nRetrieved Sources:")
    print(source_names)

    print("-" * 70)