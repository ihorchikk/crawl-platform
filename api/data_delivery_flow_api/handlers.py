import ujson
from aiohttp import web
from aiohttp_apispec import request_schema, docs

from api.data_delivery_flow_api.schemas import StartUrlSchema, SpiderSchema
from data_delivery_flow.utils.start_crawl import start_parse_process


@docs(tags=['my_tag'],
      summary='Test method summary',
      description='Test method description',
      parameters=[{
              'in': 'header',
              'name': 'X-Request-ID',
              'schema': {'type': 'string', 'format': 'uuid'},
              'required': 'true'
          }]
      )
async def get_start_urls_by_spider(request: web.Request) -> web.Response:
    redis = request.app['create_redis']
    response_data = await redis.keys('start-request:*')
    return web.json_response({"objects": response_data}, dumps=ujson.dumps)


@request_schema(StartUrlSchema)
async def post_start_urls_by_spider(request: web.Request) -> web.Response:
    redis = request.app['create_redis']
    data = await request.json()
    await redis.sadd(data['name'], *data['start_urls'])
    return web.HTTPCreated(text="")


@request_schema(SpiderSchema)
async def delete_start_urls_by_spider(request: web.Request) -> web.Response:
    redis = request.app['create_redis']
    data = await request.json()
    await redis.delete(data['name'])
    return web.HTTPNoContent()


@request_schema(SpiderSchema)
async def start_parsing(request: web.Request) -> web.Response:
    redis = request.app['create_redis']
    data = await request.json()
    spider_name = data['name']
    if await redis.exists(spider_name):
        await start_parse_process(spider_name, request.loop)
        return web.json_response({"status": 'started'}, dumps=ujson.dumps)
    else:
        return web.json_response({"status": 'failed (invalid spider name)'}, dumps=ujson.dumps)



