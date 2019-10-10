# -*- coding: utf-8 -*-
import logging
import pika

from pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet.threads import deferToThread

from utils.config import get_config_default

logging.getLogger("pika").setLevel(logging.INFO)


class MessageQueuePipeline(object):

    def __init__(self, host, port, queue):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.queue = queue
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    @classmethod
    def from_settings(cls, settings):
        """

        Parameters
        ----------
        settings

        Returns
        -------

        """
        config = get_config_default()
        host = config['rabbitmq']['host']
        port = config['rabbitmq']['port']
        queue = config['rabbitmq']['queue']
        return cls(host=host, port=port, queue=queue)

    def spider_opened(self, spider):
        """

        Parameters
        ----------
        spider

        Returns
        -------

        """
        self.publisher = self.connection.channel()
        self.publisher.queue_declare(queue=self.queue)

    def spider_closed(self, spider):
        """

        Parameters
        ----------
        spider

        Returns
        -------

        """
        self.publisher.close()

    def process_item(self, item, spider):
        """

        Parameters
        ----------
        item
        spider

        Returns
        -------

        """
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        """

        Parameters
        ----------
        item
        spider

        Returns
        -------

        """
        self.publisher.basic_publish(exchange='',
                                     routing_key=self.queue,
                                     body=ScrapyJSONEncoder().encode(dict(item)))
        return item
