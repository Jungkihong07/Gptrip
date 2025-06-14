import os
import pickle
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct
from tqdm import tqdm

# ✅ 1. 환경 변수 로드 (Qdrant API Key와 Host 주소)
load_dotenv()
API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST")

client = QdrantClient(url=f"https://{QDRANT_HOST}", api_key=API_KEY)
collection_name = "gptrip_places"

# ✅ 2. Qdrant 컬렉션 생성 (recreate 시 기존 데이터 삭제됨)
if client.collection_exists(collection_name):
    client.delete_collection(collection_name)

# ✅ 새 컬렉션 생성
client.create_collection(
    collection_name=collection_name,
    vectors_config={
        "text_vector": VectorParams(size=384, distance=Distance.COSINE),
        "image_vector": VectorParams(size=512, distance=Distance.COSINE),
    },
)

# ✅ 3. 장소 메타데이터 로드
df = pd.read_csv("data/incheon_place_set.csv")
df["contentid"] = df["contentid"].astype(str)

# ✅ 4. 텍스트 임베딩 로드
text_embeddings = np.load("data/incheon_place_embeddings.npy")

# ✅ 5. 이미지 임베딩 로드
with open("data/images/incheon_image_embeddings.pkl", "rb") as f:
    image_data = pickle.load(f)
image_vectors = image_data["features"]
image_filenames = image_data["filenames"]

# ✅ 6. 포함할 payload 컬럼 정의
desired_columns = [
    "title",
    "tel",
    "addr1",
    "addr2",
    "mapx",
    "mapy",
    "contentid",
    "image",
    "modifiedtime",
    "emotional_summary",
]


# ✅ 7. payload 정리 함수 (NaN 또는 빈 문자열 제거)
def clean_payload(row):
    payload = {}
    for col in desired_columns:
        val = row.get(col)
        if pd.notna(val) and str(val).strip() != "":
            payload[col] = val
    return payload


# ✅ 8. 텍스트 벡터 포인트 생성
text_points = []
for i, row in df.iterrows():
    payload = clean_payload(row)
    payload["type"] = "text"
    payload["region"] = "incheon"
    text_points.append(
        PointStruct(
            id=int(row["contentid"]),  # 그대로 사용
            vector={
                "text_vector": text_embeddings[i].tolist(),
                "image_vector": [0.0] * 512,
            },
            payload=payload,
        )
    )


# 🔹 먼저 image_url 정보를 불러와서 dict로 구성
url_df = pd.read_csv("data/incheon_image_url.csv")  # 컬럼: filename, image_url
image_url_map = dict(zip(url_df["filename"], url_df["image_url"]))


# ✅ 9. 이미지 벡터 포인트 생성
image_points = []
for i, (vec, filename) in enumerate(zip(image_vectors, image_filenames)):
    filename_base = filename.replace(".jpg", "")
    content_id, img_index = filename_base.split("_")
    match = df[df["contentid"] == content_id]

    if match.empty:
        print(f"{filename}에 해당하는 장소가 없습니다.")
        continue

    row = match.iloc[0]
    payload = clean_payload(row)
    payload["type"] = "image"
    payload["region"] = "incheon"

    # 🔹 filename이 일치하는 경우 image_url 추가
    if filename in image_url_map:
        payload["firstimage"] = image_url_map[filename]

    image_points.append(
        PointStruct(
            id=int(content_id) * 100 + int(img_index),
            vector={
                "text_vector": [0.0] * 384,
                "image_vector": vec,
            },
            payload=payload,
        )
    )


# ✅ 10. Qdrant 업로드 (100개씩 배치 업로드)
def batch_upload(points, batch_size=100):
    for i in tqdm(range(0, len(points), batch_size), desc="Uploading to Qdrant"):
        client.upsert(
            collection_name="gptrip_places", points=points[i : i + batch_size]
        )


batch_upload(text_points)
batch_upload(image_points)

# ✅ 11. 업로드 결과 확인
count = client.count(collection_name="gptrip_places", exact=True).count
print(f"\n✅ 업로드 완료! 총 저장된 포인트 수: {count}")

client.close()
