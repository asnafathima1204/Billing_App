# Generated by Django 5.2 on 2025-05-30 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CUSTOMER', '0002_alter_customer_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='wallet',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
