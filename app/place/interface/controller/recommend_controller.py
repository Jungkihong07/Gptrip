from fastapi import APIRouter, Depends, UploadFile, File
from app.model.prompt import parse_form, PromptModel
from app.model.response import RecommendModel
from typing import List

router = APIRouter(prefix="/recommend", tags=["Recommend API"])


@router.post("/recommend", response_class=List[RecommendModel])
async def recommend_place(
    prompt: PromptModel = Depends(parse_form), image: UploadFile = File(...)
):
    pass
