from place.domain.repository.qdrant_repo import IVectorRepository
from qdrant_client import QdrantClient
from place.domain.place import Place
from typing import Literal
from config import get_settings
from utills.db_utils import map_place

settings = get_settings()


class QdrantRepository(IVectorRepository):
    def __init__(self, collection_name: str = "gptrip_places"):
        self.client = QdrantClient(
            url=f"https://{settings.qdrant_host}",
            api_key=settings.qdrant_gptrip_cluster,
        )
        self.collection = collection_name

    def search(
        self,
        vector: list[float],
        vector_name: Literal["text_vector", "image_vector"],
        top_k: int = 5,
    ) -> list[Place]:
        results = self.client.query_points(
            collection_name=self.collection,
            query=vector,
            using=vector_name,
            limit=top_k,
            with_payload=True,
        )
        return [map_place(point.payload) for point in results.points]
