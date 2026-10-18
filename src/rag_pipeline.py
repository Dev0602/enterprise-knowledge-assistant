from src.retrieval.hybrid_retriever import HybridRetriever
from src.retrieval.reranker import Reranker
from src.generation.generator import generate_answer
from src.evaluation.grounding import check_groundedness


FALLBACK_ANSWER = (
    "I couldn't find that information in the company knowledge base."
)


class RAGPipeline:
    def __init__(
        self,
        candidate_results: int = 6,
        n_results: int = 3,
        min_rerank_score: float = -1.5,
    ):
        # Hybrid retrieval:
        # Vector Search + BM25 + RRF
        self.retriever = HybridRetriever(
            candidate_results=candidate_results,
            max_results=n_results,
        )

        # CrossEncoder reranker
        self.reranker = Reranker()

        # Number of documents sent to the LLM
        self.n_results = n_results

        # Minimum score required before
        # allowing the LLM to answer
        self.min_rerank_score = min_rerank_score

    def ask(self, question: str) -> dict:
        """
        Run the complete grounded RAG pipeline.

        Question
            ↓
        Hybrid Retrieval
            ↓
        RRF
            ↓
        Cross-Encoder Reranking
            ↓
        Confidence Check
            ↓
        Qwen
            ↓
        Grounding Evaluation
            ↓
        Answer + Sources
        """

        # -----------------------------------------
        # 1. Hybrid retrieval
        # -----------------------------------------

        retrieved_documents = self.retriever.retrieve(
            query=question,
            n_results=self.n_results,
        )

        if not retrieved_documents:
            return {
                "answer": FALLBACK_ANSWER,
                "sources": [],
                "documents": [],
                "grounding": {
                    "verdict": "ABSTENTION",
                    "reason": (
                        "No relevant documents were retrieved "
                        "from the knowledge base."
                    ),
                },
            }

        # -----------------------------------------
        # 2. Rerank documents
        # -----------------------------------------

        reranked_documents = self.reranker.rerank(
            query=question,
            results=retrieved_documents,
            top_k=self.n_results,
        )

        if not reranked_documents:
            return {
                "answer": FALLBACK_ANSWER,
                "sources": [],
                "documents": [],
                "grounding": {
                    "verdict": "ABSTENTION",
                    "reason": (
                        "No documents remained after reranking."
                    ),
                },
            }

        # -----------------------------------------
        # 3. Confidence check
        # -----------------------------------------

        best_score = reranked_documents[0]["rerank_score"]

        print(
            f"Best rerank score for '{question}': "
            f"{best_score:.4f}"
        )

        if best_score < self.min_rerank_score:
            return {
                "answer": FALLBACK_ANSWER,
                "sources": [],
                "documents": [],
                "grounding": {
                    "verdict": "ABSTENTION",
                    "reason": (
                        "The highest reranker score was below "
                        "the configured confidence threshold."
                    ),
                },
            }

        # -----------------------------------------
        # 4. Remove duplicate chunks
        # -----------------------------------------

        unique_documents = []
        seen = set()

        for document in reranked_documents:

            source = document["metadata"]["source"]

            chunk_index = document["metadata"].get(
                "chunk_index"
            )

            key = (source, chunk_index)

            if key not in seen:
                seen.add(key)
                unique_documents.append(document)

        # -----------------------------------------
        # 5. Build context
        # -----------------------------------------

        context_parts = []

        for document in unique_documents:

            source = document["metadata"]["source"]
            text = document["text"]

            context_parts.append(
                f"Source: {source}\n{text}"
            )

        context = "\n\n".join(context_parts)

        # -----------------------------------------
        # 6. Generate grounded answer
        # -----------------------------------------

        answer = generate_answer(
            question=question,
            context=context,
        )

        # -----------------------------------------
        # 7. Grounding evaluation
        # -----------------------------------------

        grounding = check_groundedness(
            question=question,
            answer=answer,
            context=context,
        )

        # -----------------------------------------
        # 8. Create clean source list
        # -----------------------------------------

        sources = []

        for document in unique_documents:

            source = document["metadata"]["source"]

            if source not in sources:
                sources.append(source)

        # -----------------------------------------
        # 9. Return complete result
        # -----------------------------------------

        return {
            "answer": answer,
            "sources": sources,
            "documents": unique_documents,
            "grounding": grounding,
        }