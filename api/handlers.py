import asyncio

import ujson
from aiohttp import web
from aiohttp_apispec import request_schema, docs

from api.schemas import StartUrlSchema, SpiderSchema
from data_delivery_flow.utils.start_crawl import start_parse_process


@docs(tags=['start-urls'],
      summary='Get all spiders name, which have start-urls in storage',
      description='Get all spiders name, which have start-urls in storage.',
      responses={
          200: {"description": '{"objects": ["http://example.com/post_1"]}'},
          404: {"description": "Not found"},
          422: {"description": "Validation error"},
      }
      )
async def get_start_urls_by_spider(request: web.Request) -> web.Response:
    """ Get all spider names which have urls in Redis.

    :param request: web request
    :return: web response in json format
    """
    redis = request.app['create_redis']
    response_data = await redis.keys('*')
    return web.json_response({"objects": response_data}, dumps=ujson.dumps)


@docs(tags=['start-urls'],
      summary='Set start-urls to storage by spider name',
      description='Set start-urls to storage by spider name.',
      responses={
          404: {"description": "Not found"},
          422: {"description": "Validation error"},
      }
      )
@request_schema(StartUrlSchema)
async def post_start_urls_by_spider(request: web.Request) -> web.Response:
    """ Add start urls by spider name to Redis.

    :param request: web request
    :return: web response without body with 201 response status
    """
    redis = request.app['create_redis']
    data = await request.json()
    await redis.sadd(data['name'], *data['start_urls'])
    return web.HTTPCreated(text="")


@docs(tags=['start-urls'],
      summary='Remove start-urls from storage',
      description='Remove start-urls from storage.',
      responses={
          404: {"description": "Not found"},
          422: {"description": "Validation error"},
      }
      )
@request_schema(SpiderSchema)
async def delete_start_urls_by_spider(request: web.Request) -> web.Response:
    """ Remove start urls from Redis by spider name.

    :param request: web request
    :return: web response without body with 204 response status
    """
    redis = request.app['create_redis']
    data = await request.json()
    await redis.delete(data['name'])
    return web.HTTPNoContent()


@docs(tags=['parse'],
      summary='Start parse process',
      description='Start parse process.',
      responses={
          200: {"description": '{"status": "started"} or failed (invalid spider name)'},
          404: {"description": "Not found"},
          422: {"description": "Validation error"},
      }
      )
@request_schema(SpiderSchema)
async def start_parsing(request: web.Request) -> web.Response:
    """ Start crawl process by spider name.

    :param request: web request
    :return: web response in json format
    """
    redis = request.app['create_redis']
    data = await request.json()
    spider_name = data['name']
    if await redis.exists(spider_name):
        try:
            executor = request.app['executor']
            task = asyncio.create_task(start_parse_process(executor, spider_name))
            request.app['tasks'].append(task)
        except Exception as e:
            print(e)
        return web.json_response({"status": 'started'}, dumps=ujson.dumps)
    else:
        return web.json_response({"status": 'failed (invalid spider name)'}, dumps=ujson.dumps)


@docs(tags=['tasks'],
      summary='Get count of all tasks',
      description='Get count of all tasks.',
      responses={
          200: {"description": '{"count": 5}'},
          404: {"description": "Not found"},
          422: {"description": "Validation error"},
      }
      )
async def get_all_running_tasks_count(request: web.Request) -> web.Response:
    """ Get all active tasks in queue.

    :param request: web request
    :return: web response in json format
    """
    all_tasks_count = len(asyncio.Task.all_tasks())
    return web.json_response({'count': all_tasks_count})
