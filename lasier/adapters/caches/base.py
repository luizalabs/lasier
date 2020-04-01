
class CacheAdapterBase:

    def __init__(self, cache):
        self.cache = cache

    def add(self, key, value, timeout=None):
        return self.cache.add(key, value, timeout)

    def set(self, key, value, timeout=None):
        return self.cache.set(key, value, timeout)

    def incr(self, key):
        return self.cache.incr(key)

    def get(self, key):
        return self._convert_to_int(self.cache.get(key))

    def delete(self, key):
        return self.cache.delete(key)

    def flushdb(self):
        return self.cache.flushdb()

    def _convert_to_int(self, value):
        if value is not None:
            return int(value)
        return None


class AsyncCacheAdapterBase(CacheAdapterBase):

    async def add(self, key, value, timeout=None):
        return await self.cache.add(key, value, timeout)

    async def set(self, key, value, timeout=None):
        return await self.cache.set(key, value, timeout)

    async def incr(self, key):
        return await self.cache.incr(key)

    async def get(self, key):
        return self._convert_to_int(await self.cache.get(key))

    async def delete(self, key):
        return await self.cache.delete(key)

    async def flushdb(self):
        return await self.cache.flushdb()
