from qdrant_client import QdrantClient

from app.config import get_settings

settings = get_settings()


def test_qdrant_connection():
    client = QdrantClient(
        url=f"https://{settings.qdrant_host}", api_key=settings.qdrant_gptrip_cluster
    )

    # 1. 인증 기반 연결 테스트 (헬스체크 대체)
    collections = client.get_collections().collections
    assert isinstance(collections, list), "Qdrant 연결 실패 또는 인증 오류"

    # 2. 컬렉션 존재 확인
    assert any(
        c.name == "gptrip_places" for c in collections
    ), "gptrip_places 컬렉션 없음"

    # 3. 검색 테스트
    result = client.query_points(
        collection_name="gptrip_places",
        query=[0.1] * 384,  # ✅ 명시적으로 벡터 이름 지정
        using="text_vector",  # ✅ 어떤 named vector 쓸지 명시
        limit=1,
        with_payload=True,
    )

    points = result.points  # ✅ QueryResponse 객체의 hits 접근
    assert points, "검색 결과가 없습니다"

    result = client.query_points(
        collection_name="gptrip_places",
        query=[0.1] * 512,  # ✅ 명시적으로 벡터 이름 지정
        using="image_vector",  # ✅ 어떤 named vector 쓸지 명시
        limit=1,
        with_payload=True,
    )

    points = result.points  # ✅ QueryResponse 객체의 hits 접근
    assert points, "검색 결과가 없습니다"

    payload = points[0].payload
    assert "title" in payload, "검색 결과에 'title' 없음"
