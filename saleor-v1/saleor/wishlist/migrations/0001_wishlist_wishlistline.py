# Generated by Django 2.2.9 on 2020-04-05 04:58

from django.conf import settings
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import saleor.core.utils.json_serializer
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shipping', '0017_django_price_2'),
        ('account', '0037_delete_wishlist'),
        ('product', '0112_delete_wishlist'),
        ('giftcard', '0002_auto_20190814_0413'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wishlist', 'fix_empty_data_in_lines'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('private_meta', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=saleor.core.utils.json_serializer.CustomJsonEncoder, null=True)),
                ('meta', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=saleor.core.utils.json_serializer.CustomJsonEncoder, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_change', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=254)),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('note', models.TextField(blank=True, default='')),
                ('currency', models.CharField(default='USD', max_length=3)),
                ('discount_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('discount_name', models.CharField(blank=True, max_length=255, null=True)),
                ('translated_discount_name', models.CharField(blank=True, max_length=255, null=True)),
                ('voucher_code', models.CharField(blank=True, max_length=12, null=True)),
                ('billing_address', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='account.Address')),
                ('gift_cards', models.ManyToManyField(blank=True, related_name='wishlists', to='giftcard.GiftCard')),
                ('shipping_address', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='account.Address')),
                ('shipping_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wishlists', to='shipping.ShippingMethod')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wishlists', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-last_change',),
            },
        ),
        migrations.CreateModel(
            name='WishlistLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='product.ProductVariant')),
                ('wishlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='wishlist.Wishlist')),
            ],
            options={
                'ordering': ('id',),
                'unique_together': {('wishlist', 'variant', 'data')},
            },
        ),
    ]
