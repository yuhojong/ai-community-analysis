import logging
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from .scripts.run_analysis import run_daily_analysis

scheduler = AsyncIOScheduler()

def start_scheduler(hour=9, minute=0):
    scheduler.add_job(run_daily_analysis, 'cron', hour=hour, minute=minute)
    scheduler.start()
    print(f"Scheduler started to run daily at {hour:02d}:{minute:02d}")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    # For testing, running once and starting scheduler
    asyncio.run(run_daily_analysis())
    start_scheduler()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutdown signal received, exiting...")
        sys.exit(0)
