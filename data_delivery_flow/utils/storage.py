import redis

from utils.config import get_config_default


def redis_pool() -> redis.ConnectionPool:
    """

    Returns
    -------

    """
    config = get_config_default()
    redis_pool = redis.ConnectionPool(host=config['redis']['host'],
                                      port=config['redis']['port'],
                                      db=config['redis']['db'],
                                      decode_responses=True)
    return redis_pool


def connection_redis() -> redis.StrictRedis:
    """

    Returns
    -------

    """
    redis_conn = redis.StrictRedis(connection_pool=redis_pool())
    return redis_conn
