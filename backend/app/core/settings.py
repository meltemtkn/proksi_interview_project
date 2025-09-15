import os
from pydantic_settings import BaseSettings
from pydantic_core import MultiHostUrl
from pydantic import (
    PostgresDsn,
    computed_field
)

class Settings(BaseSettings):
    # DB settings
    POSTGRES_USER: str = os.getenv('POSTGRES_USER', 'user')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', 'password')
    POSTGRES_DB: str = os.getenv('POSTGRES_DB', 'proksi_db')
    POSTGRES_PORT: int = int(os.getenv('POSTGRES_PORT', 5433)) 
    POSTGRES_HOST: str = os.getenv('POSTGRES_HOST', 'localhost')

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return str(MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        ))
    
    # Redis/Celery settings
    REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT: int = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB: int = int(os.getenv('REDIS_DB', 0))
    
    @computed_field
    @property
    def CELERY_BROKER_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    @computed_field
    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # First superuser settings
    FIRST_SUPERUSER: str = os.getenv('FIRST_SUPERUSER', 'admin@example.com')
    FIRST_SUPERUSER_PASSWORD: str = os.getenv('FIRST_SUPERUSER_PASSWORD', 'admin123')
    
    # App settings
    WORKERS: int = int(os.getenv('WORKERS', 1))
    
    class Config:
        case_sensitive = True

settings = Settings()