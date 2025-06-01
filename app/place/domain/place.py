from pydantic import BaseModel
from typing import Optional


class Place(BaseModel):
    title: str
    tel: Optional[str] = None
    addr1: Optional[str] = None
    addr2: Optional[str] = None
    contentid: int
    region: str
    mapx: float
    mapy: float
    image: Optional[str] = None
    emotional_summary: str
