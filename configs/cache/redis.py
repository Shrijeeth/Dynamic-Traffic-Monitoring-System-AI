"""
Redis Module for cache
"""

from redis.asyncio import ConnectionPool, Redis
from configs.config import get_settings


async def initialize_redis() -> tuple[Redis, ConnectionPool]:
    """
    Initialize Redis connection

    Returns:
        client: Redis Asynchronous client
        pool: Redis connection pool
    """
    host = get_settings().REDIS_HOST
    port = get_settings().REDIS_PORT
    username = get_settings().REDIS_USERNAME
    password = get_settings().REDIS_PASSWORD
    db = get_settings().REDIS_DB

    pool = ConnectionPool(
        host=host,
        port=port,
        username=username,
        password=password,
        db=db,
        encoding="utf-8",
        decode_responses=True,
        max_connections=10,
    )
    client = await Redis.from_pool(connection_pool=pool)

    return client, pool


async def cleanup_redis(client: Redis, pool: ConnectionPool) -> None:
    """
    Close Redis connections

    Args:
        client: Redis Asynchronous client
        pool: Redis connection pool

    Returns:
        None
    """
    if client is not None:
        await client.close()

    if pool is not None:
        await pool.disconnect()
        await pool.aclose()


async def set_cache(client: Redis, key: str, value: str) -> None:
    """
    Set cache data in Redis

    Args:
        client: Redis Asynchronous client
        key: Cache key
        value: Cache value
    """
    async with client.pipeline(transaction=True) as pipe:
        await pipe.set(key, value)
        await pipe.execute()


async def get_cache(client: Redis, key: str) -> str:
    """
    Get cache data from Redis

    Args:
        client: Redis Asynchronous client
        key: Cache key

    Returns:
        data: Cache value
    """
    async with client.pipeline(transaction=True) as pipe:
        await pipe.get(key)
        data = await pipe.execute()
    return data[0]
