from src.retrieval.hybrid_retriever import HybridRetriever


questions = [
    "Can I work remotely?",
    "What should I do if my laptop is lost?",
    "How much paid time off do employees get?",
    "How do I get technical support?",
    "What should a new employee do on the first day?",
    "What is the company's business travel policy?",
    "What are the company's information security requirements?",
]


retriever = HybridRetriever()


for question in questions:

    print("\n" + "=" * 70)
    print(f"QUESTION: {question}")
    print("=" * 70)

    results = retriever.retrieve(
        query=question,
        n_results=3,
    )

    for i, result in enumerate(results, start=1):

        print(f"\nRESULT {i}")

        print(
            "Source:",
            result["metadata"]["source"]
        )

        print(
            "Combined RRF Score:",
            round(result["score"], 6)
        )

        print(
            "Vector Rank:",
            result["vector_rank"]
        )

        print(
            "Keyword Rank:",
            result["keyword_rank"]
        )

        print(
            "Text:",
            result["text"][:300]
        )