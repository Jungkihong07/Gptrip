# 각 지역별로 관광 데이터 정보를 가져오기 위한 코드.


import os
import requests
import csv
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://apis.data.go.kr/B551011/KorService1/areaBasedList1"
API_KEY = os.getenv("TOURAPI_KEY")

# 지역명과 지역코드 매핑 (수도권 중심)
AREA_CODES = {
    "seoul": 1,
    "incheon": 2,
    "daejeon": 3,  # 대전
    "gyeonggi": 31,  # 경기도
}


def fetch_tour_data(area_name: str):
    area_code = AREA_CODES.get(area_name.lower())
    if area_code is None:
        print(f"⚠️ Invalid area name: {area_name}")
        return

    params = {
        "numOfRows": 10000,
        "MobileOS": "ETC",
        "MobileApp": "travel_recommender",
        "arrange": "O",
        "contentTypeId": 12,  # 관광지
        "areaCode": area_code,
        "_type": "json",
    }

    # 직접 serviceKey를 URL에 붙이고, 나머지만 urlencode
    query_string = f"serviceKey={API_KEY}&{urlencode(params)}"
    url = f"{BASE_URL}?{query_string}"
    try:
        response = requests.get(url, timeout=100)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"❌ Request failed for {area_name}: {e}")
        return
    except ValueError:
        print(f"❌ Failed to parse JSON for {area_name}")
        return

    items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
    print(f"[{area_name.title()}] Fetched {len(items)} items.")

    os.makedirs("data", exist_ok=True)
    output_file = f"data/{area_name.lower()}_places.csv"

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "title",
                "tel",
                "addr1",
                "addr2",
                "mapx",
                "mapy",
                "contentid",
                "firstimage",
                "firstimage2",
                "modifiedtime",
            ],
        )
        writer.writeheader()
        for item in items:
            writer.writerow(
                {
                    "title": item.get("title"),
                    "tel": item.get("tel"),
                    "addr1": item.get("addr1"),
                    "addr2": item.get("addr2"),
                    "mapx": item.get("mapx"),
                    "mapy": item.get("mapy"),
                    "contentid": item.get("contentid"),
                    "firstimage": item.get("firstimage"),
                    "firstimage2": item.get("firstimage2"),
                    "modifiedtime": item.get("modifiedtime"),
                }
            )

    print(f"[{area_name.title()}] Saved to {output_file}")


if __name__ == "__main__":
    # 원하는 지역들 입력 (원하면 여기만 바꾸면 됨)
    areas_to_fetch = ["gyeonggi"]

    for area in areas_to_fetch:
        fetch_tour_data(area)
