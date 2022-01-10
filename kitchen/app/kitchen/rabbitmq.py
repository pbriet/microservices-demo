
# RabbitMQ connectivity
import pika
from django.conf import settings

import logging

# Reduce pika log level
logging.getLogger("pika").setLevel(logging.WARNING)

class MessagingTransaction(object):
    """
    Transaction to RabbitMQ :
    - Starting with a connection
    - Ending by closing the connection
    """

    def __enter__(self):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(
                settings.RABBITMQ_CONNECTION_STRING
            )
        )
        return self

    def __exit__(self, *args, **kargs):
        self.connection.close()


class MessagingConnection(object):

    INITIALIZED = False

    @classmethod
    def on_server_start(cls):
        """
        Initialization of queues/exchanges at startup
        """
        if not settings.RABBITMQ_CONNECTION_STRING:
            print("No RabbitMQ connection configured. Disabling")
            return
        with cls.start_transaction() as transaction:
            channel = transaction.connection.channel()
            channel.queue_declare(queue='incoming_menu')
            channel.queue_declare(queue='processed_menu')


    @classmethod
    def start_transaction(cls):
        if not cls.INITIALIZED:
            cls.INITIALIZED = True
            cls.on_server_start()
        return MessagingTransaction()


