from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class Reranker:
    def __init__(self):
        self.model = CrossEncoder(MODEL_NAME)

    def rerank(
        self,
        query: str,
        results: list[dict],
        top_k: int = 3,
    ) -> list[dict]:
        """
        Rerank retrieved documents based on
        how relevant they are to the query.
        """

        if not results:
            return []

        pairs = [
            (query, result["text"])
            for result in results
        ]

        scores = self.model.predict(pairs)

        reranked_results = []

        for result, score in zip(results, scores):

            updated_result = result.copy()

            updated_result["rerank_score"] = float(score)

            reranked_results.append(updated_result)

        reranked_results.sort(
            key=lambda result: result["rerank_score"],
            reverse=True,
        )

        return reranked_results[:top_k]