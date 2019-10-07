# -*- coding: utf-8 -*-
import logging

import pika
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet.threads import deferToThread

logging.getLogger("pika").setLevel(logging.INFO)


class MessageQueuePipeline(object):

    def __init__(self, host_name):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host_name))
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    @classmethod
    def from_settings(cls, settings):
        host_name = settings.get('BROKER_HOST')
        return cls(host_name)

    def spider_opened(self, spider):
        self.publisher = self.connection.channel()
        self.publisher.queue_declare(queue='dd-items')

    def spider_closed(self, spider):
        self.publisher.close()

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        self.publisher.basic_publish(exchange='',
                                     routing_key='dd-item',
                                     body=ScrapyJSONEncoder().encode(dict(item)))
        return item
