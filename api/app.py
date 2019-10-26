from concurrent.futures.process import ProcessPoolExecutor
from functools import partial
from pathlib import Path
from typing import Optional, List

import aioredis
from aiohttp import web
from aiohttp.web_middlewares import normalize_path_middleware
from aiohttp_apispec import validation_middleware, setup_aiohttp_apispec

from api.routes import init_routes
from utils.config import init_config_app

path = Path(__file__).parent


async def redis(app: web.Application) -> None:
    """When the server has started, connects to redis,
    and after stopping it breaks the connection (after yield)

    :param app: Web application
    :return: None
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


async def on_start(app: web.Application) -> web.Application:
    """ Save some objects to application for using in future and init
    task collection to manage all tasks and gracefully finish them.

    :param app: Web application
    :return: Web application
    """
    app['tasks'] = []
    app['executor'] = ProcessPoolExecutor()
    return app


async def gracefully_on_stop(app: web.Application) -> web.Application:
    """ Gracefully cancel created tasks and shutdown all created
    on start application.

    :param app: Web application
    :return: Web application
    """
    for task in app['tasks']:
        task.cancel()
        await task

    await app['executor'].shutdown()
    return app


def init_app(config: Optional[List[str]] = None) -> web.Application:
    """ Initializing web application with middlewares, config, routs and etc.

    :param config: Configuration
    :return: Web application
    """
    app = web.Application(
        middlewares=[normalize_path_middleware(), validation_middleware]
    )

    init_config_app(app, config=config)
    init_routes(app)
    app.cleanup_ctx.extend([
        redis,
    ])

    app.on_startup.append(on_start)
    app.on_cleanup.append(gracefully_on_stop)

    setup_aiohttp_apispec(
        app=app,
        title="News project DD-flow",
        version="v1",
        url="/api/docs/swagger.json",
        swagger_path="/api/docs",
    )

    return app


app = init_app()


