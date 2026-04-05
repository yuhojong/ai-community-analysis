import os
import secrets
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings, SettingsConfigDict

import shutil
import urllib.parse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")
EXAMPLE_ENV_PATH = os.path.join(BASE_DIR, "example.env")

if not os.path.exists(ENV_PATH):
    if os.path.exists(EXAMPLE_ENV_PATH):
        with open(EXAMPLE_ENV_PATH, 'r') as example_file:
            content = example_file.read()

        # Generate a secure random secret key
        secure_key = secrets.token_urlsafe(32)
        content = content.replace("your_secret_key_here", secure_key)

        with open(ENV_PATH, 'w') as env_file:
            env_file.write(content)
        print(f"Created {ENV_PATH} from example.env with a securely generated SECRET_KEY")
    else:
        with open(ENV_PATH, "w") as f:
            pass
        print(f"Created empty {ENV_PATH}")

class Settings(BaseSettings):
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: str = "3306"
    MYSQL_DB: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        extra="ignore"
    )

settings = Settings()  # type: ignore

SQLALCHEMY_DATABASE_URL = f"mysql+aiomysql://{urllib.parse.quote_plus(settings.MYSQL_USER)}:{urllib.parse.quote_plus(settings.MYSQL_PASSWORD)}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
