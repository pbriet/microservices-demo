from django.db import models
import uuid

class Order(models.Model):

    created_at = models.DateTimeField(auto_now_add=True,
        verbose_name="Créé le")

    identifier = models.UUIDField(default=uuid.uuid4,
        verbose_name="Unique identifier for traceability")

    status = models.CharField(default='NEW', max_length=20,
        verbose_name="Status",
        choices=[
            ('PENDING', 'Waiting for validation and processing'),
            ('VALIDATED', 'Validated'),
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