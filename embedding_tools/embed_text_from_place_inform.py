# 파일명 예시: scripts/embed_text_from_overview.py

import os
import csv
import json
import numpy as np
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer

# 모델 로드
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

AREAS = ["seoul", "incheon", "gyeonggi", "daejeon"]
MAX_SENTENCES = 5


def build_text_input(row):
    title = row.get("title", "")
    addr1 = row.get("addr1", "")
    addr2 = row.get("addr2", "")
    overview = row.get("overview", "")
    return f"{title} / {addr1} {addr2} / {overview}"


def embed_overview_text(text, max_sentences=MAX_SENTENCES):
    sentences = sent_tokenize(text)
    selected = sentences[:max_sentences]
    embeddings = model.encode(selected, convert_to_numpy=True, batch_size=4)
    return np.mean(embeddings, axis=0)


def generate_text_embeddings():
    os.makedirs("text_embeddings", exist_ok=True)

    for area in AREAS:
        input_path = f"data/{area}_places_with_overview.csv"
        output_path = f"text_embeddings/{area}_text_embeddings.json"

        if not os.path.exists(input_path):
            print(f"❌ Missing input: {input_path}")
            continue

        print(f"🔄 Embedding: {area}")
        result = {}

        with open(input_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                contentid = row.get("contentid")
                if not contentid:
                    continue
                text_input = build_text_input(row)
                vector = embed_overview_text(text_input)
                result[contentid] = vector.tolist()

        with open(output_path, "w", encoding="utf-8") as out:
            json.dump(result, out, ensure_ascii=False)

        print(f"✅ Saved: {output_path}")


if __name__ == "__main__":
    generate_text_embeddings()
