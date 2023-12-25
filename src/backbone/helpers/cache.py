import functools
from collections import OrderedDict
from sys import getsizeof
import time

import dill
import hermes.backend.redis

from backbone.configs import config


hermes_cache = hermes.Hermes(
    backend=hermes.backend.redis.Backend,
    ttl=100 * 600,
    host=config.REDIS_HOST  ,
    db=1,
    port=config.REDIS_PORT,
    username=config.REDIS_USER,
    password=config.REDIS_PASSWORD,
)


def cache_with_custom_serialization(ttl=None):
    def decorator_cache(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create a unique key based on the function's name and arguments
            key = (func.__name__, args, frozenset(kwargs.items()))
            serialized_key = dill.dumps(key)

            # Try to retrieve the cached value
            cached_value = hermes_cache.get(serialized_key)
            if cached_value is not None:
                return cached_value

            # If not cached, call the function and cache its result
            result = func(*args, **kwargs)
            hermes_cache.set(serialized_key, result, ttl=ttl)
            return result
        return wrapper
    return decorator_cache


class SizedMemoryCache:
    def __init__(self, max_size):
        self.cache = hermes.Hermes(backend=hermes.backend.memory.Backend, ttl=600)
        self.max_size = max_size
        self.current_size = 0

    def set(self, key, value):
        # Evict items if the max size is exceeded
        if self.current_size >= self.max_size:
            self.evict_items()
        self.cache.set(key, value)
        self.current_size += 1  # Adjust this logic based on how you measure size

    def get(self, key):
        return self.cache.get(key)

    def evict_items(self):
        # Implement your eviction logic here
        # This is just a placeholder
        pass


def cache_in_mem(expiry_time=3 * 60, max_size=10000 * 1024 * 1024):
    def decorator(func):
        cache = OrderedDict()
        current_size = 0

        def make_key(args, kwargs):
            return *args, frozenset(kwargs.items())

        def wrapper(*args, **kwargs):
            nonlocal current_size
            key = make_key(args, kwargs)

            if key in cache:
                value, timestamp = cache.pop(key)
                cache[key] = (value, timestamp)  # Move to end (most recently used)
                if time.time() - timestamp < expiry_time:
                    return value

            while max_size and current_size > max_size:
                _, (val, _) = cache.popitem(last=False)
                current_size -= getsizeof(val)

            result = func(*args, **kwargs)
            cache[key] = (result, time.time())
            current_size += getsizeof(result)
            return result

        return wrapper
    return decorator
