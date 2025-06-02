# 1. Python 3.12 slim base image
FROM python:3.12-slim

COPY .env .env
# 기본 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Poetry 설치
RUN pip install --upgrade pip && pip install poetry

# 작업 디렉토리 설정
WORKDIR /app
ENV PYTHONPATH=/app/app \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1



# Poetry 설정 복사 및 의존성 설치
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root --only main

# 나머지 앱 소스 복사
COPY . /app


# 8. FastAPI 실행 (기본 포트: 8080)
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]