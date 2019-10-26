# -*- coding: utf-8 -*-
import logging

from pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.serialize import ScrapyJSONEncoder

from data_delivery_flow.utils.brocker import RabbitMQConnection
from utils.config import get_config_default

logging.getLogger("pika").setLevel(logging.WARNING)
logger = logging.getLogger("MessageQueuePipeline")


class MessageQueuePipeline(object):

    def __init__(self, config):
        self.config = config['rabbitmq']
        self.queue = self.config['queue']
        self.exchange_name = self.config['exchange_name']
        self.exchange_type = self.config['exchange_type']
        self.routing_key = self.config['routing_key']
        self.host = self.config['host']
        self.port = self.config['port']
        self.rbmq_conn = RabbitMQConnection.get_connection(host=self.host,
                                                           port=self.port)
        self.publisher = self.rbmq_conn.get_channel(exchange_name=self.exchange_name,
                                                    exchange_type=self.exchange_type,
                                                    queue=self.queue)
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    @classmethod
    def from_settings(cls, settings):
        """ Setup config to MessageQueuePipeline object.

        :param settings:
        :return:
        """
        config = get_config_default()
        return cls(config=config)

    def spider_opened(self, spider):
        """ Action after spider open process.

        :param spider:
        :return:
        """
        logger.info(f'Spider {spider.name} is opening and has next config: q: {self.queue}, '
                    f'ex.n: {self.exchange_name}, ex.t: {self.exchange_type}, rk: {self.routing_key}')

    def spider_closed(self, spider):
        """ Action after spider close process.

        :param spider:
        :return:
        """
        logger.info(f'Rabbitmq connection closed')
        self.rbmq_conn.connection.close()

    def process_item(self, item, spider):
        """ Handle items. Send items to RabbitMQ.

        :param item:
        :param spider:
        :return:
        """
        self.rbmq_conn.send_message(channel=self.publisher,
                                    message=ScrapyJSONEncoder().encode(dict(item)),
                                    exchange_name=self.exchange_name,
                                    routing_key=self.routing_key)
        logger.debug(f'Item scraped')
        return item
