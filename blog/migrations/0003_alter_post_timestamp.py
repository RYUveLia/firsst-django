# Generated by Django 4.0.4 on 2022-05-06 08:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 6, 8, 21, 49, 957916, tzinfo=utc)),
        ),
    ]