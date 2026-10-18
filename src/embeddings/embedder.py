from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

    def embed(self, text: str) -> list[float]:
        vector = self.model.encode(text)
        return vector.tolist()