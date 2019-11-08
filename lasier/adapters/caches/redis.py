from .base import CacheAdapterBase


class RedisAdapter(CacheAdapterBase):

    def add(self, key, value, timeout):
        return self.cache.set(key, value, timeout, nx=True)
