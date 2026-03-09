import asyncio
import sys
from backend.database import engine, Base
from backend.models import User, Platform, CommunityTarget, Channel, CollectedData, Report
from sqlalchemy.exc import OperationalError

async def init_db():
    try:
        async with engine.begin() as conn:
            # Create tables
            await conn.run_sync(Base.metadata.create_all)
            print("Database tables created successfully.")
    except OperationalError as e:
        print("\nError: Could not connect to the database.", file=sys.stderr)
        print("Please ensure that the MySQL server is running and the credentials in your .env file are correct.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(init_db())
