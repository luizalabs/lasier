import logging

from .base import BaseRule

logger = logging.getLogger(__name__)


class MaxFailuresRule(BaseRule):

    def __init__(self, max_failures: int, failure_cache_key: str) -> None:
        super().__init__(failure_cache_key=failure_cache_key)
        self.max_failures = max_failures

    def should_open_circuit(
        self, total_failures: int, total_requests: int
    ) -> bool:
        return total_failures >= self.max_failures

    def log_increase_failures(
        self, total_failures: int, total_requests: int
    ) -> None:
        logger.info(
            f'Increase failure for: {self.failure_cache_key} - '
            f'max failures {self.max_failures} - '
            f'total requests {total_requests} - '
            f'total failures {total_failures}'
        )
