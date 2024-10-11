from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str
    DB_CONNECTION: str
    DB_NAME: str
    API_STR: str = "/api"

# Crear una instancia de Settings que cargará las variables desde el archivo .env
settings = Settings()