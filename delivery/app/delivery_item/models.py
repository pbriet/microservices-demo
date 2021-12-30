from django.db import models

import uuid

class DeliveryItem(models.Model):
    """
    Delivery process of one menu
    """

    identifier = models.UUIDField(default=uuid.uuid4,
        verbose_name="Unique identifier for traceability")

    status = models.CharField(default='NEW', max_length=20,
        verbose_name="Status",
        choices=[
            ('SCHEDULED', 'Scheduled'),
            ('STARTED', 'Delivery in progress'),
            ('DELIVERED', 'Successfully delivered'),
            ('FAILED', 'Could\'n t deliver'),
        ]
    )

    departure_time = models.DateTimeField(
        blank=False,
        verbose_name="Estimated or real time of departure"
    )

    arrival_time = models.DateTimeField(
        blank=False,
        verbose_name="Estimated or real time of arrival"
    )


