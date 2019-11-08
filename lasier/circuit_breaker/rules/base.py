import abc
import logging

logger = logging.getLogger(__name__)


class RuleBase(metaclass=abc.ABCMeta):

    def __init__(self, failure_cache_key, request_cache_key=None):
        self.failure_cache_key = failure_cache_key
        self.request_cache_key = request_cache_key

    @abc.abstractmethod
    def should_open_circuit(self, total_failures, total_requests):
        pass

    def should_increase_failure_count(self):
        return self.failure_cache_key is not None

    def should_increase_request_count(self):
        return self.request_cache_key is not None

    @abc.abstractmethod
    def log_increase_failures(self, total_failures, total_requests):
        pass
