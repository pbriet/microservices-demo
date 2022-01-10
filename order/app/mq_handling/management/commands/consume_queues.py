#!/usr/bin/env python

# import pika
from django.core.management.base import BaseCommand
from mq_handling.kitchen import handle_cooked_meal
from order.rabbitmq import MessagingTransaction
from saga.new_order import OrderSagaManager

class Command(BaseCommand):
    help = 'Listen to RabbitMQ queues and handle messages'

    def handle(self, *args, **kargs):

        with MessagingTransaction() as transaction:
            channel = transaction.channel

            OrderSagaManager.initialize_queues(transaction)

            channel.exchange_declare('kitchen', "direct", durable=True)
            channel.queue_declare(queue='cooked')
            channel.queue_bind('cooked', 'kitchen', routing_key='cooked')

            OrderSagaManager.consume_reply_queues(transaction)

            transaction.channel.basic_consume(queue='cooked',
                                on_message_callback=handle_cooked_meal)

            print(' [*] Waiting for messages')
            transaction.channel.start_consuming()
