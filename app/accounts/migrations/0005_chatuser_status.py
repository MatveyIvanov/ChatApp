# Generated by Django 3.0.7 on 2022-03-17 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_chatuser_last_online'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatuser',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
