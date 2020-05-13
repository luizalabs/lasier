from typing import Optional, Union

from .base import CacheAdapterBase


class Adapter(CacheAdapterBase):
    def add(
        self, key: str, value: int, timeout: Optional[Union[int, float]] = None
    ) -> None:
        self.cache.set(key, value, timeout, nx=True)
