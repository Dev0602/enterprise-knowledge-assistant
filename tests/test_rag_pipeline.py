from src.rag_pipeline import RAGPipeline


rag = RAGPipeline()


questions = [
    "Can I work remotely?",
    "What should I do if my laptop is lost?",
    "How do I get technical support?",
]


for question in questions:

    print("\n" + "=" * 70)
    print(f"QUESTION: {question}")
    print("=" * 70)

    result = rag.ask(question)

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES:")

    for source in result["sources"]:
        print(
            f"- {source['metadata']['source']}"
        )