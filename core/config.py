from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ALLOWED_ORIGINS: str = "*"
    ENVIRONMENT: str = "production"

    model_config = {"env_file": ".env"}


settings = Settings()
