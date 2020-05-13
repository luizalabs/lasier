import asyncio
from unittest import mock

import pytest

from lasier.circuit_breaker.asyncio import CircuitBreaker, circuit_breaker

from .exceptions import MyException


async def success_function():
    return True


async def fail_function():
    raise ValueError()


@pytest.mark.asyncio
class TestCircuitBreaker:

    @pytest.fixture
    def failure_cache_key(self):
        return 'fail'

    @pytest.fixture
    def request_cache_key(self):
        return 'request'

    async def test_should_exec_func_with_success(
        self,
        async_cache,
        should_not_open_rule
    ):
        async with CircuitBreaker(
            rule=should_not_open_rule,
            cache=async_cache,
            failure_exception=ValueError,
            catch_exceptions=[]
        ):
            await success_function()

    async def test_should_exec_func_with_success_ussing_decorator(
        self,
        async_cache,
        should_not_open_rule
    ):
        @circuit_breaker(
            rule=should_not_open_rule,
            cache=async_cache,
            failure_exception=ValueError,
            catch_exceptions=[],
        )
        async def inner_func():
            await success_function()

        await inner_func()

    async def test_should_raise_error(self, async_cache, should_open_rule):
        with pytest.raises(MyException):
            async with CircuitBreaker(
                rule=should_open_rule,
                cache=async_cache,
                failure_exception=MyException,
                catch_exceptions=(ValueError,),
            ):
                await fail_function()

    async def test_should_raise_error_with_decorator(
        self,
        async_cache,
        should_open_rule
    ):
        @circuit_breaker(
            rule=should_open_rule,
            cache=async_cache,
            failure_exception=MyException,
            catch_exceptions=(ValueError,),
        )
        async def inner_func():
            await fail_function()

        with pytest.raises(MyException):
            await inner_func()

    async def test_should_increase_fail_cache_count(
        self,
        async_cache,
        failure_cache_key,
        should_not_open_rule
    ):
        await async_cache.set(failure_cache_key, 1)

        with pytest.raises(ValueError):
            async with CircuitBreaker(
                rule=should_not_open_rule,
                cache=async_cache,
                failure_exception=MyException,
                catch_exceptions=(ValueError,),
            ):
                await fail_function()

        assert await async_cache.get(failure_cache_key) == 2

    async def test_should_increase_request_cache_count(
        self,
        async_cache,
        request_cache_key,
        should_not_open_rule
    ):
        await async_cache.set(request_cache_key, 0)

        async with CircuitBreaker(
            rule=should_not_open_rule,
            cache=async_cache,
            failure_exception=MyException,
            catch_exceptions=(ValueError,),
        ):
            await success_function()

        with pytest.raises(ValueError):
            async with CircuitBreaker(
                rule=should_not_open_rule,
                cache=async_cache,
                failure_exception=MyException,
                catch_exceptions=(ValueError,),
            ):
                await fail_function()

        assert await async_cache.get(request_cache_key) == 2

    async def test_should_open_circuit_when_failures_exceeds(
        self,
        async_cache,
        should_open_rule,
        failure_cache_key,
    ):
        await async_cache.set(failure_cache_key, 3)

        with pytest.raises(MyException):
            async with CircuitBreaker(
                rule=should_open_rule,
                cache=async_cache,
                failure_exception=MyException,
                catch_exceptions=(ValueError,),
            ) as cb:
                await fail_function()

        assert await cb.is_circuit_open()

    async def test_should_raise_exception_when_circuit_is_open(
        self,
        async_cache,
        should_open_rule,
        failure_cache_key
    ):
        circuit_cache_key = f'circuit_{failure_cache_key}'
        await async_cache.set(circuit_cache_key, 1)

        with pytest.raises(MyException):
            async with CircuitBreaker(
                rule=should_open_rule,
                cache=async_cache,
                failure_exception=MyException,
                catch_exceptions=(ValueError,),
            ) as cb:
                await success_function()
                assert await cb.is_circuit_open()

    async def test_should_not_call_exit_when_circuit_is_open(
        self,
        async_cache,
        should_open_rule,
        failure_cache_key
    ):
        circuit_cache_key = f'circuit_{failure_cache_key}'
        await async_cache.set(circuit_cache_key, 1)

        with pytest.raises(MyException):
            with mock.patch(
                'lasier.circuit_breaker.asyncio.CircuitBreaker.__aexit__'
            ) as exit_method:
                async with CircuitBreaker(
                    rule=should_open_rule,
                    cache=async_cache,
                    failure_exception=MyException,
                    catch_exceptions=(ValueError,),
                ):
                    await success_function()

        assert not exit_method.called

    async def test_should_not_increment_fail_when_circuit_is_open(
        self,
        async_cache,
        should_open_rule,
        failure_cache_key
    ):
        """
        It should not increment fail count over the max failures limit, when
        circuit breaker is open after a successful enter.
        """
        await async_cache.set(failure_cache_key, 3)

        with pytest.raises(MyException):
            async with CircuitBreaker(
                rule=should_open_rule,
                cache=async_cache,
                failure_exception=MyException,
                catch_exceptions=(ValueError,),
            ):
                await fail_function()

        assert (await async_cache.get(failure_cache_key)) is None

    async def test_should_not_increment_request_when_circuit_is_open(
        self,
        async_cache,
        should_open_rule,
        failure_cache_key,
        request_cache_key
    ):
        """
        It should not increment request count over the max failures limit, when
        circuit breaker is open after a successful enter.
        """
        await asyncio.gather(
            async_cache.set(failure_cache_key, 2),
            async_cache.set(request_cache_key, 5)
        )

        with pytest.raises(MyException):
            async with CircuitBreaker(
                rule=should_open_rule,
                cache=async_cache,
                failure_exception=MyException,
                catch_exceptions=(ValueError,),
            ):
                await fail_function()

        assert (await async_cache.get(request_cache_key)) is None

    async def test_should_not_increment_request_when_rule_is_false(
        self,
        async_cache,
        should_not_increase_request_rule,
        request_cache_key
    ):
        await async_cache.set(request_cache_key, 5)

        with pytest.raises(ValueError):
            async with CircuitBreaker(
                rule=should_not_increase_request_rule,
                cache=async_cache,
                failure_exception=MyException,
                catch_exceptions=(ValueError,),
            ):
                await fail_function()

        assert await async_cache.get(request_cache_key) == 5

    async def test_should_not_increment_failure_when_rule_is_false(
        self,
        async_cache,
        should_not_increase_failure_rule,
        failure_cache_key
    ):
        await async_cache.set(failure_cache_key, 5)

        with pytest.raises(ValueError):
            async with CircuitBreaker(
                rule=should_not_increase_failure_rule,
                cache=async_cache,
                failure_exception=MyException,
                catch_exceptions=(ValueError,),
            ):
                await fail_function()

        assert await async_cache.get(failure_cache_key) == 5

    async def test_should_delete_count_key_when_circuit_is_open(
        self,
        async_cache,
        should_open_rule,
        failure_cache_key,
        request_cache_key
    ):
        await asyncio.gather(
            async_cache.set(failure_cache_key, 2),
            async_cache.set(request_cache_key, 5)
        )

        with pytest.raises(MyException):
            async with CircuitBreaker(
                rule=should_open_rule,
                cache=async_cache,
                failure_exception=MyException,
                catch_exceptions=(ValueError,),
            ) as cb:
                await fail_function()

            assert await cb.is_circuit_open()

        assert await async_cache.get(failure_cache_key) is None
        assert await async_cache.get(request_cache_key) is None

    async def test_should_create_failure_cache_when_increase_request_count(
        self,
        async_cache,
        should_not_open_rule,
        failure_cache_key,
        request_cache_key,
    ):
        assert await async_cache.get(failure_cache_key) is None

        async with CircuitBreaker(
            rule=should_not_open_rule,
            cache=async_cache,
            failure_exception=MyException,
            catch_exceptions=(ValueError,),
        ):
            await success_function()

        assert await async_cache.get(failure_cache_key) == 0

    async def test_should_call_expire_if_incr_returns_one(
        self,
        async_cache,
        should_not_open_rule
    ):
        future = asyncio.Future()
        future.set_result(None)

        with mock.patch.object(
            async_cache, 'expire', return_value=future, autospec=True
        ) as mock_expire:
            for _ in range(5):
                with pytest.raises(ValueError):
                    async with CircuitBreaker(
                        rule=should_not_open_rule,
                        cache=async_cache,
                        failure_exception=MyException,
                        catch_exceptions=(ValueError,),
                    ):
                        await fail_function()

        # for request and fail count
        assert mock_expire.call_count == 2
