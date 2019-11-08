import inspect
import logging

logger = logging.getLogger(__name__)


class CircuitBreakerBase:

    def __init__(
        self,
        rule,
        cache,
        failure_exception,
        failure_timeout=None,
        circuit_timeout=None,
        catch_exceptions=None,
    ):
        self.rule = rule
        self.cache = cache
        self.failure_timeout = failure_timeout
        self.circuit_timeout = circuit_timeout
        self.circuit_cache_key = 'circuit_{}'.format(rule.failure_cache_key)
        self.failure_exception = failure_exception
        self.catch_exceptions = catch_exceptions or (Exception,)

    def _is_catchable_exception(self, exception):
        return inspect.isclass(exception) and any(
            issubclass(exception, exception_class)
            for exception_class in self.catch_exceptions
        )

    def _notify_open_circuit(self):
        logger.critical(
            f'Open circuit for {self.rule.failure_cache_key} '
            f'{self.circuit_cache_key}'
        )

    def _notify_max_failures_exceeded(self):
        logger.info(f'Max failures exceeded by: {self.rule.failure_cache_key}')
