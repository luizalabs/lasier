# Lasier
A sync/async circuit breaker implementation

[![Build Status](https://travis-ci.org/luizalabs/lasier.svg?branch=master)](https://travis-ci.org/luizalabs/lasier)

According to Nygard on your masterpiece book [Release It!](http://pragprog.com/titles/mnee/release-it):

> [...] circuit breakers protect overeager gadget hounds from burning their houses down. The principle is the same: detect excess usage, fail first, and open the circuit. More abstractly, the circuit breaker exists to allow one subsystem (an electrical circuit) to fail (excessive current draw, possibly from a short circuit) without destroying the entire system (the house). Furthermore, once the danger has passed, the circuit breaker can be reset to restore full function to the system.

## Requirements
* Python >= 3.7

## Instalation
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
You can use the Lasier circuit breaker with a *context\_manager* f.ex:

```python
from lasier.circuit_breaker.sync import CircuitBreaker

...

def some_protected_func():
    with CircuitBreaker(
        rule=rule,
        cache=cache,
        failure_exception=ValueError,
        catch_exceptions=(KeyError, TypeError)
    ):
        # some process
```
Or a _decorator_, f.ex:

```python
from lasier.circuit_breaker.asyncio import circuit_breaker

...

@circuit_breaker(
    rule=rule,
    cache=cache,
    failure_exception=ValueError,
    catch_exceptions=(KeyError, TypeError)
)
async def some_protected_func():
    # some process
```

The **sync** and **async** implementations follow the same interface, so you only need to change the import path:

* `lasier.circuit_breaker.sync`: for sync implementataion
* `lasier.circuit_breaker.asyncio`: for async implementataion

##### Arguments
| Argument | Definition |
|----------|------------|
| rule | Instance of class [rule](https://github.com/luizalabs/lasier#rule). |
| cache | Instance of the circuit breaker [state storage](https://github.com/luizalabs/lasier#circuit-state-storage). |
| failure\_exception | Exception to be raised when it exceeds the maximum number of errors and when the circuit is open. |
| failure\_timeout | This value is set on first error. It is used to validate the number of errors by time. (seconds, default 60) |
| circuit\_timeout | Time that the circuit will be open. (seconds, default 60) |
| catch\_exceptions | List of exceptions catched to increase the number of errors. |

> **WARNING**: The args `failure_timeout` and `circuit_timeout` will be used on state storage commands so if you'll use libs that expects milliseconds instead of seconds on `timeout` arguments maybe you'll get yourself in trouble

## Circuit state storage
Lasier works with a storage to register the current state of the circuit, number of failures, etc. That storage respects the follow interface:

```python
from lasier.types import Timeout  # Timeout = Optional[Union[int, float]]


class Storage:

    def add(self, key: str, value: int, timeout: Timeout = None) -> None:
        pass

    def set(self, key: str, value: int, timeout: Timeout = None) -> None:
        pass

    def incr(self, key: str) -> int:
        pass

    def get(self, key: str) -> int:
        pass

    def expire(key: str, timeout: Timeout = None) -> None:
        pass

    def delete(self, key: str) -> None:
        pass

    def flushdb(self) -> None:
        pass
```

> For `async` circuit breaker, lasier works with that same interface however with async syntax, f.ex: `async def set(self, key=str, value=int, timeout=Optional[int])`

So you can use any cache/storage that respects that interface.

### Adapters
If you'll use Lasier with [redis-py](https://github.com/andymccurdy/redis-py) as cache, you can use `lasier.adapters.caches.redis.RedisAdapter`

```python
from lasier.adapters.caches import RedisAdapter
from redis import Redis

cache = RedisAdapter(Redis(host='localhost', port=6479, db=0))
```

#### Implemented Adapters
| Lib | Adapter |
| --- | --- |
| redis-py | `lasier.adapters.caches.RedisAdapter`|
| django-cache | `lasier.adapters.caches.DjangoAdapter`|
| aiocache | `lasier.adapters.caches.AiocacheAdapter`|
