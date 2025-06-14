from place.domain.place import Place as PlaceVO


def map_place(row: dict) -> PlaceVO:
    # User 객체 생성
    user = PlaceVO(
        title=row.get("title"),
        tel=row.get("tel"),
        addr1=row.get("addr1"),
        addr2=row.get("addr2"),
        contentid=int(row["contentid"]),
        region=row.get("region"),
        mapx=float(row["mapx"]),
        mapy=float(row["mapy"]),
        image=row.get("firstimage"),  # 또는 원하는 image source
        emotional_summary=row.get(
            "emotional_summary", ""
        ),  # 만약에 값이 없으면 그냥 ""
    )

    return user
