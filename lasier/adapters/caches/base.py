from typing import Any, Optional, Union


class _CacheAdapterMixin:
    def __init__(self, cache: Any) -> None:
        self.cache = cache

    def _convert_to_int(self, value: Optional[str]) -> Optional[int]:
        if value is not None:
            return int(value)
        return None


class CacheAdapterBase(_CacheAdapterMixin):
    def add(
        self, key: str, value: int, timeout: Optional[Union[int, float]] = None
    ) -> None:
        self.cache.add(key, value, timeout)

    def set(
        self, key: str, value: int, timeout: Optional[Union[int, float]] = None
    ) -> None:
        self.cache.set(key, value, timeout)

    def incr(self, key: str) -> int:
        return self.cache.incr(key)

    def get(self, key: str) -> Optional[int]:
        return self._convert_to_int(self.cache.get(key))

    def expire(self, key: str, timeout: Optional[Union[int, float]]) -> None:
        self.cache.expire(key, timeout)

    def delete(self, key: str) -> None:
        self.cache.delete(key)

    def flushdb(self) -> None:
        self.cache.flushdb()


class AsyncCacheAdapterBase(_CacheAdapterMixin):
    async def add(
        self, key: str, value: int, timeout: Optional[Union[int, float]] = None
    ) -> None:
        await self.cache.add(key, value, timeout)

    async def set(
        self, key: str, value: int, timeout: Optional[Union[int, float]] = None
    ) -> None:
        await self.cache.set(key, value, timeout)

    async def incr(self, key: str) -> int:
        return await self.cache.incr(key)

    async def get(self, key: str) -> Optional[int]:
        return self._convert_to_int(await self.cache.get(key))

    async def expire(
        self, key: str, timeout: Optional[Union[int, float]]
    ) -> None:
        await self.cache.expire(key, timeout)

    async def delete(self, key: str) -> None:
        await self.cache.delete(key)

    async def flushdb(self) -> None:
        await self.cache.flushdb()
