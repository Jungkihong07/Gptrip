from sentence_transformers import SentenceTransformer


class TextEmbedder:
    def __init__(
        self,
        model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    ):
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> list[float]:
        return self.model.encode(text, normalize_embeddings=True).tolist()
