from pydantic import BaseModel
from typing import Optional


class RecommendModel(BaseModel):
    title: str
    tel: Optional[str]
    addr1: Optional[str]
    addr2: Optional[str]
    mapx: float
    mapy: float
    image: str
    summary: str
