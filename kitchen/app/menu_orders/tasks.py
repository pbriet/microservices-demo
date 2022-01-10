from celery import shared_task
from menu_orders.models import MenuOrder
from django.utils import timezone
from kitchen.rabbitmq import MessagingConnection

import json
import random
import time

@shared_task
def cook_order(identifier):
    """
    Simulate somebody who would cook and tell that the meal is cooked
    """
    print("[Bob] Starting cooking order %s" % identifier)
    order = MenuOrder.objects.get(identifier=identifier)

    order.preparation_start = timezone.now()
    order.save()

    time.sleep(20 + random.randint(0, 15))

    order.preparation_end = timezone.now()
    order.status = "COOKED"
    order.save()
    print("[Bob] Order %s is now cooked" % identifier)

    with MessagingConnection.start_transaction() as transaction:
        channel = transaction.connection.channel()

        # Send message that menu is cooked
        message = {
            'identifier': str(order.identifier),
            'status': 'cooked'
        }

        channel.basic_publish(
            exchange='kitchen',
            routing_key='cooked',
            body=json.dumps(message)
        )