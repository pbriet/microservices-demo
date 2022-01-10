
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
        self.channel = self.connection.channel()
        return self

    def __exit__(self, *args, **kargs):
        self.connection.close()

