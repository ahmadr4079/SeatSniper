import redis

from seas.app.helpers.singleton import Singleton
from seas.project.config import seas_config


class RedisBaseAdapter(metaclass=Singleton):

    def __init__(self):
        self.client = redis.Redis(
            **{
                "host": seas_config.redis_dsn.host,
                "port": seas_config.redis_dsn.port,
                "db": seas_config.redis_dsn.path.split("/")[1],
                "decode_responses": True,
            }
        )
