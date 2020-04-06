# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-19 13:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("account", "0009_auto_20170206_0407")]

    replaces = [("userprofile", "0010_auto_20170919_0839")]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "permissions": (
                    ("view_user", "Can view users"),
                    ("edit_user", "Can edit users"),
                ),
                "verbose_name": "user",
                "verbose_name_plural": "users",
            },
        )
    ]
