from .base import AsyncCacheAdapterBase


class Adapter(AsyncCacheAdapterBase):

    async def add(self, key, value, timeout=None):
        try:
            return await super().add(key, value, timeout)
        except ValueError:
            return True

    async def incr(self, key):
        return await self.cache.increment(key)

    async def flushdb(self):
        return await self.cache.clear()
