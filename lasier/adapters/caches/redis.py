from lasier.types import Timeout

from .base import CacheAdapterBase


class Adapter(CacheAdapterBase):
    def add(self, key: str, value: int, timeout: Timeout = None) -> None:
        self.cache.set(key, value, timeout, nx=True)
