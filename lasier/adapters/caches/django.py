from lasier.types import Timeout

from .base import CacheAdapterBase


class Adapter(CacheAdapterBase):
    def expire(self, key: str, timeout: Timeout = None) -> None:
        self.cache.touch(key, timeout)
