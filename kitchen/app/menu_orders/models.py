from django.db import models


class MenuOrder(models.Model):

    created_at = models.DateTimeField(auto_now_add=True,
        verbose_name="Créé le")

    identifier = models.UUIDField(blank=False,
        verbose_name="Unique identifier for traceability")

    menu = models.CharField(blank=True, max_length=40,
        verbose_name="Selected menu",
        choices=[
            ('STANDARD', 'Standard menu'),
            ('XXL', 'XXL Menu')
        ]
    )

    preparation_estimated_start = models.DateTimeField(null=True,
        verbose_name="Preparation: estimated start"
    )

    preparation_estimated_end = models.DateTimeField(null=True,
        verbose_name="Preparation: estimated start"
    )

    preparation_start = models.DateTimeField(null=True,
        verbose_name="Preparation: start date/time"
    )
    preparation_end = models.DateTimeField(null=True,
        verbose_name="Preparation: end date/time"
    )

    status = models.CharField(default='NEW', max_length=20,
        verbose_name="Status",
        choices=[
            ('SCHEDULED', 'Scheduled to be cooked'),
            ('IN_PROGRESS', 'Being cooked'),
            ('COOKED', 'Cooked - ready to be picked'),
            ('PICKED', 'Picked by delivery service')
        ]
    )

