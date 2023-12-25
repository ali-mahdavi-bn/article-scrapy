from abc import ABC, abstractmethod
from typing import Optional

from backbone.infrastructure.redis.connection import RedisConnection


class AbstractStore(ABC):
    @abstractmethod
    def get_value(self, key):
        raise NotImplementedError

    @abstractmethod
    def set_value(self, key, value, exp: Optional[int] = None):
        raise NotImplementedError

    @abstractmethod
    def delete_key(self, key):
        raise NotImplementedError


class RedisStore(AbstractStore):
    def get_value(self, key):
        return RedisConnection.get_value(key=key)

    def set_value(self, key, value, exp: Optional[int] = None):
        RedisConnection.set_value(key=key, value=value, exp=exp)

    def delete_key(self, key):
        RedisConnection.delete_key(key=key)
