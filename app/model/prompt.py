from pydantic import BaseModel
from fastapi import Form


class PromptModel(BaseModel):
    text: str


# Form()은 BaseModel에 직접 쓸 수 없기 때문에, parse_form() 같은 함수를 만들어 Depends()로 의존성 주입
""" Form에서 받아서 PromptModel로 변환하는 의존성 주입 함수 """


def parse_form(text: str = Form(...)) -> PromptModel:
    return PromptModel(text=text)
