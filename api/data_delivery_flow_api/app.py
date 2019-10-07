from functools import partial
from pathlib import Path
from typing import Optional, List

import aioredis
from aiohttp import web
from aiohttp.web_middlewares import normalize_path_middleware
from aiohttp_apispec import validation_middleware, setup_aiohttp_apispec

from api.data_delivery_flow_api.routes import init_routes
from api.data_delivery_flow_api.utils.common import init_config

path = Path(__file__).parent


async def redis(app: web.Application) -> None:
    '''
    A function that, when the server is started, connects to redis,
    and after stopping it breaks the connection (after yield)
    '''
    config = app['config']['redis']

    create_redis = partial(
        aioredis.create_redis,
        f'redis://{config["host"]}:{config["port"]}'
    )
    app['create_redis'] = await create_redis()

    yield

    app['create_redis'].close()
    await app['create_redis'].wait_closed()


def init_app(config: Optional[List[str]] = None) -> web.Application:
    app = web.Application(
        middlewares=[normalize_path_middleware(), validation_middleware]
    )

    init_config(app, config=config)
    init_routes(app)

    app.cleanup_ctx.extend([
        redis,
    ])

    setup_aiohttp_apispec(
        app=app,
        title="My Documentation",
        version="v1",
        url="/api/docs/swagger.json",
        swagger_path="/api/docs",
    )

    return app
