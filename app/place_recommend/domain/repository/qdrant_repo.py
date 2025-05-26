from abc import ABCMeta, abstractmethod
from domain.place import Place


class IVectorRepository(metaclass=ABCMeta):
    @abstractmethod
    def search(self, vector: list[float], top_k: int = 5) -> list[Place]:
        """벡터를 사용한 장소 검색을 진행한다."""
        pass
