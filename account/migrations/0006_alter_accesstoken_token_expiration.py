# Generated by Django 3.2 on 2021-04-16 14:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_accesstoken_token_expiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesstoken',
            name='token_expiration',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 16, 16, 59, 47, 955869)),
        ),
    ]
