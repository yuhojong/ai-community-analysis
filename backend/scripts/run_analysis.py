import asyncio
import datetime
import os
from sqlalchemy.future import select
from backend.database import AsyncSessionLocal
from backend.models import Platform, CommunityTarget, Channel, CollectedData, Report, SystemConfig
from scrapers.daum_cafe import DaumCafeScraper
from scrapers.discord_scraper import DiscordScraper
from backend.llm_service import LLMService
from backend.report_generator import ReportGenerator
from backend.slack_notifier import SlackNotifier

async def run_daily_analysis():
    print(f"Starting daily analysis at {datetime.datetime.now()}")
    async with AsyncSessionLocal() as db:
        # 1. Fetch active platforms and targets
        platforms = await db.execute(select(Platform).where(Platform.is_active == True))
        platforms = platforms.scalars().all()

        llm_provider = await SystemConfig.get_value(db, "LLM_PROVIDER", "openai")
        llm = LLMService(provider=llm_provider)

        slack_token = await SystemConfig.get_value(db, "SLACK_TOKEN") or os.getenv("SLACK_TOKEN")
        slack_channel_id = await SystemConfig.get_value(db, "SLACK_CHANNEL_ID") or os.getenv("SLACK_CHANNEL_ID")
        slack = SlackNotifier(slack_token) if slack_token else None

        analysis_results = []

        for platform in platforms:
            targets = await db.execute(select(CommunityTarget).where(CommunityTarget.platform_id == platform.id, CommunityTarget.is_active == True))
            targets = targets.scalars().all()

            scraper = None
            if platform.name == 'daum':
                scraper = DaumCafeScraper(headless=True)
                await scraper.start()

                daum_id = platform.config.get("daum_id") if platform.config else None
                daum_pw = platform.config.get("daum_pw") if platform.config else None

                if not daum_id or not daum_pw:
                    daum_id = os.getenv("DAUM_ID")
                    daum_pw = os.getenv("DAUM_PW")

                await scraper.login(daum_id, daum_pw)
            elif platform.name == 'discord':
                discord_token = platform.config.get("discord_token") if platform.config else None
                if not discord_token:
                    discord_token = os.getenv("DISCORD_TOKEN")
                scraper = DiscordScraper(discord_token)

            if not scraper:
                continue

            for target in targets:
                channels = await db.execute(select(Channel).where(Channel.target_id == target.id))
                channels = channels.scalars().all()

                for channel in channels:
                    print(f"Scraping {platform.name} - {target.name} - {channel.name}")
                    posts = await scraper.fetch_posts(target.target_url, channel.identifier)

                    # Store posts in DB
                    for post in posts:
                        new_data = CollectedData(
                            channel_id=channel.id,
                            author=post['author'],
                            content=post['content'],
                            posted_at=post['posted_at'],
                            external_id=post['external_id']
                        )
                        db.add(new_data)

                    # Analyze using LLM
                    if posts:
                        analysis = await llm.analyze_content(posts, target_lang=channel.language, db=db)
                        analysis_results.append({
                            'platform': platform.name,
                            'target': target.name,
                            'channel': channel.name,
                            'analysis': analysis
                        })

            if hasattr(scraper, 'close'):
                await scraper.close()

        await db.commit()

        # 6. Generate Markdown Report
        report_md = ReportGenerator.generate_markdown(datetime.date.today(), analysis_results)
        ReportGenerator.save_to_file(report_md, f"data/report_{datetime.date.today()}.md")

        # 7. Notify via Slack
        if slack and analysis_results:
            slack.post_message(slack_channel_id, f"데일리 커뮤니티 분석 리포트 완료\n\n{report_md[:1000]}...") # Slack limit 40k chars, but let's keep it brief

        print("Daily analysis completed successfully.")

if __name__ == "__main__":
    asyncio.run(run_daily_analysis())
