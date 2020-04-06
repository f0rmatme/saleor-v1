# Generated by Django 2.0.2 on 2018-02-27 10:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("order", "0041_auto_20180222_0458")]

    operations = [
        migrations.AlterField(
            model_name="fulfillment",
            name="fulfillment_order",
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name="orderline",
            name="order",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="lines",
                to="order.Order",
            ),
        ),
        migrations.RemoveField(model_name="deliverygroup", name="order"),
        migrations.RemoveField(model_name="orderline", name="delivery_group"),
        migrations.DeleteModel(name="DeliveryGroup"),
    ]
