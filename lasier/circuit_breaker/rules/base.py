import abc
from typing import Optional


class BaseRule(metaclass=abc.ABCMeta):
    def __init__(
        self, failure_cache_key: str, request_cache_key: Optional[str] = None
    ) -> None:
        self.failure_cache_key = failure_cache_key
        self.request_cache_key = request_cache_key

    @abc.abstractmethod
    def should_open_circuit(
        self, total_failures: int, total_requests: int
    ) -> bool:
        pass

    def should_increase_failure_count(self) -> bool:
        return self.failure_cache_key is not None

    def should_increase_request_count(self) -> bool:
        return self.request_cache_key is not None

    @abc.abstractmethod
    def log_increase_failures(
        self, total_failures: int, total_requests: int
    ) -> None:
        pass
