# Generated by Django 3.1.6 on 2021-10-11 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0003_auto'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderSagaTracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', 'Waiting for validation and processing'), ('PAYMENT_OK', 'Payment accepted'), ('MENU_SCHEDULED', 'Scheduled to be cooked'), ('COOKED', 'Ready to be delivered'), ('DELIVERY', 'Delivery in progress'), ('DELIVERED', 'Delivered')], default='CREATED', max_length=20, verbose_name='Status')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.order')),
            ],
        ),
    ]
