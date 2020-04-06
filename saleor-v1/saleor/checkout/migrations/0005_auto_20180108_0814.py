# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-08 14:14
from __future__ import unicode_literals

import uuid

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.contrib.postgres import fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("checkout", "0004_auto_20171129_1004")]

    replaces = [("cart", "0005_auto_20180108_0814")]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="checkout_data",
            field=fields.JSONField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name="cart",
            name="created",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="cart",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name="cart",
            name="last_status_change",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="cart",
            name="quantity",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="cart",
            name="status",
            field=models.CharField(
                choices=[
                    ("open", "Open - currently active"),
                    ("payment", "Waiting for payment"),
                    ("saved", "Saved - for items to be purchased later"),
                    ("ordered", "Submitted - an order was placed"),
                    ("checkout", "Checkout - processed in checkout"),
                    ("canceled", "Canceled - canceled by user"),
                ],
                default="open",
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name="cart",
            name="token",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="cart",
            name="total",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name="cart",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="carts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="cart",
            name="voucher",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="discount.Voucher",
            ),
        ),
        migrations.AlterField(
            model_name="cartline",
            name="cart",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="lines",
                to="checkout.Cart",
            ),
        ),
        migrations.AlterField(
            model_name="cartline",
            name="data",
            field=fields.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name="cartline",
            name="quantity",
            field=models.PositiveIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(999),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="cartline",
            name="variant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="product.ProductVariant",
            ),
        ),
    ]
