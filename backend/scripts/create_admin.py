import asyncio
import argparse
import getpass
import sys
from backend.database import AsyncSessionLocal, engine
from backend.models import User
from backend.auth import get_password_hash
from sqlalchemy.future import select
from sqlalchemy.exc import OperationalError

async def create_admin(username, password):
    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(User).where(User.username == username))
            existing_user = result.scalars().first()
            if existing_user:
                print(f"User {username} already exists.")
                return

            hashed_password = get_password_hash(password)
            new_user = User(username=username, hashed_password=hashed_password, is_admin=True)
            db.add(new_user)
            await db.commit()
            print(f"Admin user {username} created successfully.")
    except OperationalError as e:
        print("\nError: Could not connect to the database.", file=sys.stderr)
        print("Please ensure that the MySQL server is running and the credentials in your .env file are correct.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        await engine.dispose()

def main():
    parser = argparse.ArgumentParser(description="Create an admin user")
    parser.add_argument("--username", required=True, help="Admin username")
    args = parser.parse_args()

    try:
        password = getpass.getpass("Admin password: ")
        if not password:
            print("Password cannot be empty.")
            return

        asyncio.run(create_admin(args.username, password))
    except (EOFError, KeyboardInterrupt):
        print("\nAdmin password input cancelled.")
        sys.exit(1)

if __name__ == "__main__":
    main()
