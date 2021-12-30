
from sagapy.saga import SagaManager
from saga.step_payment import PaymentStep
from saga.step_kitchen import KitchenStep
from saga.step_delivery import DeliveryStep
from saga.models import OrderSagaTracker

# from django.utils import timezone
# from api.models import Order
# from order.rabbitmq import MessagingConnection
# import json
# import pika


class OrderSagaManager(SagaManager):

    STEPS = [
        PaymentStep(),
        KitchenStep(),
        DeliveryStep()
    ]

    SAGA_MODEL = OrderSagaTracker

    EXCHANGE_NAME = "order_saga"


####################################

# class NewOrderSaga(object):
#     """
#     Saga orchestrator for a new order

#     1. Check that payment is valid (payment microservice)
#     2. Tell the kitchen to prepare the meal
#     3. Schedule delivery
#     """

#     @classmethod
#     def on_create(cls, order, request):
#         """
#         New order
#         Ask payment micro-service to validate credit card and charge it
#         """
#         print("NewOrderSaga::on_create")

#         message = {
#             'payment_card_details': {
#                 'number': request.POST['payment_card_number'],
#                 'cvc': request.POST['payment_cvc']
#             }
#         }

#         with MessagingConnection.start_transaction() as messaging_transaction:
#             channel = messaging_transaction.connection.channel()
#             channel.basic_publish(
#                 exchange='order_saga',
#                 routing_key='incoming_payment',
#                 properties=pika.BasicProperties(
#                     reply_to='processed_payment',
#                     correlation_id=str(order.identifier)
#                 ),
#                 body=json.dumps(message)
#             )

#         print("Queue 'payment_validate'")


#     @classmethod
#     def on_payment_validated(cls, order_identifier, body):
#         """
#         Payment card was charged
#         Ask the kitchen to prepare the meal and estimate time
#         """

#         print("NewOrderSaga::on_payment_validated")

#         # TODO : payment not valid

#         try:
#             order = Order.objects.get(identifier=str(order_identifier))
#         except Order.DoesNotExist:
#             # It is probably a duplicated message
#             # We should be idempotent
#             return

#         order.status = 'PAYMENT_OK'
#         order.save()

#         message = {
#             'menu': order.menu
#         }

#         with MessagingConnection.start_transaction() as messaging_transaction:
#             channel = messaging_transaction.connection.channel()
#             channel.basic_publish(
#                 exchange='order_saga',
#                 routing_key='incoming_menu',
#                 properties=pika.BasicProperties(
#                     reply_to='processed_menu',
#                     correlation_id=str(order.identifier)
#                 ),
#                 body=json.dumps(message)
#             )

#         print("Queue 'incoming_menus'")


#     @classmethod
#     def on_menu_scheduled(cls, order_identifier, body):
#         """
#         Restaurant planned execution of menu.
#         Now tell the delivery service.
#         """
#         data = json.loads(body)

#         print("NewOrderSaga::on_menu_scheduled")

#         # TODO : unable to cook

#         try:
#             order = Order.objects.get(identifier=str(order_identifier))
#         except Order.DoesNotExist:
#             # It is probably a duplicated message
#             # We should be idempotent
#             return

#         message = {
#             'cooked_at': data['estimated_cooked_time']
#         }

#         with MessagingConnection.start_transaction() as messaging_transaction:
#             channel = messaging_transaction.connection.channel()
#             channel.basic_publish(
#                 exchange='order_saga',
#                 routing_key='incoming_delivery',
#                 properties=pika.BasicProperties(
#                     reply_to='processed_delivery',
#                     correlation_id=str(order.identifier)
#                 ),
#                 body=json.dumps(message)
#             )

#         print("Queue 'incoming_delivery'")


#     @classmethod
#     def on_delivery_scheduled(cls, order_identifier, body):
#         """
#         Delivery is scheduled. We're all good.
#         """
#         data = json.loads(body)

#         print("NewOrderSaga::on_delivery_scheduled")

#         # TODO : unable to deliver

#         print("Delivery is scheduled. Everything seems ok. End of SAGA")

#         print("Send SMS to customer : << Estimated delivery : %s >>" % data['estimated_delivery'])
