# Lasier
A sync/async circuit breaker implementation

According to Nygard on your masterpiece book [Release It!](http://pragprog.com/titles/mnee/release-it):

> [...] circuit breakers protect overeager gadget hounds from burning their houses down. The principle is the same: detect excess usage, fail first, and open the circuit. More abstractly, the circuit breaker exists to allow one subsystem (an electrical circuit) to fail (excessive current draw, possibly from a short circuit) without destroying the entire system (the house). Furthermore, once the danger has passed, the circuit breaker can be reset to restore full function to the system.

## Requirements
* Python >= 3.7

## Instalation (WIP)
Using `pip`:

```
pip install lasier
```

## Usage
TODO

## Circuit state storage
Lasier works with a storage to register the current state of the circuit, number of failures, etc. That storage respects the follow interface:

```python
class Storage:

    def add(self, key=str, value=int, timeout=Optional[int]):
        pass

    def set(self, key=str, value=int, timeout=Optional[int]):
        pass

    def incr(self, key=str):
        pass

    def get(self, key=str) -> int:
        pass

    def delete(self, key=str):
        pass

    def flushdb(self):
        pass
```

> For `async` circuit breaker, lasier works with that same interface however with async syntax, f.ex: `async def set(self, key=str, value=int, timeout=Optional[int])`

So you can use any cache/storage that respects that interface, f.ex the [django caches object](https://docs.djangoproject.com/en/3.0/topics/cache/)

### Adapters
If you'll use Lasier with [redis-py] as cache, you can use `lasier.adapters.caches.redis.RedisAdapter`

```python
from lasier.adapters.cache.redis import RedisAdapter
from redis import Redis

cache = RedisAdapter(Redis(host='localhost', port=6479, db=0))
```
