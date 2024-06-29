# pylint: disable=unused-argument, unnecessary-pass

"""
Lifespan module
"""

from fastapi import FastAPI

from configs.cache.redis import initialize_redis, cleanup_redis


async def startup(app: FastAPI) -> None:
    """
    This function is called when the FastAPI application starts up.
    It initializes any necessary resources or services.

    Args:
        app (FastAPI): The FastAPI application instance.

    Returns:
        None
    """
    # Initialize any resources or services here
    redis_client, redis_pool = await initialize_redis()
    app.state.redis_client = redis_client
    app.state.redis_pool = redis_pool


async def shutdown(app: FastAPI) -> None:
    """
    An asynchronous function that handles the shutdown of the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.

    Returns:
        None
    """
    # Perform any necessary shutdown operations here
    redis_client = app.state.redis_client
    redis_pool = app.state.redis_pool
    await cleanup_redis(redis_client, redis_pool)


async def lifespan_init(app: FastAPI):
    """
    An asynchronous function that initializes the FastAPI application lifespan.

    Args:
        app (FastAPI): The FastAPI application instance.

    Returns:
        None
    """
    # Call the startup function
    await startup(app)

    # Yield to allow the application to run
    yield

    # Call the shutdown function
    await shutdown(app)
