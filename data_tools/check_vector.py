import numpy as np
import pickle

# 텍스트 임베딩 차원 확인
text_embeddings = np.load("data/incheon_place_embeddings.npy", allow_pickle=True)
print("텍스트 임베딩 shape:", text_embeddings.shape)

# 이미지 임베딩 차원 확인
with open("data/images/incheon_image_embeddings.pkl", "rb") as f:
    image_data = pickle.load(f)

image_embeddings = image_data["features"]
filenames = image_data["filenames"]

print("이미지 임베딩 shape:", image_embeddings.shape)
print("예시 파일명:", filenames[:3])
