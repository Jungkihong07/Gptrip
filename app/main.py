# app/main.py
from fastapi import FastAPI
from place_recommend.interface.controller.recommend_controller import (
    router as recommend_router,
)
import uvicorn

app = FastAPI()
app.include_router(recommend_router)


@app.get("/")
def hello():
    return {"message": "Hello from your FastAPI app!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
