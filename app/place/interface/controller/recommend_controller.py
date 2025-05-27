from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from model.prompt import parse_form, PromptModel
from model.response import PlaceResponse
from dependency_injector.wiring import inject, Provide
from typing import Optional
from place.application.recommend_service import RecommendService
from containers import Container

router = APIRouter(prefix="/recommend", tags=["Recommend API"])


@router.post("/recommend", response_model=list[PlaceResponse])
@inject
async def recommend_place(
    prompt: PromptModel = Depends(parse_form),
    image: Optional[UploadFile] = File(None),
    recommend_service: RecommendService = Depends(Provide[Container.recommend_service]),
):
    try:
        text = prompt.text.strip() if prompt.text else None
        image_bytes = await image.read() if image else None

        if not text and not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="텍스트 또는 이미지를 최소 하나는 입력해야 합니다.",
            )

        results = recommend_service.recommend(text=text, image=image_bytes)

        return results
    except HTTPException as e:
        raise e  # ⬅ 이미 준비한 HTTP 오류는 그대로 전달

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # ⬅ 진짜 예외는 500 처리
