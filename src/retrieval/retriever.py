from src.embeddings.embedder import Embedder
from src.vectorstore.chroma_store import ChromaStore


class Retriever:
    def __init__(
        self,
        candidate_results: int = 6,
        max_results: int = 3,
        distance_threshold: float = 1.4,
    ):
        # Embedding model
        self.embedder = Embedder()

        # ChromaDB vector store
        self.store = ChromaStore()

        # Number of chunks we initially retrieve
        self.candidate_results = candidate_results

        # Maximum number of final results we return
        self.max_results = max_results

        # Maximum acceptable distance
        self.distance_threshold = distance_threshold

    def retrieve(
        self,
        query: str,
        n_results: int | None = None,
    ) -> list[dict]:
        """
        Retrieve relevant documents for a user query.

        Steps:
        1. Convert the question into an embedding.
        2. Retrieve candidate chunks from ChromaDB.
        3. Remove results that are too far away.
        4. Remove duplicate PDF sources.
        5. Return the best results.
        """

        # --------------------------------------------------
        # STEP 1: Decide how many final results to return
        # --------------------------------------------------

        if n_results is not None:
            max_results = n_results
        else:
            max_results = self.max_results

        # --------------------------------------------------
        # STEP 2: Convert the user's question into an embedding
        # --------------------------------------------------

        query_embedding = self.embedder.embed(query)

        # --------------------------------------------------
        # STEP 3: Retrieve candidate chunks from ChromaDB
        # --------------------------------------------------

        results = self.store.search(
            query_embedding=query_embedding,
            n_results=self.candidate_results,
        )

        retrieved_documents = []

        # Keep track of PDFs we have already returned
        seen_sources = set()

        # --------------------------------------------------
        # STEP 4: Process ChromaDB results
        # --------------------------------------------------

        for i, document in enumerate(results["documents"][0]):

            # Distance tells us how far the result is
            # from the user's question.
            distance = results["distances"][0][i]

            # Metadata contains information such as
            # the PDF filename.
            metadata = results["metadatas"][0][i]

            source = metadata["source"]

            # --------------------------------------------------
            # STEP 5: Remove low-relevance results
            # --------------------------------------------------

            if distance > self.distance_threshold:
                continue

            # --------------------------------------------------
            # STEP 6: Remove duplicate PDF sources
            # --------------------------------------------------

            if source in seen_sources:
                continue

            seen_sources.add(source)

            # --------------------------------------------------
            # STEP 7: Store the useful result
            # --------------------------------------------------

            retrieved_documents.append(
                {
                    "text": document,
                    "metadata": metadata,
                    "distance": distance,
                }
            )

            # --------------------------------------------------
            # STEP 8: Stop once we have enough results
            # --------------------------------------------------

            if len(retrieved_documents) >= max_results:
                break

        return retrieved_documents