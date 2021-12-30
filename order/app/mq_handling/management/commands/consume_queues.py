#!/usr/bin/env python

# import pika
from django.core.management.base import BaseCommand
from saga.new_order import OrderSagaManager

# from order.rabbitmq import MessagingConnection
# from saga.new_order import NewOrderSaga

# from api.models import Order

# def handle_payment_ok(ch, method, props, body):
#     """
#     Received message : payment is ok
#     """

#     NewOrderSaga.on_payment_validated(
#         props.correlation_id,
#         body
#     )
#     ch.basic_ack(delivery_tag = method.delivery_tag)


# def handle_scheduled_menus(ch, method, props, body):
#     """
#     Received message : menu preparation is scheduled
#     """
#     NewOrderSaga.on_menu_scheduled(
#         props.correlation_id,
#         body
#     )

#     ch.basic_ack(delivery_tag = method.delivery_tag)


# def handle_scheduled_deliveries(ch, method, props, body):
#     """
#     Received message : delivery is scheduled
#     """
#     NewOrderSaga.on_delivery_scheduled(
#         props.correlation_id,
#         body
#     )

#     ch.basic_ack(delivery_tag = method.delivery_tag)


class Command(BaseCommand):
    help = 'Listen to RabbitMQ queues and handle messages'

    def handle(self, *args, **kargs):

        OrderSagaManager.initialize_queues()
        OrderSagaManager.consume_reply_queues()

        # with MessagingConnection.start_transaction() as transaction:
        #     channel = transaction.connection.channel()

        #     channel.basic_consume(queue='processed_payment',
        #                         on_message_callback=handle_payment_ok)

        #     channel.basic_consume(queue='processed_menu',
        #                         on_message_callback=handle_scheduled_menus)

        #     channel.basic_consume(queue='processed_delivery',
        #                         on_message_callback=handle_scheduled_deliveries)


        #     print(' [*] Waiting for messages')
        #     channel.start_consuming()