# Generated by Django 4.1 on 2024-05-19 20:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0012_alter_cartitem_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="expirationDate",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 6, 19, 20, 21, 19, 17527, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
