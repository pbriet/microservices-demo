# Generated by Django 3.1.6 on 2022-01-10 08:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('saga', '0002_ordersagatracker_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordersagatracker',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Créé le'),
            preserve_default=False,
        ),
    ]