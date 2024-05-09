# Generated by Django 5.0.4 on 2024-05-08 07:50

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vendor", "0003_rename_delivery_rate_vendor_on_time_delivery_rate_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="purchaseorder",
            name="actual_delivery_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="purchaseorder",
            name="delivery_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 5, 15, 7, 50, 38, 137950, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="purchaseorder",
            name="issue_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="purchaseorder",
            name="quantity",
            field=models.PositiveIntegerField(),
        ),
    ]
