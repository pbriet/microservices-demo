
# RabbitMQ connectivity
import pika
from django.conf import settings


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
            
            channel.exchange_declare("order_saga", "direct",
                durable=True)

            for queue_name in (
                "incoming_payment",
                "processed_payment",
                "incoming_menu",
                "processed_menu",
                "incoming_delivery",
                "processed_delivery"
                ):
                channel.queue_declare(
                    queue_name
                )
                channel.queue_bind(queue_name, "order_saga",
                    routing_key=queue_name)

    @classmethod
    def start_transaction(cls):
        if not cls.INITIALIZED:
            cls.INITIALIZED = True
            cls.on_server_start()
        return MessagingTransaction()

