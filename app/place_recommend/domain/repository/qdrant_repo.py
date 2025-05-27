from abc import ABCMeta, abstractmethod
from place_recommend.domain.place import Place
from typing import Literal


class IVectorRepository(metaclass=ABCMeta):
    @abstractmethod
    def search(
        self,
        vector: list[float],
        vector_name: Literal["text_vector", "image_vector"],
        top_k: int = 5,
    ) -> list[Place]:
        """벡터를 사용한 장소 검색을 진행한다."""
        pass
