import inspect
import logging
from typing import Any, Iterable, Optional, Type, Union

from .rules.base import BaseRule

logger = logging.getLogger(__name__)
_ONE_MINUTE = 60


class CircuitBreakerBase:
    def __init__(
        self,
        rule: BaseRule,
        cache: Any,
        failure_exception: Type[Exception],
        failure_timeout: Optional[Union[int, float]] = _ONE_MINUTE,
        circuit_timeout: Optional[Union[int, float]] = _ONE_MINUTE,
        catch_exceptions: Optional[Iterable[Type[Exception]]] = None,
    ) -> None:
        self.rule = rule
        self.cache = cache
        self.failure_timeout = failure_timeout
        self.circuit_timeout = circuit_timeout
        self.circuit_cache_key = 'circuit_{}'.format(rule.failure_cache_key)
        self.failure_exception = failure_exception
        self.catch_exceptions = catch_exceptions or (Exception,)

    def _is_catchable_exception(self, exception: Type[Exception]) -> bool:
        return inspect.isclass(exception) and any(
            issubclass(exception, exception_class)
            for exception_class in self.catch_exceptions
        )

    def _notify_open_circuit(self) -> None:
        logger.critical(
            f'Open circuit for {self.rule.failure_cache_key} '
            f'{self.circuit_cache_key}'
        )

    def _notify_max_failures_exceeded(self) -> None:
        logger.info(f'Max failures exceeded by: {self.rule.failure_cache_key}')
