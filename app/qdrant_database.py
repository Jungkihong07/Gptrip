from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance

# Qdrant Cloud 정보
QDRANT_API_KEY = "your-api-key"
QDRANT_HOST = "your-cluster-id.cloud.qdrant.io"

client = QdrantClient(url=f"https://{QDRANT_HOST}", api_key=QDRANT_API_KEY)
