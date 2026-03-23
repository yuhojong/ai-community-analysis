"""Script to manually trigger backend functions."""

import argparse
import asyncio
from backend.scripts.run_analysis import run_daily_analysis
from backend.scripts.init_db import init_db

def main():
    """Parses arguments and runs the requested backend function."""
    parser = argparse.ArgumentParser(
        description="Trigger backend functions for testing and maintenance"
    )
    parser.add_argument("action", choices=["run_analysis", "init_db"], help="The action to perform")

    args = parser.parse_args()

    if args.action == "run_analysis":
        print("Triggering daily analysis...")
        asyncio.run(run_daily_analysis())
    elif args.action == "init_db":
        print("Triggering database initialization...")
        asyncio.run(init_db())

if __name__ == "__main__":
    main()
