# Generated by Django 2.0.3 on 2018-08-08 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0066_auto_20180803_0528"),
        ("site", "0018_sitesettings_homepage_collection"),
    ]

    operations = [migrations.RemoveField(model_name="product", name="is_featured")]
