# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-07 14:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("product", "0015_transfer_locations")]

    operations = [
        migrations.AlterUniqueTogether(
            name="stock", unique_together=set([("variant", "location_link")])
        )
    ]
