# app/main.py
from fastapi import FastAPI
from place.interface.controller.recommend_controller import (
    router as recommend_router,
)
from fastapi.middleware.cors import CORSMiddleware  # 🔹 추가
import uvicorn
from containers import Container


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI(
        title="GPtrip API",
        description="텍스트·이미지 기반 장소 추천 API",
        version="1.0.0",
    )

    app.container = container

    # wire()는 반드시 container 등록 이후에 호출
    container.wire(modules=["place.interface.controller.recommend_controller"])

    app.include_router(recommend_router)
    # 🔹 CORS 설정 추가
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "*"
        ],  # 또는 ["http://127.0.0.1:5500", "https://your-frontend.vercel.app"]
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


app = create_app()


@app.get("/")
def hello():
    return {"message": "Hello from your FastAPI app!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
