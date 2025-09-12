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
    
    # First superuser settings
    FIRST_SUPERUSER: str = os.getenv('FIRST_SUPERUSER', 'admin@example.com')
    FIRST_SUPERUSER_PASSWORD: str = os.getenv('FIRST_SUPERUSER_PASSWORD', 'admin123')
    
    class Config:
        case_sensitive = True

settings = Settings()