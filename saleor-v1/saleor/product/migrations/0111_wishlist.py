# Generated by Django 2.2.9 on 2020-04-04 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0110_auto_20191108_0340'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=120)),
            ],
        ),
    ]
