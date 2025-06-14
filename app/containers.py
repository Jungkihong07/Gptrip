from dependency_injector import containers, providers
from place.infra.embedder.text_embedder import TextEmbedder
from place.infra.repository.qdrant_repo import QdrantRepository
from place.application.recommend_service import RecommendService
from place.infra.embedder.image_embedder import ImageEmbedder


class Container(containers.DeclarativeContainer):
    text_embedder = providers.Singleton(TextEmbedder)
    # 해당 레포지토리는 상태가 없으며, 사용되는데 거의 비용이 없다. 그렇기 때문에 factory를 사용하지 않는다.
    vector_repo = providers.Singleton(QdrantRepository)
    image_embedder = providers.Singleton(ImageEmbedder)

    recommend_service = providers.Factory(
        RecommendService,
        text_embedder=text_embedder,
        image_embedder=image_embedder,
        vector_repo=vector_repo,
        alpha=0.5,
    )
