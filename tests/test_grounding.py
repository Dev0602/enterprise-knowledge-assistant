from src.rag_pipeline import RAGPipeline


rag = RAGPipeline()


questions = [
    "Can I work remotely?",
    "How do I get technical support?",
    "What is the company's maternity leave policy?",
    "What is the employee stock option policy?",
]


for question in questions:

    print("=" * 70)
    print(f"QUESTION: {question}")
    print("=" * 70)

    result = rag.ask(question)

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES:")

    for document in result["sources"]:
        print(
            f"- {document['metadata']['source']}"
        )

    print()