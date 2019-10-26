import logging
from typing import Any

import pika

logging.getLogger("pika").setLevel(logging.WARNING)
logger = logging.getLogger("RabbitMQConnection")


class RabbitMQConnection(object):

    def __init__(self, connection):
        self.connection = connection

    @classmethod
    def get_connection(cls, host: str, port: int):
        """ Create connection to RabbitMQ and return them.

        :param host: RabbitMQ host
        :param port: RabbitMQ port
        :return: RabbitMQConnection
        """
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=port))
        logger.info(f'Got connection to RabbitMQ')
        return cls(connection=connection)

    def get_channel(self, exchange_name: str, exchange_type: str,
                    queue: str, binding_key: str = None) -> pika.BlockingConnection.channel:
        """ Setup channel, queue and queue bind if need.

        :param exchange_name: exchange name
        :param exchange_type: exchange type (fanout, direct, topic, headers)
        :param queue: queue name
        :param binding_key: binding key between queue and exchange
        :return: channel
        """

        channel = self.connection.channel()
        channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)
        channel.queue_declare(queue=queue)
        if exchange_type == 'topic' and binding_key:
            channel.queue_bind(exchange='topic_logs', queue=queue, routing_key=binding_key)
        logger.info(f'Got channel <exchange_name:{exchange_name},exchange_type:{exchange_type},'
                    f'queue:{queue}, binding_key:{binding_key}>')
        return channel

    @staticmethod
    def send_message(channel: pika.BlockingConnection.channel,
                     message: Any, exchange_name: str, routing_key: str) -> None:
        """ Send message to RabbitMQ.

        :param channel: channel name
        :param message: message
        :param exchange_name: exchange name
        :param routing_key: routing key
        :return: None
        """
        logger.debug(f'Sent message:{message} to exchange_name:{exchange_name} with routing_key:{routing_key}')
        channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message)
