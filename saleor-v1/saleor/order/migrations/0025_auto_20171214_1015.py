# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-14 16:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("order", "0024_remove_order_status")]

    operations = [
        migrations.AlterField(
            model_name="deliverygroup",
            name="status",
            field=models.CharField(
                choices=[
                    ("new", "Processing"),
                    ("cancelled", "Cancelled"),
                    ("shipped", "Shipped"),
                ],
                default="new",
                max_length=32,
                verbose_name="shipment status",
            ),
        ),
        migrations.AlterField(
            model_name="orderhistoryentry",
            name="status",
            field=models.CharField(
                choices=[
                    ("new", "Processing"),
                    ("cancelled", "Cancelled"),
                    ("shipped", "Shipped"),
                ],
                max_length=32,
                verbose_name="order status",
            ),
        ),
    ]
