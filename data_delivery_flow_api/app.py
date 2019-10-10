from concurrent.futures.process import ProcessPoolExecutor
from functools import partial
from pathlib import Path
from typing import Optional, List

import aioredis
from aiohttp import web
from aiohttp.web_middlewares import normalize_path_middleware
from aiohttp_apispec import validation_middleware, setup_aiohttp_apispec

from data_delivery_flow_api.routes import init_routes
from utils.config import init_config_app

path = Path(__file__).parent


async def redis(app: web.Application) -> None:
    """ A function that, when the server is started, connects to redis,
    and after stopping it breaks the connection (after yield)

    Parameters
    ----------
    app - web application

    Returns
    -------

    """
    config = app['config']['redis']

    create_redis = partial(
        aioredis.create_redis,
        f'redis://{config["host"]}:{config["port"]}'
    )
    app['create_redis'] = await create_redis()

    yield

    app['create_redis'].close()
    await app['create_redis'].wait_closed()


async def init_tasks(app: web.Application) -> web.Application:
    """

    Parameters
    ----------
    app - web application

    Returns
    -------

    """
    app['tasks'] = []
    app['executor'] = ProcessPoolExecutor()
    return app


async def gracefully_stop_tasks(app: web.Application) -> web.Application:
    """

    Parameters
    ----------
    app - web application

    Returns
    -------

    """
    for task in app['tasks']:
        task.cancel()
        await task
    app['executor'].shutdown()
    return app


def init_app(config: Optional[List[str]] = None) -> web.Application:
    """

    Parameters
    ----------
    config

    Returns
    -------

    """
    app = web.Application(
        middlewares=[normalize_path_middleware(), validation_middleware]
    )

    init_config_app(app, config=config)
    init_routes(app)
    app.cleanup_ctx.extend([
        redis,
    ])

    app.on_startup.append(init_tasks)
    app.on_cleanup.append(gracefully_stop_tasks)

    setup_aiohttp_apispec(
        app=app,
        title="News project DD-flow",
        version="v1",
        url="/api/docs/swagger.json",
        swagger_path="/api/docs",
    )

    return app
