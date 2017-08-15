# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_auto_20170814_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='invite_code',
            field=models.PositiveIntegerField(unique=True, null=True),
        ),
    ]
