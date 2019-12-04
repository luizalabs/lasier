from .base import CacheAdapterBase


class RedisAdapter(CacheAdapterBase):

    def add(self, key, value, timeout=None):
        return self.cache.set(key, value, timeout, nx=True)
