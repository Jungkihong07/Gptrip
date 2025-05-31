# contentID를 기반으로 사진을 저장하고 사진의 이름을 contentID로 구성하는 코드


import os
import csv
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TOURAPI_KEY")
IMAGE_API_URL = "http://apis.data.go.kr/B551011/KorService1/detailImage1"


def fetch_and_save_images_from_contentid(content_id: str, save_dir: str):
    """지정된 contentid로 TourAPI 이미지 리스트를 조회하고 로컬에 저장"""
    os.makedirs(save_dir, exist_ok=True)

    params = {
        "serviceKey": API_KEY,
        "MobileOS": "ETC",
        "MobileApp": "travel_recommender",
        "_type": "json",
        "contentId": content_id,
        "imageYN": "Y",
        "subImageYN": "Y",
    }

    # 직접 serviceKey를 URL에 붙이고, 나머지만 urlencode
    query_string = f"serviceKey={API_KEY}&{urlencode(params)}"
    url = f"{IMAGE_API_URL}?{query_string}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"❌ HTTP error for {content_id}: {e}")
        return
    except ValueError:
        print(f"❌ Invalid JSON response for {content_id}")
        return

    try:
        items = (
            data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
        )
    except AttributeError:
        print(f"❌ Unexpected JSON structure for {content_id}")
        return

    if not items:
        print(f"⚠️ No images found for content_id: {content_id}")
        return

    for idx, item in enumerate(items):
        image_url = item.get("originimgurl")
        if not image_url:
            continue

        filename = f"{content_id}_{idx+1}.jpg"
        save_path = os.path.join(save_dir, filename)
        download_image(image_url, save_path)


def download_image(url: str, path: str):
    """이미지 URL로부터 파일 다운로드"""
    if os.path.exists(path):
        print(f"✅ Already exists: {path}")
        return
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(path, "wb") as f:
            f.write(response.content)
        print(f"⬇️ Downloaded: {path}")
    except requests.RequestException as e:
        print(f"❌ Failed to download {url}: {e}")
    except OSError as e:
        print(f"❌ Failed to save image {path}: {e}")


def run_from_csv(csv_path: str, save_dir: str):
    # 만약 csv 파일이 존재하지 않을 경우
    if not os.path.exists(csv_path):
        print(f"❌ CSV not found: {csv_path}")
        return
    # csv 파일을 통해서 저장 진행
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            content_id = row.get("contentid")
            if not content_id or not content_id.isdigit():
                print(f"⚠️ Skipping invalid content_id: {content_id}")
                continue
            fetch_and_save_images_from_contentid(content_id, save_dir)


Areas = ["seoul", "incheon", "gyeonggi", "daejeon"]


if __name__ == "__main__":

    for area in Areas:
        csv_path = f"data/{area}_places.csv"
        image_save_dir = f"data/images/{area}"
        run_from_csv(csv_path, image_save_dir)
