from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    tourapi_key: str
    qdrant_api_key: str
    qdrant_host: str
    qdrant_gptrip_cluster: str


@lru_cache
def get_settings():
    return Settings()
