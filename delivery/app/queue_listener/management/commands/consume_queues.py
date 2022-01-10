#!/usr/bin/env python

import pika
from django.core.management.base import BaseCommand
from django.utils import timezone
from delivery.rabbitmq import MessagingConnection

from delivery_item.models import DeliveryItem

import datetime
import time
import json

import logging

# Reduce pika log level
logging.getLogger("pika").setLevel(logging.WARNING)

def handle_incoming_delivery(ch, method, props, body):
    """
    New menu to deliver
    """
    print("DELIVERY : handle_incoming_delivery")
    time.sleep(5)
    try:
        order_identifier = props.correlation_id
        deliveries = list(DeliveryItem.objects.filter(identifier=str(order_identifier)))

        if len(deliveries) > 0:
            # It is probably a duplicated message
            # We should be idempotent
            return

        data = json.loads(body)
        departure_time = datetime.datetime.fromisoformat(data['cooked_at'])

        # Plan the delivery.
        order = DeliveryItem.objects.create(
            identifier=order_identifier,
            status='SCHEDULED',
            departure_time=departure_time,
            arrival_time=departure_time + datetime.timedelta(seconds=150)
        )


        # Send message that delivery is scheduled
        message = {
            'status': 'ok',
            'estimated_delivery': order.arrival_time.isoformat()
        }

        print("DELIVERY : will be delivered at %s" % order.arrival_time.isoformat())

        ch.basic_publish(
            exchange='order_saga',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(
                correlation_id=str(order.identifier)
            ),
            body=json.dumps(message)
        )
    finally:
        ch.basic_ack(delivery_tag = method.delivery_tag)

    print("Queued scheduled_deliveries")



class Command(BaseCommand):
    help = 'Listen to RabbitMQ queues and handle messages'

    def handle(self, *args, **kargs):

        with MessagingConnection.start_transaction() as transaction:
            channel = transaction.connection.channel()

            channel.basic_consume(queue='incoming_delivery',
                                on_message_callback=handle_incoming_delivery)

            print(' [*] Waiting for messages')
            channel.start_consuming()

