import pathlib

from aiohttp import web

from api.data_delivery_flow_api.handlers import get_start_urls_by_spider, \
    post_start_urls_by_spider, delete_start_urls_by_spider, start_parsing

PROJECT_PATH = pathlib.Path(__file__).parent


def init_routes(app: web.Application) -> None:
    add_route = app.router.add_route

    add_route('GET', '/api/v1/start-urls', get_start_urls_by_spider, name='get_start_urls')
    add_route('POST', '/api/v1/start-urls', post_start_urls_by_spider, name='set_start_urls')
    add_route('DELETE', '/api/v1/start-urls', delete_start_urls_by_spider, name='remove_start_urls')

    add_route('POST', '/api/v1/parse', start_parsing, name='start_parsing_process')

