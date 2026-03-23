"""Script to initialize the database tables."""

import asyncio
import sys
from sqlalchemy.exc import OperationalError
from backend.database import engine, Base
import backend.models  # pylint: disable=unused-import

async def init_db():
    """Creates all tables defined in SQLAlchemy models."""
    try:
        async with engine.begin() as conn:
            # Create tables
            await conn.run_sync(Base.metadata.create_all)
            print("Database tables created successfully.")
    except OperationalError:
        print("\nError: Could not connect to the database.", file=sys.stderr)
        print(
            "Please ensure that the MySQL server is running "
            "and the credentials in your .env file are correct.",
            file=sys.stderr
        )
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())
