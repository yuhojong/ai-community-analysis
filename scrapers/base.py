import asyncio
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    @abstractmethod
    async def login(self, **kwargs):
        pass

    @abstractmethod
    async def fetch_posts(self, target, **kwargs):
        pass

    @abstractmethod
    async def close(self):
        pass
