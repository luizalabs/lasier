from typing import Optional, Union

from .base import CacheAdapterBase


class Adapter(CacheAdapterBase):
    def expire(
        self, key: str, timeout: Optional[Union[int, float]] = None
    ) -> None:
        self.cache.touch(key, timeout)
