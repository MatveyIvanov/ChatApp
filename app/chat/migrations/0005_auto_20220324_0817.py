# Generated by Django 3.0.7 on 2022-03-24 08:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20220317_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='last_message_sender',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='chatroom',
            name='unread',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='chatroom',
            name='last_message',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 24, 8, 17, 28, 293349, tzinfo=utc)),
        ),
    ]