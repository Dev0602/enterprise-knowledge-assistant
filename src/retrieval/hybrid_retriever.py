from rank_bm25 import BM25Okapi

from src.retrieval.retriever import Retriever


class HybridRetriever:
    def __init__(
        self,
        candidate_results: int = 6,
        max_results: int = 3,
    ):
        self.candidate_results = candidate_results
        self.max_results = max_results

        # Vector retriever
        self.vector_retriever = Retriever(
            candidate_results=candidate_results,
            max_results=max_results,
        )

        # Documents for BM25
        self.documents = []

        # BM25 index
        self.bm25 = None

        self._build_keyword_index()

    def _build_keyword_index(self):
        """Build BM25 index from all Chroma documents."""

        collection = self.vector_retriever.store.collection

        data = collection.get(
            include=["documents", "metadatas"]
        )

        documents = data["documents"]
        metadatas = data["metadatas"]

        for document, metadata in zip(documents, metadatas):
            self.documents.append(
                {
                    "text": document,
                    "metadata": metadata,
                }
            )

        tokenized_documents = [
            document["text"].lower().split()
            for document in self.documents
        ]

        if tokenized_documents:
            self.bm25 = BM25Okapi(tokenized_documents)

    def _keyword_search(
        self,
        query: str,
        n_results: int = 6,
    ) -> list[dict]:
        """Retrieve candidate chunks using BM25."""

        if self.bm25 is None:
            return []

        query_tokens = query.lower().split()

        scores = self.bm25.get_scores(query_tokens)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True,
        )

        results = []

        for index in ranked_indices[:n_results]:

            if scores[index] <= 0:
                continue

            document = self.documents[index]

            results.append(
                {
                    "text": document["text"],
                    "metadata": document["metadata"],
                    "keyword_score": float(scores[index]),
                }
            )

        return results

    def _result_id(self, result: dict) -> str:
        """
        Identify an individual chunk.

        Source + chunk_index prevents different chunks
        from the same PDF being treated as one result.
        """

        metadata = result["metadata"]

        return (
            f"{metadata.get('source', '')}:"
            f"{metadata.get('chunk_index', '')}"
        )

    def _rrf_score(
        self,
        rank: int,
        k: int = 60,
    ) -> float:
        """Calculate Reciprocal Rank Fusion contribution."""

        return 1.0 / (k + rank)

    def retrieve(
        self,
        query: str,
        n_results: int | None = None,
    ) -> list[dict]:
        """
        Hybrid retrieval using:

        1. Vector search
        2. BM25 keyword search
        3. RRF fusion
        """

        final_results = (
            n_results
            if n_results is not None
            else self.max_results
        )

        # -----------------------------------------
        # 1. Retrieve a larger vector candidate pool
        # -----------------------------------------

        vector_results = self.vector_retriever.retrieve(
            query=query,
            n_results=self.candidate_results,
        )

        # -----------------------------------------
        # 2. Retrieve a larger BM25 candidate pool
        # -----------------------------------------

        keyword_results = self._keyword_search(
            query=query,
            n_results=self.candidate_results,
        )

        # -----------------------------------------
        # 3. Combine using RRF
        # -----------------------------------------

        combined = {}

        # Vector results
        for rank, result in enumerate(
            vector_results,
            start=1,
        ):

            result_id = self._result_id(result)

            if result_id not in combined:
                combined[result_id] = {
                    "text": result["text"],
                    "metadata": result["metadata"],
                    "score": 0.0,
                    "vector_rank": None,
                    "keyword_rank": None,
                }

            combined[result_id]["vector_rank"] = rank

            combined[result_id]["score"] += (
                self._rrf_score(rank)
            )

        # BM25 results
        for rank, result in enumerate(
            keyword_results,
            start=1,
        ):

            result_id = self._result_id(result)

            if result_id not in combined:
                combined[result_id] = {
                    "text": result["text"],
                    "metadata": result["metadata"],
                    "score": 0.0,
                    "vector_rank": None,
                    "keyword_rank": None,
                }

            combined[result_id]["keyword_rank"] = rank

            combined[result_id]["score"] += (
                self._rrf_score(rank)
            )

        # -----------------------------------------
        # 4. Sort by RRF score
        # -----------------------------------------

        ranked_results = sorted(
            combined.values(),
            key=lambda result: result["score"],
            reverse=True,
        )

        # -----------------------------------------
        # 5. Return final top results
        # -----------------------------------------

        return ranked_results[:final_results]