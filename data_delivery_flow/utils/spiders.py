import logging

import scrapy

from data_delivery_flow.utils.storage import connection_redis

logger = logging.getLogger("BaseSpider")


class BaseSpider(scrapy.Spider):
    def __init__(self):

        redis_connection = connection_redis()
        count_urls = redis_connection.scard(self.name)
        start_urls = redis_connection.spop(self.name, count=count_urls)

        logger.info(f'Collect {count_urls} urls from Redis by name={self.name}')
        super(BaseSpider, self).__init__(start_urls=start_urls)


