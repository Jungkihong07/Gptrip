# contentID를 기반으로 사진을 저장하고 사진의 이름을 contentID로 구성하는 코드


import os
import csv
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TOURAPI_KEY")
IMAGE_API_URL = "http://apis.data.go.kr/B551011/KorService1/detailImage1"


def fetch_and_save_images_from_contentid(content_id: str, save_dir: str) -> list:
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

    metadata_list = []

    for idx, item in enumerate(items):
        image_url = item.get("originimgurl")
        if not image_url:
            continue

        filename = f"{content_id}_{idx+1}.jpg"
        save_path = os.path.join(save_dir, filename)
        if download_image(image_url, save_path):
            metadata_list.append(
                {"contentid": content_id, "filename": filename, "image_url": image_url}
            )
    return metadata_list


def download_image(url: str, path: str):
    """이미지 URL로부터 파일 다운로드"""
    if os.path.exists(path):
        print(f"✅ Already exists: {path}")
        return True
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(path, "wb") as f:
            f.write(response.content)
        print(f"⬇️ Downloaded: {path}")
        return True
    except requests.RequestException as e:
        print(f"❌ Failed to download {url}: {e}")
        return False
    except OSError as e:
        print(f"❌ Failed to save image {path}: {e}")
        return False


def run_from_csv(csv_path: str, save_dir: str, metadata_csv_path: str):
    # 만약 csv 파일이 존재하지 않을 경우
    if not os.path.exists(csv_path):
        print(f"❌ CSV not found: {csv_path}")
        return

    metadata_all = []

    # csv 파일을 통해서 저장 진행
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            content_id = row.get("contentid")
            if not content_id or not content_id.isdigit():
                print(f"⚠️ Skipping invalid content_id: {content_id}")
                continue
            metadata = fetch_and_save_images_from_contentid(content_id, save_dir)
            if metadata:
                metadata_all.extend(metadata)

    if metadata_all:
        with open(metadata_csv_path, "w", newline="", encoding="utf-8") as out_csv:
            writer = csv.DictWriter(
                out_csv, fieldnames=["contentid", "filename", "image_url"]
            )
            writer.writeheader()
            writer.writerows(metadata_all)
        print(f"📁 Saved image metadata to {metadata_csv_path}")
    else:
        print(f"⚠️ No image metadata to save for {csv_path}")


# Areas = ["seoul", "incheon", "gyeonggi", "daejeon"]
Areas = ["incheon"]


if __name__ == "__main__":

    for area in Areas:
        csv_path = f"data/{area}_places.csv"
        image_save_dir = f"data/images/{area}"
        image_url_path = f"data/image_url_{area}.csv"
        run_from_csv(csv_path, image_save_dir, image_url_path)
