import logging

from .base import BaseRule

logger = logging.getLogger(__name__)


class PercentageFailuresRule(BaseRule):

    def __init__(
        self,
        max_failures_percentage: int,
        failure_cache_key: str,
        min_accepted_requests: int,
        request_cache_key: str,
    ) -> None:
        super().__init__(
            failure_cache_key=failure_cache_key,
            request_cache_key=request_cache_key,
        )
        self.max_failures_percentage = max_failures_percentage
        self.min_accepted_requests = min_accepted_requests

    def _get_percentage_failures(
        self, total_failures: int, total_requests: int
    ) -> float:
        if total_requests > 0:
            return (total_failures * 100) / total_requests
        return 0

    def should_open_circuit(
        self, total_failures: int, total_requests: int
    ) -> bool:
        percentage_failures = self._get_percentage_failures(
            total_failures=total_failures,
            total_requests=total_requests
        )
        return (
            total_requests > self.min_accepted_requests and
            percentage_failures >= self.max_failures_percentage
        )

    def log_increase_failures(
        self, total_failures: int, total_requests: int
    ) -> None:
        percentage_failures = self._get_percentage_failures(
            total_failures=total_failures,
            total_requests=total_requests
        )
        logger.info(
            f'Increase failure for: {self.failure_cache_key} - '
            f'max failures {self.max_failures_percentage}% - '
            f'total failures {total_failures} - '
            f'min accepted requests {self.min_accepted_requests} - '
            f'total requests {total_requests} - '
            f'percentage failures {percentage_failures}%'
        )
