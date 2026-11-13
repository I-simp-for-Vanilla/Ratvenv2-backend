from pydantic_settings import BaseSettings

"""Charge les variables d'environnement"""
class Settings(BaseSettings):
    db_host: str = "localhost"
    db_user: str
    db_password: str
    db_port: int = 3306
    pool_size: int = 30

    class Config:
        env_file = ".env"

settings = Settings()