# Generated by Django 3.1.6 on 2022-01-10 08:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 1, 10, 8, 40, 36, 561486, tzinfo=utc), verbose_name='Créé le'),
            preserve_default=False,
        ),
    ]