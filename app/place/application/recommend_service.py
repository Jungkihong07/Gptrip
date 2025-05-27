# qdrant repo를 만들때까지 보류
from place

class RecommendService:
    def __init__(self, vector_repo:):
        """
        :param text_dim: 텍스트 임베딩 차원 (기본값: 384)
        :param image_dim: 이미지 임베딩 차원 (기본값: 384, CLIP에 맞춤)
        :param alpha: 텍스트와 이미지 임베딩 결합 시 텍스트 가중치 (0~1 사이)
        """
        self.text_dim = text_dim
        self.image_dim = image_dim
        self.alpha = alpha
