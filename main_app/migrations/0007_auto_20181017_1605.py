# Generated by Django 2.1.2 on 2018-10-17 16:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_auto_20181016_1844'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lineitem',
            name='size',
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.date(2018, 10, 17)),
        ),
    ]