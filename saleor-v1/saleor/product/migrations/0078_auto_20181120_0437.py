# Generated by Django 2.1.3 on 2018-11-20 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("product", "0077_generate_versatile_background_images")]

    operations = [
        migrations.AddField(
            model_name="collection",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="collectiontranslation",
            name="description",
            field=models.TextField(blank=True),
        ),
    ]
