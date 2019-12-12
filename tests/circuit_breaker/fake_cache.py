from fakeredis import FakeStrictRedis

from lasier.adapters.caches.redis import RedisAdapter


class FakeAsyncCache:

    def __init__(self):
        self.fake = RedisAdapter(FakeStrictRedis())

    async def add(self, key, value, timeout=None):
        return self.fake.add(key, value, timeout)

    async def set(self, key, value, timeout=None):
        return self.fake.set(key, value, timeout)

    async def incr(self, key):
        return self.fake.incr(key)

    async def get(self, key):
        return self.fake.get(key)

    async def flushdb(self):
        return self.fake.flushdb()

    async def delete(self, key):
        return self.fake.delete(key)
