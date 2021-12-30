from django.db import models
from api.models import Order
import uuid

class OrderSagaTracker(models.Model):
    """
    Saga transaction for a given order
    """
    # Link to the order being treated by the SAGA
    order = models.ForeignKey(Order, models.CASCADE)

    identifier = models.UUIDField(default=uuid.uuid4,
        verbose_name="Unique identifier for traceability")

    status = models.CharField(default='CREATED', max_length=20,
        verbose_name="Status",
        choices=[
            ('PENDING', 'Waiting for validation and processing'),
            ('PAYMENT_OK', 'Payment accepted'),
            ('MENU_SCHEDULED', 'Scheduled to be cooked'),
            ('COOKED', 'Ready to be delivered'),
            ('DELIVERY', 'Delivery in progress'),
            ('DELIVERED', 'Delivered')
        ]
    )
    # TODO
    # status = models.CharField(max_length=50, default='CREATED')
