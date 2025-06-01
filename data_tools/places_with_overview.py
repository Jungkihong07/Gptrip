# 해당 코드는 기존의 관광지 csv 파일이 이미 있는 것을 전제 조건으로 한다. 따라서 tourapi_fetcet.py를 미리 실행하고 올 것.
import os
import csv
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TOURAPI_KEY")
DETAIL_API_URL = "http://apis.data.go.kr/B551011/KorService1/detailCommon1"


def fetch_overview(content_id: str) -> str:
    """contentid 기반으로 /detailCommon1 API에서 overview 가져오기"""
    params = {
        "MobileOS": "ETC",
        "MobileApp": "travel_recommender",
        "_type": "json",
        "contentId": content_id,
        "overviewYN": "Y",
    }

    query = f"serviceKey={API_KEY}&{urlencode(params)}"
    url = f"{DETAIL_API_URL}?{query}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        item = data.get("response", {}).get("body", {}).get("items", {}).get("item", {})
        # 리스트 대응
        if isinstance(item, list):
            item = item[0]

        return item.get("overview", "").replace("\n", " ").replace("\r", " ")
    except Exception as e:
        print(f"❌ Failed to fetch overview for {content_id}: {e}")
        return ""


def run_for_area(area: str, input_path: str, output_path: str):

    if not os.path.exists(input_path):
        print(f"❌ Input CSV not found: {input_path}")
        return

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"🔍 Processing {area}...")

    with open(input_path, newline="", encoding="utf-8") as infile, open(
        output_path, "w", newline="", encoding="utf-8"
    ) as outfile:

        reader = csv.DictReader(infile)
        fieldnames = [
            "title",
            "addr1",
            "addr2",
            "mapx",
            "mapy",
            "contentid",
            "modifiedtime",
            "overview",
        ]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            content_id = row.get("contentid")
            if not content_id or not content_id.isdigit():
                print(f"⚠️ Skipping invalid content_id: {content_id}")
                continue

            overview = fetch_overview(content_id)

            writer.writerow(
                {
                    "title": row.get("title", ""),
                    "addr1": row.get("addr1", ""),
                    "addr2": row.get("addr2", ""),
                    "mapx": row.get("mapx", ""),
                    "mapy": row.get("mapy", ""),
                    "contentid": content_id,
                    "modifiedtime": row.get("modifiedtime", ""),
                    "overview": overview,
                }
            )

        print(f"✅ Saved: {output_path}")


Areas = ["seoul", "incheon", "gyeonggi", "daejeon"]

if __name__ == "__main__":

    for area in Areas:
        input_path = f"data/{area}_places.csv"
        output_path = f"data/{area}_places_with_overview.csv"
        run_for_area(area, input_path, output_path)
