#!/usr/bin/env python

import os
import json
import pika
import time

import logging

# Reduce pika log level
logging.getLogger("pika").setLevel(logging.WARNING)

RABBITMQ_CONNECTION_STRING = os.environ.get('RABBITMQ_CONNECTION_STRING')

print("Connecting to... ", RABBITMQ_CONNECTION_STRING)

retries = 0
while True:
    try:
        # Initializing connection to RabbitMQ
        connection = pika.BlockingConnection(
            pika.URLParameters(
                RABBITMQ_CONNECTION_STRING
            )
        )
    except pika.exceptions.AMQPConnectionError:
        retries += 1
        if retries > 5:
            print("Aborting - did not succeed to connect")
            exit(1)
        time.sleep(5)
        print("Failed to connect... retrying")
    else:
        break


channel = connection.channel()
channel.exchange_declare("order_saga", "direct", durable=True)
channel.queue_declare('incoming_payment')
channel.queue_bind('incoming_payment', 'order_saga', routing_key='incoming_payment')

# Make sure that no worker receive a new message
# While still working on one
channel.basic_qos(prefetch_count=1)

def handle_payment_validation(ch, method, props, body):
    """
    Received a new order
    """
    try:
        print("PAYMENT : Validating payment: %s" % body)

        time.sleep(5)

        print("PAYMENT : Payment succeeded")

        response = {"status": "ok"}

        # Replying to the channel that was asked
        ch.basic_publish(exchange='order_saga',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = \
                                                            props.correlation_id),
                        body=json.dumps(response))

    finally:
        ch.basic_ack(delivery_tag = method.delivery_tag)


channel.basic_consume(queue='incoming_payment',
                      on_message_callback=handle_payment_validation)


print(' [*] Waiting for messages')
channel.start_consuming()