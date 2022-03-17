import pytest
from aiocache import Cache
from fakeredis import FakeStrictRedis

from lasier.adapters.caches import AiocacheAdapter, RedisAdapter

from .fake_rules import (
    ShouldNotIncreaseFailureRule,
    ShouldNotIncreaseRequestRule,
    ShouldNotOpenRule,
    ShouldOpenRule,
)


@pytest.fixture
def cache():
    fake_cache = RedisAdapter(FakeStrictRedis())
    yield fake_cache
    fake_cache.flushdb()


@pytest.fixture
async def async_cache():
    fake_cache = AiocacheAdapter(Cache(Cache.MEMORY))
    yield fake_cache
    await fake_cache.flushdb()


@pytest.fixture
def should_not_open_rule(failure_cache_key, request_cache_key):
    return ShouldNotOpenRule(
        failure_cache_key=failure_cache_key,
        request_cache_key=request_cache_key
    )


@pytest.fixture
def should_open_rule(failure_cache_key, request_cache_key):
    return ShouldOpenRule(
        failure_cache_key=failure_cache_key,
        request_cache_key=request_cache_key
    )


@pytest.fixture
def should_not_open_rule_without_request_cache_key(failure_cache_key):
    return ShouldNotOpenRule(
        failure_cache_key=failure_cache_key,
    )


@pytest.fixture
def should_not_increase_request_rule(failure_cache_key, request_cache_key):
    return ShouldNotIncreaseRequestRule(
        failure_cache_key=failure_cache_key,
        request_cache_key=request_cache_key
    )


@pytest.fixture
def should_not_increase_failure_rule(failure_cache_key, request_cache_key):
    return ShouldNotIncreaseFailureRule(
        failure_cache_key=failure_cache_key,
        request_cache_key=request_cache_key
    )
