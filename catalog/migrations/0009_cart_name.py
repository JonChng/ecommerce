# Generated by Django 4.2.11 on 2024-03-08 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0008_rename_price_cart_unit_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="name",
            field=models.CharField(default="", max_length=200),
        ),
    ]
