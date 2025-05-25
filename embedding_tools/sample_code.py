from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")
embedding = model.encode("광화문은 경복궁의 정문입니다.")

# 유사도 비교
similarity = util.cos_sim(
    embedding, model.encode("경복궁의 주요 입구는 광화문이다.")
).item()

print(similarity)
