import logging

from .base import RuleBase

logger = logging.getLogger(__name__)


class MaxFailuresRule(RuleBase):

    def __init__(self, max_failures, failure_cache_key):
        super().__init__(failure_cache_key=failure_cache_key)
        self.max_failures = max_failures

    def should_open_circuit(self, total_failures, total_requests):
        return total_failures >= self.max_failures

    def log_increase_failures(self, total_failures, total_requests):
        logger.info(
            f'Increase failure for: {self.failures_cache_key} - '
            f'max failures {self.max_failures} - '
            f'total requests {total_requests} - '
            f'total failures {total_failures}'
        )
