import asyncio
from backend.database import engine, Base
from backend.models import User, Platform, CommunityTarget, Channel, CollectedData, Report

async def init_db():
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)
        print("Database tables created successfully.")

if __name__ == "__main__":
    asyncio.run(init_db())
