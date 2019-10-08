import redis


def redis_pool():
    redis_pool = redis.ConnectionPool(host='redis', port=6379, db=0, decode_responses=True)
    return redis_pool


def connection_redis():
    redis_conn = redis.StrictRedis(connection_pool=redis_pool())
    return redis_conn
