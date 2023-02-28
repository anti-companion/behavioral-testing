from pydantic import BaseSettings


class Settings(BaseSettings):
    model_name: str

    class Config:
        env_file = ".env"
