from typing import Optional

from .base import CacheAdapterBase


class Adapter(CacheAdapterBase):

    def add(
        self, key: str, value: int, timeout: Optional[int] = None
    ) -> None:
        self.cache.set(key, value, timeout, nx=True)
