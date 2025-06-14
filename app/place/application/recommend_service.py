# qdrant repo를 만들때까지 보류
from place.domain.repository.qdrant_repo import IVectorRepository
from typing import Optional
from place.domain.place import Place
from fastapi import HTTPException
from place.infra.embedder.text_embedder import TextEmbedder
from place.infra.embedder.image_embedder import ImageEmbedder
from utills.fuse_results import fuse_results
from dependency_injector.wiring import inject


class RecommendService:
    def __init__(
        self,
        text_embedder: TextEmbedder,
        image_embedder: ImageEmbedder,
        vector_repo: IVectorRepository,
        alpha: float = 0.5,
    ):
        """
        :param alpha: 텍스트와 이미지 임베딩 결합 시 텍스트 가중치 (0~1 사이)
        """
        self.text_embedder = text_embedder
        self.image_embedder = image_embedder
        self.vector_repo = vector_repo
        self.alpha = alpha

    def recommend(
        self, text: Optional[str] = None, image: Optional[bytes] = None, top_k: int = 5
    ) -> list[Place]:
        if not text and not image:
            raise HTTPException(
                status_code=400,  # Bad request
                detail="텍스트 또는 이미지를 최소 하나는 입력해야 합니다.",
            )
        results = []
        if text:
            text_vector = self.text_embedder.embed(text)
            text_results: list[Place] = self.vector_repo.search(
                text_vector, "text_vector", top_k * 2
            )
            results.append(("text", text_results))
        if image:
            image_vec = self.image_embedder.embed(image)
            image_results: list[Place] = self.vector_repo.search(
                image_vec, "image_vector", top_k * 2
            )
            results.append(("image", image_results))

        return fuse_results(
            results,
            top_k,
            self.alpha,
        )
