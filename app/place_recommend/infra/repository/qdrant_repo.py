from domain.repository.qdrant_repo import IVectorRepository
from qdrant_client import QdrantClient
from domain.place import Place

from config import get_settings

settings = get_settings()


class QdrantRepository(IVectorRepository):
    def __init__(self, collection_name: str = "gptrip_places"):
        self.client = QdrantClient(
            url=f"https://{settings.qdrant_host}",
            api_key=settings.qdrant_gptrip_cluster,
        )
        self.collection = collection_name

    def search(self, vector: list[float], top_k: int = 5) -> list[Place]:
        results = self.client.query_points(
            collection_name=self.collection,
            query_vector=vector,
            limit=top_k,
            with_payload=True,
        )
        return [Place(**point.payload) for point in results]
