from lasier.types import Timeout

from .base import AsyncCacheAdapterBase


class Adapter(AsyncCacheAdapterBase):
    async def add(self, key: str, value: int, timeout: Timeout = None) -> None:
        await self.cache.set(key, value, timeout, nx=True)
