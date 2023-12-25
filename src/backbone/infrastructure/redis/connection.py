from typing import Optional

from redis import BlockingConnectionPool, StrictRedis

from backbone.configs import config


class RedisConnection:
    _connection: Optional[StrictRedis] = None
    pool = BlockingConnectionPool(
        max_connections=30,
        timeout=200,
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        password=config.REDIS_PASSWORD,
        username=config.REDIS_USER,
    )

    @classmethod
    def get_connection(cls):
        if not cls._connection:
            cls._connection = StrictRedis(connection_pool=cls.pool)
        return cls._connection

    @classmethod
    def get_value(cls, key):
        cls.get_connection()
        return cls._connection.get(key)

    @classmethod
    def exists_key(cls, key):
        cls.get_connection()
        return True if cls._connection.exists(key) == 1 else False

    @classmethod
    def set_value(cls, key, value, exp: Optional[int] = None):
        cls.get_connection()
        cls._connection.set(key, value)
        if exp:
            cls._connection.expire(key, time=exp)

    @classmethod
    def delete_key(cls, key):
        cls.get_connection()
        cls._connection.delete(key)

    @classmethod
    def get_keys_with_prefix(cls, prefix: str):
        cls.get_connection()
        return [item.decode("utf-8") for item in cls._connection.keys(prefix + "*")]

    @classmethod
    def push_values(cls, key, values: list, exp: Optional[int] = None):
        cls.get_connection()
        cls._connection.lpush(key, *values)
        if exp:
            cls._connection.expire(key, time=exp)

    @classmethod
    def get_all_list_values(cls, key: str):
        cls.get_connection()
        values_list = cls._connection.lrange(key, 0, -1)
        values_list = [item.decode("utf-8") for item in values_list]
        return values_list
