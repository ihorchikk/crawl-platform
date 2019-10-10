import scrapy

from data_delivery_flow.utils.storage import connection_redis


class BaseSpider(scrapy.Spider):
    def __init__(self):

        redis_connection = connection_redis()
        count_urls = redis_connection.scard(self.name)
        start_urls = redis_connection.spop(self.name,count=count_urls)
        super(BaseSpider, self).__init__(start_urls=start_urls)


