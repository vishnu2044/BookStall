# Generated by Django 4.2.2 on 2023-08-01 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_cart', '0003_cart_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='coupon_discount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
