from lasier.types import Timeout

from .base import CacheAdapterBase


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
