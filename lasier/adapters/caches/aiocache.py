from typing import Optional, Union

from .base import AsyncCacheAdapterBase


class Adapter(AsyncCacheAdapterBase):
    async def add(
        self, key: str, value: int, timeout: Optional[Union[int, float]] = None
    ) -> None:
        try:
            await super().add(key, value, timeout)
        except ValueError:
            return

    async def incr(self, key: str) -> int:
        return await self.cache.increment(key)

    async def flushdb(self) -> None:
        await self.cache.clear()
