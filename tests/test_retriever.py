from src.retrieval.retriever import Retriever


retriever = Retriever()


questions = [
    "Can I work remotely?",
    "What should I do if my laptop is lost?",
    "How much paid time off do employees get?",
    "How do I get technical support?",
    "What should a new employee do on the first day?",
]


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
        print(f"Source: {result['metadata']['source']}")
        print(f"Distance: {result['distance']}")
        print(f"Text: {result['text'][:500]}")