import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings, SettingsConfigDict

import shutil

import secrets

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")
EXAMPLE_ENV_PATH = os.path.join(BASE_DIR, "example.env")

def generate_env_file():
    secret_key = secrets.token_urlsafe(32)
    env_content = ""

    if os.path.exists(EXAMPLE_ENV_PATH):
        with open(EXAMPLE_ENV_PATH, "r") as f:
            env_content = f.read()

        # Replace dummy secret key with a real one
        if "SECRET_KEY=your_secret_key_here" in env_content:
            env_content = env_content.replace(
                "SECRET_KEY=your_secret_key_here",
                f"SECRET_KEY={secret_key}"
            )
        elif "SECRET_KEY=" not in env_content:
            env_content += f"\nSECRET_KEY={secret_key}\n"

        with open(ENV_PATH, "w") as f:
            f.write(env_content)
        print(f"Created {ENV_PATH} from example.env with a newly generated SECRET_KEY")
    else:
        # Fallback if example.env is missing
        with open(ENV_PATH, "w") as f:
            f.write(f"SECRET_KEY={secret_key}\n")
            f.write("MYSQL_USER=your_username\n")
            f.write("MYSQL_PASSWORD=your_password\n")
            f.write("MYSQL_HOST=localhost\n")
            f.write("MYSQL_PORT=3306\n")
            f.write("MYSQL_DB=community_analyzer\n")
        print(f"Created new {ENV_PATH} with default values and a newly generated SECRET_KEY")

if not os.path.exists(ENV_PATH):
    generate_env_file()

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

settings = Settings()

SQLALCHEMY_DATABASE_URL = f"mysql+aiomysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
