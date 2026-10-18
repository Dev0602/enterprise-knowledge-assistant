from src.rag_pipeline import RAGPipeline
from src.evaluation.grounding import check_groundedness


rag = RAGPipeline()


TEST_CASES = [
    "Can I work remotely?",
    "What should I do if my laptop is lost?",
    "How do I get technical support?",
    "What should a new employee do on the first day?",
    "What is the company's maternity leave policy?",
    "What is the employee stock option policy?",
]


print("=" * 70)
print("GROUNDEDNESS EVALUATION")
print("=" * 70)


for question in TEST_CASES:

    # Run the complete RAG pipeline
    result = rag.ask(question)

    answer = result["answer"]
    sources = result["sources"]
    documents = result["documents"]

    # -----------------------------------------
    # Build grounding context
    # -----------------------------------------

    context_parts = []

    for document in documents:

        source = document["metadata"]["source"]
        text = document["text"]

        context_parts.append(
            f"Source: {source}\n{text}"
        )

    context = "\n\n".join(context_parts)

    # -----------------------------------------
    # Grounding evaluation
    # -----------------------------------------

    grounding = check_groundedness(
        question=question,
        answer=answer,
        context=context,
    )

    # -----------------------------------------
    # Print results
    # -----------------------------------------

    print("\n" + "-" * 70)

    print(f"Question: {question}")

    print("\nAnswer:")
    print(answer)

    print("\nSources:")

    if sources:

        for source in sources:
            print(f"- {source}")

    else:
        print("- None")

    print("\nVerdict:")
    print(grounding["verdict"])

    print("\nReason:")
    print(grounding["reason"])

    print("-" * 70)