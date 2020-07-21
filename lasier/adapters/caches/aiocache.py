from lasier.types import Timeout

from .base import AsyncCacheAdapterBase


class Adapter(AsyncCacheAdapterBase):
    async def add(self, key: str, value: int, timeout: Timeout = None) -> None:
        try:
            await super().add(key, value, timeout)
        except ValueError:
            return

    async def incr(self, key: str) -> int:
        """
        According to aiocache docs:
        Value of the key once incremented. -1 if key is not found.
        """
        value = await self.cache.increment(key)
        if value == -1:
            return 1
        return value

    async def flushdb(self) -> None:
        await self.cache.clear()
