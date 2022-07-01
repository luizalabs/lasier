from typing import Optional

from lasier.types import Timeout

from .base import AsyncCacheAdapterBase, CacheAdapterBase


class Adapter(CacheAdapterBase):
    def expire(self, key: str, timeout: Timeout = None) -> None:
        self.cache.touch(key, timeout)

    def incr(self, key: str) -> int:
        try:
            return self.cache.incr(key)
        except ValueError:
            self.cache.add(key, 1)
            return 1

    def flushdb(self) -> None:
        self.cache.clear()


class AdapterAsync(AsyncCacheAdapterBase):
    async def add(self, key: str, value: int, timeout: Timeout = None) -> None:
        await self.cache.aadd(key, value, timeout)

    async def set(self, key: str, value: int, timeout: Timeout = None) -> None:
        await self.cache.aset(key, value, timeout)

    async def incr(self, key: str) -> int:
        try:
            return await self.cache.aincr(key)
        except ValueError:
            await self.cache.aadd(key, 1)
            return 1

    async def get(self, key: str) -> Optional[int]:
        return self._convert_to_int(await self.cache.aget(key))

    async def expire(self, key: str, timeout: Timeout) -> None:
        await self.cache.atouch(key, timeout)

    async def delete(self, key: str) -> None:
        await self.cache.adelete(key)

    async def flushdb(self) -> None:
        await self.cache.aclear()
