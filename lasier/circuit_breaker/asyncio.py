import asyncio
from functools import wraps

from .base import CircuitBreakerBase


class CircuitBreaker(CircuitBreakerBase):

    async def is_circuit_open(self):
        return await self.cache.get(self.circuit_cache_key) or False

    async def total_failures(self):
        return await self.cache.get(self.rule.failure_cache_key) or 0

    async def total_requests(self):
        return await self.cache.get(self.rule.request_cache_key) or 0

    async def open_circuit(self):
        await self.cache.set(
            self.circuit_cache_key,
            1,
            self.circuit_timeout
        )

        # Delete the cache key to mitigate multiple sequentials openings
        # when a key is created accidentally without timeout (from an incr
        # operation)
        await asyncio.gather(
            self.cache.delete(self.rule.failure_cache_key),
            self.cache.delete(self.rule.request_cache_key)
        )

        self._notify_open_circuit()

    async def __aenter__(self):
        if await self.is_circuit_open():
            raise self.failure_exception

        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._increase_request_count()
        if self._is_catchable_exception(exc_type):
            await self._increase_failure_count()

            total_failures = await self.total_failures()
            total_requests = await self.total_requests()

            if self.rule.should_open_circuit(
                total_failures=total_failures,
                total_requests=total_requests
            ):
                await self.open_circuit()
                self._notify_max_failures_exceeded()
                raise self.failure_exception

    def __call__(self, func):
        @wraps(func)
        async def inner(*args, **kwargs):
            async with self:
                return await func(*args, **kwargs)
        return inner

    async def _increase_failure_count(self):
        if (
            await self.is_circuit_open() or
            not self.rule.should_increase_failure_count()
        ):
            return

        # Between the cache.add and cache.incr, the cache MAY expire,
        # which will lead to a circuit that will eventually open
        await self.cache.add(
            self.rule.failure_cache_key,
            0,
            self.failure_timeout
        )

        total_failures = await self.cache.incr(self.rule.failure_cache_key)
        total_requests = await self.total_requests()

        self.rule.log_increase_failures(
            total_failures=total_failures,
            total_requests=total_requests
        )

    async def _increase_request_count(self):
        if (
            await self.is_circuit_open() or
            not self.rule.should_increase_request_count()
        ):
            return

        await self.cache.add(
            self.rule.request_cache_key,
            0,
            self.failure_timeout
        )
        # To calculate the exact percentage, the cache of requests and the
        # cache of failures must expire at the same time.
        if self.rule.should_increase_failure_count():
            await self.cache.add(
                self.rule.failure_cache_key, 0, self.failure_timeout
            )

        await self.cache.incr(self.rule.request_cache_key)


circuit_breaker = CircuitBreaker
