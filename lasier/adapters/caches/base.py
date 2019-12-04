
class CacheAdapterBase:

    def __init__(self, cache):
        self.cache = cache

    def add(self, key, value, timeout=None):
        return self.cache.add(key, value, timeout)

    def set(self, key, value, timeout=None):
        return self.cache.set(key, value, timeout)

    def incr(self, key):
        return self.cache.incr(key)

    def get(self, key):
        value = self.cache.get(key)
        if value is not None:
            return int(value)
        return None

    def delete(self, key):
        return self.cache.delete(key)

    def flushdb(self):
        return self.cache.flushdb()
