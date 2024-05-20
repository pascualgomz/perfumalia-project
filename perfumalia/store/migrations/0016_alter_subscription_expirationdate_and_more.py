# Generated by Django 5.0.2 on 2024-05-20 18:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_auto_20240519_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='expirationDate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='plan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.subscriptionplan'),
        ),
    ]