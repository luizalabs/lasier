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
To use lasier circuit breaker you'll need a `rule` and a `cache` (the circuit state storage) instance

### Rule
A `Rule` is the mechanism that define where circuit will open or close.

#### MaxFailuresRule
Rule to open circuit based on maximum number of failures

```python
from lasier.circuit_breaker.rules import MaxFailuresRule

rule = MaxFailuresRule(
    max_failures=500,
    failure_cache_key='my_cb'
)
```

##### Arguments
| Argument | Definition |
|----------|------------|
| max\_failures | Maximum number of errors |
| failure\_cache\_key | Cache key where the number of errors is incremented |

#### PercentageFailuresRule
Rule to open circuit based on a percentage of failures

```python
from lasier.circuit_breaker.rules import PercentageFailuresRule

rule = PercentageFailuresRule(
    max_failures_percentage=60,
    failure_cache_key='my_cb',
    min_accepted_requests=100,
    request_cache_key='my_cb_request'
)
```

##### Arguments
| Argument | Definition |
|----------|------------|
| max\_failures\_percentage | Maximum percentage of errors |
| failure\_cache\_key | Cache key where the number of errors is incremented |
| min\_accepted\_requests | Minimum number of requests accepted to not open circuit breaker |
| request\_cache\_key | Cache key where the number of requests is incremented |

### Circuit Breaker
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
