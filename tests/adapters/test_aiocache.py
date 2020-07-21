from unittest.mock import MagicMock

import pytest

from lasier.adapters.caches.aiocache import Adapter

from ..future import new_future


@pytest.mark.asyncio
class TestAioCacheAdapter:

    @pytest.fixture
    def mocked_cache(self):
        return MagicMock()

    @pytest.fixture
    def adapter(self, mocked_cache):
        return Adapter(mocked_cache)

    async def test_should_increment_value(self, adapter, mocked_cache):
        mocked_cache.increment.return_value = new_future(result=-1)
        assert await adapter.incr('some-key') == 1

    async def test_should_suppress_add_value_error_exception(
        self, adapter, mocked_cache
    ):
        mocked_cache.add.return_value = new_future(exception=ValueError)
        try:
            await adapter.add('some-key', 0)
        except Exception as e:
            pytest.fail(f'Its should not raise: {e}')
