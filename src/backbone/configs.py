from pathlib import Path

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DEFAULT_HEADERS: dict = {
        'User-Agent': 'MyApp/1.0',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'Custom-Header': 'CustomValue',
        'X-Api-Version': '2.0'
    }

    PDF_WEB: str = "src/data_file/pdf_web/"

    SCI_PATH: str = "https://sci-hub.wf/"

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "ali3z110"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_DATABASE: str = "postgres"
    POSTGRES_PORT: int = 5432


    class Config:
        case_sensitive = False
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        env_file = (str(BASE_DIR) + "/.env").replace("//", "/")
        env_file_encoding = 'utf-8'


config = Config()


class PasswordConfig:
    MIN_LENGTH = 8
    UPPERCASE_REQUIRED = False
    LOWERCASE_REQUIRED = True
    DIGIT_REQUIRED = True
    SPECIAL_CHARACTERS_REQUIRED = False
    SPECIAL_CHARACTERS = r"[!@#$%^&*()]"
