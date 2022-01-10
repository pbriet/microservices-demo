#!/usr/bin/env python

# import pika
from django.core.management.base import BaseCommand
from delivery.rabbitmq import MessagingTransaction

class Command(BaseCommand):
    help = 'Check rabbit MQ connectivity'

    def handle(self, *args, **kargs):

        with MessagingTransaction() as transaction:
            print("Rabbit MQ connection is ok")
