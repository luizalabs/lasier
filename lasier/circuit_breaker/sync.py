from functools import wraps

from lasier.adapters.caches.base import CacheAdapterBase

from .base import CircuitBreakerBase


class CircuitBreaker(CircuitBreakerBase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not isinstance(self.cache, CacheAdapterBase):
            self.cache = CacheAdapterBase(self.cache)

    def is_circuit_open(self) -> bool:
        return self.cache.get(self.circuit_cache_key) == 1

    def get_total_failures(self) -> int:
        return self.cache.get(self.rule.failure_cache_key) or 0

    def get_total_requests(self) -> int:
        return self.cache.get(self.rule.request_cache_key) or 0

    def open_circuit(self) -> None:
        self.cache.set(self.circuit_cache_key, 1, self.circuit_timeout)

        # Delete the cache key to mitigate multiple sequentials openings
        # when a key is created accidentally without timeout (from an incr
        # operation)
        self.cache.delete(self.rule.failure_cache_key)
        self.cache.delete(self.rule.request_cache_key)

        self._notify_open_circuit()

    def __enter__(self):
        if self.is_circuit_open():
            raise self.failure_exception

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._increase_request_count()
        if self._is_catchable_exception(exc_type):
            self._increase_failure_count()

            if self.rule.should_open_circuit(
                total_failures=self.get_total_failures(),
                total_requests=self.get_total_requests(),
            ):
                self.open_circuit()
                self._notify_max_failures_exceeded()
                raise self.failure_exception

    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return inner

    def _increase_failure_count(self) -> None:
        if (
            self.is_circuit_open()
            or not self.rule.should_increase_failure_count()
        ):
            return

        # Between the cache.add and cache.incr, the cache MAY expire,
        # which will lead to a circuit that will eventually open
        self.cache.add(self.rule.failure_cache_key, 0, self.failure_timeout)
        total_failures = self.cache.incr(self.rule.failure_cache_key)

        self.rule.log_increase_failures(
            total_failures=total_failures,
            total_requests=self.get_total_requests(),
        )

    def _increase_request_count(self) -> None:
        if (
            self.is_circuit_open()
            or not self.rule.should_increase_request_count()
        ):
            return

        self.cache.add(self.rule.request_cache_key, 0, self.failure_timeout)
        # To calculate the exact percentage, the cache of requests and the
        # cache of failures must expire at the same time.
        if self.rule.should_increase_failure_count():
            self.cache.add(
                self.rule.failure_cache_key, 0, self.failure_timeout
            )

        self.cache.incr(self.rule.request_cache_key)


circuit_breaker = CircuitBreaker
