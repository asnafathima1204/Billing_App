# Generated by Django 5.2 on 2025-06-13 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CUSTOMER', '0005_alter_customer_credit_limit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='credit_limit',
        ),
    ]
