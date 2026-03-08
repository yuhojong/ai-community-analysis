import discord
import asyncio
from .base import BaseScraper
import datetime

class DiscordScraper(BaseScraper):
    def __init__(self, token):
        self.token = token
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.client = discord.Client(intents=self.intents)

    async def login(self):
        # Discord bot login is handled by client.start()
        pass

    async def fetch_messages(self, guild_id, channel_id=None, days_ago=1):
        messages = []
        target_date = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=days_ago)

        # Using a slightly cleaner approach to manage client start/stop
        class ScraperClient(discord.Client):
            def __init__(self, *args, **kwargs):
                self.messages = []
                super().__init__(*args, **kwargs)

            async def on_ready(self):
                guild = self.get_guild(int(guild_id))
                if not guild:
                    print(f"Guild {guild_id} not found.")
                    await self.close()
                    return

                channels = [guild.get_channel(int(channel_id))] if channel_id else guild.text_channels

                for channel in channels:
                    if not isinstance(channel, discord.TextChannel):
                        continue

                    print(f"Fetching messages from channel: {channel.name}")
                    try:
                        async for message in channel.history(after=target_date, limit=None):
                            if not message.author.bot:
                                self.messages.append({
                                    'channel_id': str(channel.id),
                                    'channel_name': channel.name,
                                    'author': str(message.author),
                                    'content': message.content,
                                    'posted_at': message.created_at,
                                    'message_id': str(message.id)
                                })
                    except discord.Forbidden:
                        print(f"Access denied to channel: {channel.name}")

                await self.close()

        client = ScraperClient(intents=self.intents)
        await client.start(self.token)
        return client.messages

    async def close(self):
        if not self.client.is_closed():
            await self.client.close()

    async def fetch_posts(self, target, **kwargs):
        # Implementation to match base interface
        return await self.fetch_messages(target, **kwargs)
