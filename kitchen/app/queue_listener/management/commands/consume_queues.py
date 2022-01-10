#!/usr/bin/env python

import pika
from django.core.management.base import BaseCommand
from django.utils import timezone
from kitchen.rabbitmq import MessagingConnection

from menu_orders.models import MenuOrder
from menu_orders.tasks import cook_order

import datetime
import json
import time
import random

import logging

# Reduce pika log level
logging.getLogger("pika").setLevel(logging.WARNING)


def handle_incoming_menu(ch, method, props, body):
    """
    New menu to prepare, incoming
    """
    try:
        order_identifier = props.correlation_id
        print("KITCHEN : handle_incoming_menu ", order_identifier)
        time.sleep(5)
        menu_orders = list(MenuOrder.objects.filter(identifier=str(order_identifier)))

        if len(menu_orders) > 0:
            # It is probably a duplicated message
            # We should be idempotent
            print("KITCHEN : duplicated message")
            return

        data = json.loads(body)

        # Plan the preparation. Estimate time
        order = MenuOrder.objects.create(
            identifier=order_identifier,
            menu=data['menu'],
            status='SCHEDULED',
            preparation_estimated_start=timezone.now() + datetime.timedelta(seconds=30),
            preparation_estimated_end=timezone.now() + datetime.timedelta(seconds=150)
        )

        print("KITCHEN : planning Mock cook")
        # Celery task to execute mock cooking
        cook_order.apply_async(
            (order_identifier,),
            eta=order.preparation_estimated_start + datetime.timedelta(seconds=random.randint(-5, 5)))

        # Send message that menu is scheduled
        message = {
            'status': 'ok',
            'estimated_cooked_time': order.preparation_estimated_end.isoformat()
        }

        print("KITCHEN : menu will be cooked at ", order.preparation_estimated_end.isoformat())

        # Replying to the channel that was asked
        ch.basic_publish(
            exchange='order_saga',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(
                correlation_id=props.correlation_id
            ),
            body=json.dumps(message)
        )
    finally:

        ch.basic_ack(delivery_tag = method.delivery_tag)



class Command(BaseCommand):
    help = 'Listen to RabbitMQ queues and handle messages'

    def handle(self, *args, **kargs):

        with MessagingConnection.start_transaction() as transaction:
            channel = transaction.connection.channel()

            channel.basic_consume(queue='incoming_menu',
                                on_message_callback=handle_incoming_menu)

            print(' [*] Waiting for messages')
            channel.start_consuming()