# Generated by Django 5.0.4 on 2024-05-02 22:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vendor", "0002_rename_on_time_delivery_rate_vendor_delivery_rate_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="vendor",
            old_name="delivery_rate",
            new_name="on_time_delivery_rate",
        ),
        migrations.AlterField(
            model_name="purchaseorder",
            name="delivery_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 5, 9, 22, 0, 27, 351866, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
