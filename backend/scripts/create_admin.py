import asyncio
import argparse
from backend.database import AsyncSessionLocal
from backend.models import User
from backend.auth import get_password_hash
from sqlalchemy.future import select

async def create_admin(username, password):
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create an admin user")
    parser.add_argument("--username", required=True, help="Admin username")
    parser.add_argument("--password", required=True, help="Admin password")
    args = parser.parse_args()

    asyncio.run(create_admin(args.username, args.password))
