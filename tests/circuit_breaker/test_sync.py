from unittest import mock

import pytest

from lasier.circuit_breaker.sync import CircuitBreaker, circuit_breaker

from .exceptions import MyException


def success_function():
    return True


def fail_function():
    raise ValueError()


class TestCircuitBreaker:

    @pytest.fixture
    def failure_cache_key(self):
        return 'fail'

    @pytest.fixture
    def request_cache_key(self):
        return 'request'

    def test_should_exec_func_with_success(self, cache, should_not_open_rule):
        with CircuitBreaker(
            rule=should_not_open_rule,
            cache=cache,
            failure_exception=ValueError,
            catch_exceptions=[]
        ):
            success_function()

    def test_should_exec_func_with_success_ussing_decorator(
        self,
        cache,
        should_not_open_rule
    ):
        @circuit_breaker(
            rule=should_not_open_rule,
            cache=cache,
            failure_exception=ValueError,
            catch_exceptions=[],
        )
        def inner_func():
            success_function()

        inner_func()

    def test_should_raise_error(self, cache, should_open_rule):
        with pytest.raises(MyException):
            with CircuitBreaker(
                rule=should_open_rule,
                cache=cache,
                failure_exception=MyException,
                catch_exceptions=(ValueError,),
            ):
                fail_function()

    def test_should_raise_error_with_decorator(self, cache, should_open_rule):
        @circuit_breaker(
            rule=should_open_rule,
            cache=cache,
            failure_exception=MyException,
            catch_exceptions=(ValueError,),
        )
        def inner_func():
            fail_function()

        with pytest.raises(MyException):
            inner_func()

    def test_should_increase_fail_cache_count(
        self,
        cache,
        failure_cache_key,
        should_not_open_rule
    ):
        cache.set(failure_cache_key, 1)

        with pytest.raises(ValueError):
            with CircuitBreaker(
                rule=should_not_open_rule,
                cache=cache,
                failure_exception=MyException,
                catch_exceptions=(ValueError,),
            ):
                fail_function()

        assert cache.get(failure_cache_key) == 2

    def test_should_increase_request_cache_count(
        self,
        cache,
        request_cache_key,
        should_not_open_rule
    ):
        cache.set(request_cache_key, 0)

        with CircuitBreaker(
            rule=should_not_open_rule,
            cache=cache,
            failure_exception=MyException,
            catch_exceptions=(ValueError,),
        ):
            success_function()

        with pytest.raises(ValueError):
            with CircuitBreaker(
                rule=should_not_open_rule,
                cache=cache,
                failure_exception=MyException,
                catch_exceptions=(ValueError,),
            ):
                fail_function()

        assert cache.get(request_cache_key) == 2

    def test_should_open_circuit_when_failures_exceeds(
        self,
        cache,
        should_open_rule,
        failure_cache_key,
    ):
        cache.set(failure_cache_key, 3)

        with pytest.raises(MyException):
            with CircuitBreaker(
                rule=should_open_rule,
                cache=cache,
                failure_exception=MyException,
                catch_exceptions=(ValueError,),
            ) as cb:
                fail_function()

        assert cb.is_circuit_open()

    def test_should_raise_exception_when_circuit_is_open(
        self,
        cache,
        should_open_rule,
        failure_cache_key
    ):
        circuit_cache_key = f'circuit_{failure_cache_key}'
        cache.set(circuit_cache_key, 1)

        with pytest.raises(MyException):
            with CircuitBreaker(
                rule=should_open_rule,
                cache=cache,
                failure_exception=MyException,
                catch_exceptions=(ValueError,),
            ) as cb:
                success_function()
                assert cb.is_circuit_open()

    def test_should_not_call_exit_when_circuit_is_open(
        self,
        cache,
        should_open_rule,
        failure_cache_key
    ):
        circuit_cache_key = f'circuit_{failure_cache_key}'
        cache.set(circuit_cache_key, 1)

        with pytest.raises(MyException):
            with mock.patch(
                'lasier.circuit_breaker.sync.CircuitBreaker.__exit__'
            ) as exit_method:
                with CircuitBreaker(
                    rule=should_open_rule,
                    cache=cache,
                    failure_exception=MyException,
                    catch_exceptions=(ValueError,),
                ):
                    success_function()

        assert not exit_method.called

    def test_should_not_increment_fail_when_circuit_is_open(
        self,
        cache,
        should_open_rule,
        failure_cache_key
    ):
        """
        It should not increment fail count over the max failures limit, when
        circuit breaker is open after a successful enter.
        """
        cache.set(failure_cache_key, 3)

        with pytest.raises(MyException):
            with CircuitBreaker(
                rule=should_open_rule,
                cache=cache,
                failure_exception=MyException,
                catch_exceptions=(ValueError,),
            ):
                fail_function()

        assert cache.get(failure_cache_key) is None

    def test_should_not_increment_request_when_circuit_is_open(
        self,
        cache,
        should_open_rule,
        failure_cache_key,
        request_cache_key
    ):
        """
        It should not increment request count over the max failures limit, when
        circuit breaker is open after a successful enter.
        """
        cache.set(failure_cache_key, 2)
        cache.set(request_cache_key, 5)

        with pytest.raises(MyException):
            with CircuitBreaker(
                rule=should_open_rule,
                cache=cache,
                failure_exception=MyException,
                catch_exceptions=(ValueError,),
            ):
                fail_function()

        assert cache.get(request_cache_key) is None

    def test_should_not_increment_request_when_rule_is_false(
        self,
        cache,
        should_not_increase_request_rule,
        request_cache_key
    ):
        cache.set(request_cache_key, 5)

        with pytest.raises(ValueError):
            with CircuitBreaker(
                rule=should_not_increase_request_rule,
                cache=cache,
                failure_exception=MyException,
                catch_exceptions=(ValueError,),
            ):
                fail_function()

        assert cache.get(request_cache_key) == 5

    def test_should_not_increment_failure_when_rule_is_false(
        self,
        cache,
        should_not_increase_failure_rule,
        failure_cache_key
    ):
        cache.set(failure_cache_key, 5)

        with pytest.raises(ValueError):
            with CircuitBreaker(
                rule=should_not_increase_failure_rule,
                cache=cache,
                failure_exception=MyException,
                catch_exceptions=(ValueError,),
            ):
                fail_function()

        assert cache.get(failure_cache_key) == 5

    def test_should_delete_count_key_when_circuit_is_open(
        self,
        cache,
        should_open_rule,
        failure_cache_key,
        request_cache_key
    ):
        cache.set(failure_cache_key, 2)
        cache.set(request_cache_key, 5)

        with pytest.raises(MyException):
            with CircuitBreaker(
                rule=should_open_rule,
                cache=cache,
                failure_exception=MyException,
                catch_exceptions=(ValueError,),
            ) as cb:
                fail_function()

            assert cb.is_circuit_open

        assert cache.get(failure_cache_key) is None
        assert cache.get(request_cache_key) is None

    def test_should_create_failure_cache_when_increase_request_count(
        self,
        cache,
        should_not_open_rule,
        failure_cache_key,
        request_cache_key,
    ):
        assert cache.get(failure_cache_key) is None

        with CircuitBreaker(
            rule=should_not_open_rule,
            cache=cache,
            failure_exception=MyException,
            catch_exceptions=(ValueError,),
        ):
            success_function()

        assert cache.get(failure_cache_key) == 0
