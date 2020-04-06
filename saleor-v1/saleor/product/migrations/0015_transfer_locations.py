# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-07 14:41
from __future__ import unicode_literals

from django.db import migrations


def forward_transfer_locations(apps, schema_editor):
    Stock = apps.get_model("product", "Stock")
    StockLocation = apps.get_model("product", "StockLocation")
    for stock in Stock.objects.all():
        location = StockLocation.objects.get_or_create(name=stock.location)[0]
        stock.location_link = location
        stock.save()


def reverse_transfer_locations(apps, schema_editor):
    Stock = apps.get_model("product", "Stock")
    for stock in Stock.objects.all():
        if stock.location_link:
            location = stock.location_link.name
            stock.location = location
            stock.save()


class Migration(migrations.Migration):

    dependencies = [("product", "0014_auto_20161207_0840")]

    operations = [
        migrations.RunPython(forward_transfer_locations, reverse_transfer_locations)
    ]
