from app.place.infra.repository.qdrant_repo import QdrantRepository


# 3. 테스트 염두 로직 (이후 pytest 또는 unittest에서 사용 가능)
def _mock_vector(dim: int) -> list[float]:
    return [0.1] * dim


def test_text_vector_search():
    repo = QdrantRepository()
    result = repo.search(_mock_vector(384), vector_name="text_vector")
    assert isinstance(result, list)
    if result:
        assert hasattr(result[0], "title")


def test_image_vector_search():
    repo = QdrantRepository()
    result = repo.search(_mock_vector(512), vector_name="image_vector")
    assert isinstance(result, list)
    if result:
        assert hasattr(result[0], "title")
