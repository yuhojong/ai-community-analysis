from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from .scripts.run_analysis import run_daily_analysis

scheduler = AsyncIOScheduler()

def start_scheduler(hour=9, minute=0):
    scheduler.add_job(run_daily_analysis, 'cron', hour=hour, minute=minute)
    scheduler.start()
    print(f"Scheduler started to run daily at {hour:02d}:{minute:02d}")

if __name__ == "__main__":
    # For testing, running once and starting scheduler
    asyncio.run(run_daily_analysis())
    start_scheduler()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
