# Generated by Django 4.0.4 on 2022-05-02 05:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_post_mainphoto'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 2, 5, 45, 6, 137791, tzinfo=utc)),
        ),
    ]
