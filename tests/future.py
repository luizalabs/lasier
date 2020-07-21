import asyncio

SENTINEL = object()


def new_future(result=SENTINEL, exception=SENTINEL):
    future = asyncio.Future()
    if result is not SENTINEL:
        future.set_result(result)
    elif exception is not SENTINEL:
        future.set_exception(exception)
    return future
