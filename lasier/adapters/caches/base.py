
class CacheAdapterBase:

    def __init__(self, cache):
        self.cache = cache

    def add(self, key, value, timeout):
        return self.cache.add(key, value, timeout)

    def set(self, key, value, timeout):
        return self.cache.set(key, value, timeout)

    def incr(self, key):
        return self.cache.incr(key)

    def get(self, key):
        return self.cache.get(key)

    def delete(self, key):
        return self.cache.delete(key)

    def flushdb(self):
        return self.cache.flushdb()
