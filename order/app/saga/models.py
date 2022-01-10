from django.db import models
from api.models import Order
import uuid

class OrderSagaTracker(models.Model):
    """
    Saga transaction for a given order
    """
    created_at = models.DateTimeField(auto_now_add=True,
        verbose_name="Créé le")
    # Link to the order being treated by the SAGA
    order = models.ForeignKey(Order, models.CASCADE)

    identifier = models.UUIDField(default=uuid.uuid4,
        verbose_name="Unique identifier for traceability")

    status = models.CharField(default='CREATED', max_length=20,
        verbose_name="Status",
        choices=[
            ('PENDING', 'Waiting for validation and processing'),
            ('PAYMENT_OK', 'Payment accepted'),
            ('PAYMENT_CANCELLED', 'Payment cancelled'),
            ('PAYMENT_FAILED', 'Payment failed'),
            ('KITCHEN_SCHEDULED', 'Scheduled to be cooked'),
            ('KITCHEN_CANCELLED', 'Cancelling cooking'),
            ('KITCHEN_FAILED', 'Kitchen failure'),
            ('DELIVERY_SCHEDULED', 'Scheduled to be deliveed'),
            ('DELIVERY_CANCELLED', 'Cancelling delivery'),
            ('DELIVERY_FAILED', 'Delivery failure')
        ]
    )
    # TODO
    # status = models.CharField(max_length=50, default='CREATED')
