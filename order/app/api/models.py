from django.db import models
import uuid

class Order(models.Model):

    identifier = models.UUIDField(default=uuid.uuid4,
        verbose_name="Unique identifier for traceability")

    status = models.CharField(default='NEW', max_length=20,
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
            ('DELIVERY_FAILED', 'Delivery failure'),


            ('BEING_COOKED', 'Kitchen working on it'),
            ('COOKED', 'Ready to be delivered'),
            ('DELIVERY', 'Delivery in progress'),
            ('DELIVERED', 'Delivered')
        ]
    )

    menu = models.CharField(blank=True, max_length=40,
        verbose_name="Selected menu",
        choices=[
            ('STANDARD', 'Standard menu'),
            ('XXL', 'XXL Menu')
        ]
    )

    payment_card_number = models.CharField(max_length=40, blank=False)
    payment_cvc = models.CharField(max_length=10, blank=False)

    # delivery_start = models.DateTimeField(null=True,
    #     verbose_name="Delivery: start date/time"
    # )
    # delivery_end = models.DateTimeField(null=True,
    #     verbose_name="Delivery: end date/time"
    # )


    def serialize(self):
        """
        Serialize an order into a dictionnary
        """
        return {
            "identifier": self.identifier,
            "status": self.status
        }